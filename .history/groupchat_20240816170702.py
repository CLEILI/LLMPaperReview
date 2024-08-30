from autogen import UserProxyAgent,AssistantAgent,GroupChat,GroupChatManager,register_function,ConversableAgent
from setenvrion import get_llm_config,chatout_dir
from get_rag import get_all_rag
import sys
from typing import Callable
def regis_func(
    f: Callable,
    caller: ConversableAgent,
    executor: ConversableAgent,
    name: str,
    description: str,
    api_type:str,
) -> None:
    f = caller.register_for_llm(name=name, description=description,api_style=api_type)(f)
    executor.register_for_execution(name=name)(f)
    
def writeinfo(papername:str,score:str,comment:str)->str:
    with open(f"{chatout_dir}/second_round.txt", mode='a+') as filename:
        filename.write(papername)
        filename.write('\n')
        filename.write(score)
        filename.write('\n')
        filename.write(comment)
        filename.write('\n')
        filename.write('\n')
        return "Write Excute Success"
    
def group_chat(pdf:list,retrieval_functions:list):
    '''
    simulate the round table of paper review
    '''
    llm_config=get_llm_config()
    user_proxy=UserProxyAgent(
        name="user_proxy",
        code_execution_config=False,
        human_input_mode="NEVER",
        system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
        Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
        llm_config=llm_config,
    )
    chiefeditor=AssistantAgent(
        name="chiefeditor",
        llm_config=llm_config,
        system_message="You are a journal chiefeditor, as the Editor-in-Chief, you are joining the final round table discussion to review and finalize the publication's upcoming issue. Your responsibilities include leading the discussion, providing decisive input on the content lineup, and ensuring that all articles meet the publication's standards of quality and relevance. You will evaluate each piece for its contribution to the overall theme, make recommendations for last-minute edits, and address any concerns raised by the editorial team. Your goal is to ensure a cohesive and compelling issue that upholds the publication's voice and vision. Additionally, you are supposed to decide the scores and comments for each paper based on the discussion process",
        description="a journal chiefeditor who participate in the final review of paper",
    )
    subeditor=AssistantAgent(
        name="subeditor",
        llm_config=llm_config,
        system_message="You are a journal subeditor, as the Subeditor, you are joining the final round table discussion to contribute to the review and finalization of the publication's upcoming issue. Your role involves providing detailed feedback on the articles, ensuring grammatical accuracy, factual correctness, and adherence to the publication's style guide. You will collaborate with the Editor-in-Chief and other editorial team members to make any necessary last-minute edits and improvements. Your keen eye for detail and commitment to quality will help ensure that the final content is polished, engaging, and ready for publication.",
        description="a journal subeditor who participate in the final review of paper",
    )
    professor=AssistantAgent(
        name="professor",
        llm_config=llm_config,
        system_message="You are a professor, as a Professor, you are joining the final round table discussion to provide expert insights and academic perspectives on the topics being covered in the publication's upcoming issue. Your role involves critically evaluating the depth and accuracy of the content, ensuring that it meets high academic and intellectual standards. You will offer constructive feedback, suggest improvements, and help refine complex ideas to make them accessible to a broader audience. Your expertise will be invaluable in enhancing the quality and credibility of the publication, ensuring it delivers well-researched and thought-provoking content.",
        description="a professor who participate in the final review of paper"
    )

    groupchat=GroupChat(
        agents=[user_proxy,chiefeditor,subeditor,professor],
        messages=[],
        speaker_selection_method="auto",
        max_round=100,
        send_introductions=True,
        allow_repeat_speaker=False,
        func_call_filter=False,
    )
    for i in range(len(pdf)):
        j=0
        for assistant in [chiefeditor,subeditor,professor]:
            regis_func(
            retrieval_functions[pdf[i]],
            caller=assistant,
            executor=user_proxy,
            name=f"answer_{i}_{j}",
            description=f"useful when someone want to ask questions about the paper named \"{pdf[i]}\"",
            api_type="tool",
            )
            j+=1
    for role in [chiefeditor,subeditor,professor]:
        regis_func(
            writeinfo,
            caller=role,
            executor=user_proxy,
            name=f"writeinfo_{j}",
            description="useful when need to write papername, corresponding score and review comments into designative txt file",
            api_type="tool",
        )
        j+=1


    manager=GroupChatManager(groupchat=groupchat,llm_config=llm_config)
    standards="""
    1. The paper should have a strong research background and address an important question.
    2. The paper should have a complete paper structure.
    3. The paper should have a clear theme, analysis, and conclusion.
    4. The content of the paper must be original to enhance the existing knowledge system in the given topic area.
    5. Experiments, statistics, and other analyses must be conducted in accordance with high-tech standards and described in sufficient detail. Experiments, data, and analysis should be able to support the current conclusion.
    6. If there is algorithm design, it is necessary to ensure that the algorithm is feasible and effective.
    7. The conclusion must be clear, correct, reliable, and valuable.
    8. The paper should have a certain contribution and driving effect on the given thematic area.
    """
    message=rf'''
Now there is a round table to decide which papers should be accepted in a conference, please discuss and review the paper in {pdf}. In your questions, there should be the paper's name.

You should evaluate each paper accurately based on each of the following standards one by one:
{standards}
Pay attention to using uniform evaluation standards for all papers.

After evaluating all the standards, chiefeditor gives a final score of each paper based on the review comments and discuss process. (The maximum score is 100, which should be accurate to two decimal places.) Then, write the papername, score, and the review comments of each paper into the designative txt file.
The review comments should be personalized and pertinence and it should include the advantages and disadvantages of corresponding paper.

Dont write the writeinfo function again!
Note that the review comments should use a string and should not have a "\n". 
The score must be a string.
The papername that you wanna write should not have a ":".

Just terminate the conversation after all the papers are written into the txt file.

Start the work now.
'''
    sys.stdout=open(f"{chatout_dir}/chatout2","a+")
    user_proxy.initiate_chat(manager,message=message)

    sys.stdout=sys.__stdout__


def testfunc():
    pdfs=[
        "A Confidential Batch Payment Scheme with Integrated Auditing for Enhanced Data Trading Security",
        "A Flexible Numerology Resource Allocation to Guarantee Delay and Reliability Requirements in 5G NR-V2X Networks",
        "DesTest A Decentralised Testing Architecture for Improving Data Accuracy of Blockchain Oracle"
    ]
    get_llm_config()
    functions=get_all_rag(pdfs)
    group_chat(pdfs,functions)

#testfunc()
from autogen import UserProxyAgent,AssistantAgent,GroupChat,GroupChatManager,register_function,ConversableAgent
from setenvrion import get_llm_config,chatout_dir,pdf_dir
from get_rag_1 import get_all_rag
import sys,re,json,os
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
    
def group_chat(pdf:list,retrieval_function):
    '''
    simulate the round table of paper review
    '''
    llm_config=get_llm_config()
    user_proxy=UserProxyAgent(
        name="user_proxy",
        code_execution_config=False,
        human_input_mode="NEVER",
        #system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
        #Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
        is_termination_msg=lambda msg: "{\"comment\":" in str(msg["content"]) or "**Paper:**" in str(msg["content"]),
    )
    chiefeditor=AssistantAgent(
        name="chiefeditor",
        llm_config=llm_config,
        is_termination_msg=lambda msg: "{\"comment\":" in str(msg["content"]) or "**Paper:**" in str(msg["content"]),
        system_message="You are a journal chiefeditor, as the Editor-in-Chief, you are joining the final round table discussion to review and finalize the publication's upcoming issue. Your responsibilities include leading the discussion, providing decisive input on the content lineup, and ensuring that all papers meet the publication's standards of quality and relevance. You will evaluate each piece for its contribution to the overall theme, make recommendations for last-minute edits, and address any concerns raised by the editorial team. Your goal is to ensure a cohesive and compelling issue that upholds the publication's voice and vision. Additionally, you are supposed to decide the scores and comments for each paper based on the discussion process",
        description="a journal chiefeditor who participate in the final review of paper",
    )
    subeditor=AssistantAgent(
        name="subeditor",
        llm_config=llm_config,
        is_termination_msg=lambda msg: "{\"comment\":" in str(msg["content"]) or "**Paper:**" in str(msg["content"]),
        system_message="You are a journal subeditor, as the Subeditor, you are joining the final round table discussion to contribute to the review and finalization of the publication's upcoming issue. Your role involves providing detailed feedback on the papers, ensuring grammatical accuracy, factual correctness, and adherence to the publication's style guide. You will collaborate with the Editor-in-Chief and other editorial team members to make any necessary last-minute edits and improvements. Your keen eye for detail and commitment to quality will help ensure that the final content is polished, engaging, and ready for publication.",
        description="a journal subeditor who participate in the final review of paper",
    )
    professor=AssistantAgent(
        name="expert",
        llm_config=llm_config,
        is_termination_msg=lambda msg: "{\"comment\":" in str(msg["content"]) or "**Paper:**" in str(msg["content"]),
        system_message="You are a journal expert, as a expert, you are joining the final round table discussion to provide expert insights and academic perspectives on the topics being covered in the publication's upcoming issue. Your role involves critically evaluating the depth and accuracy of the content, ensuring that it meets high academic and intellectual standards. You will offer constructive feedback, suggest improvements, and help refine complex ideas to make them accessible to a broader audience. Your expertise will be invaluable in enhancing the quality and credibility of the publication, ensuring it delivers well-researched and thought-provoking content.",
        description="a journal expert who participate in the final review of paper"
    )

    groupchat=GroupChat(
        agents=[user_proxy,chiefeditor,subeditor,professor],
        messages=[],
        speaker_selection_method="round_robin",
        max_round=100,
        send_introductions=True,
        allow_repeat_speaker=False,
        #func_call_filter=False,
    )
    for i in range(len(pdf)):
        j=0
        for assistant in [chiefeditor,subeditor,professor]:
            regis_func(
            retrieval_function,
            caller=assistant,
            executor=user_proxy,
            name=f"answer_{i}_{j}",
            description=f"useful when someone want to evaluate or ask questions about the paper named \"{pdf[i]}\"",
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
Now there is a final round table to decide which papers should be accepted in a conference, the three roles of chiefeditor, subeditor and expert should discuss and review the papers in {pdf}. 

To review the papers, they must finish this job step-by-step:
- Step 1:EVALUATE EVERY PAPER. 
They should review and evaluate each paper accurately based on each of the following standards one by one:
{standards}
Pay attention to using uniform evaluation standards for all papers. In their questions, there must be the paper's name.
Here are the examples of their questions:
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' have a strong research background and address an important question?"
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' have a complete paper structure?"
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' have a clear theme, analysis, and conclusion?"
"Is the content of 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' original and does it enhance the existing knowledge system in the given topic area?"
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' conduct experiments, statistics, and analyses in accordance with high-tech standards and describe them in sufficient detail?"
"Is the algorithm in 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' feasible and effective?"
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' have a clear, correct, reliable, and valuable conclusion?"
"Does the paper 'FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN' have a certain contribution and driving effect on the given thematic area?"

- Step 2:COMPARE ALL PAPERS. 
They should compare the advantages and disadvantages of all papers in {pdf} and give a rank of these papers.

- Step 3:GENERATE REVIEW COMMENTS.
They must generate the review comments of every paper. The review comments of each paper should be personalized and pertinence and it should include the advantages and disadvantages of corresponding paper.

- Step 4:SCORE ALL PAPERS.
They must think step by step. Then decide a final score of every paper based on the responses of all tool calls and the comparison. (The maximum score is 100, which should be accurate to two decimal places.) 

- Step 5:EXPLAIN THE SCORES.
At the same time, they must explain why they give that score to the papers. 

- Step 6:REPLY EVERY PAPER'S INFORMATION.
After they explain the scores, they just need to reply every paper's information in the template of the following examples and terminate the conversation.
Here is the template of one paper's information, you must follow this format to output the information:
**Paper:**\n<paper's name>\n
**Comment:**\n<comment on paper>\n
**Score:**\n<score of paper>\n
'''
    sys.stdout=open(f"{chatout_dir}/chatout2","a+")
    a=user_proxy.initiate_chat(manager,message=message,max_turns=100)
    sys.stdout=sys.__stdout__

    s=""
    for i in range(-1,-5,-1):
        if "**Paper:**" in a.chat_history[i]['content']:
            s=a.chat_history[i]['content']
            break

    pattern=r'\*\*Paper:\*\*\s*(.*?)\n\*\*Comment:\*\*\s*(.*?)\n\*\*Score:\*\*\s*([0-9.]+)'
    paper_sections = re.findall(pattern, s)
    if len(paper_sections)!=len(pdf):
        return False
    for element in paper_sections:
        writeinfo(element[0].replace(':','').replace('\n','').rstrip(),element[2],element[1].replace('\n',''))
        
    return True


def testfunc():
    get_llm_config()
    pdfs=[]
    pdfs_path=pdf_dir
    for filename in os.listdir(pdfs_path):#read all pdf names
        if filename.endswith('.pdf'):
            new_filename,_ = os.path.splitext(filename)
            pdfs.append(new_filename)
    function=get_all_rag(pdfs[0:3])
    group_chat(pdfs,function)

#testfunc()#4o model problem
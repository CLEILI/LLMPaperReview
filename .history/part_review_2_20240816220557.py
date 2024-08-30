import os
from autogen import AssistantAgent,UserProxyAgent,register_function
import sys
from setenvrion import get_llm_config,template_dir,image_dir,chatout_dir,layout_config,googleSearchKey,workload
from serpapi import GoogleSearch
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from get_rag import get_all_rag
def check_layout(pdfname:str)->str:
    '''
    Filter out papers that do not meet the standard template
    '''
    templatestr=""
    templatepath=template_dir
    for filename in os.listdir(templatepath):
        templatestr+=f"<img src=\"{templatepath}/{filename}\">.\n\t"
    image_agent = MultimodalConversableAgent(
        name="image-explainer",
        #max_consecutive_auto_reply=10,
        #system_message="""Reply "TERMINATE" in the end when everything is done.""",
        llm_config=layout_config,
    )

    user_proxy =UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        human_input_mode="NEVER",  # Try between ALWAYS or NEVER
        max_consecutive_auto_reply=0,
        code_execution_config={
            "use_docker": False
        },
    )
    
    sys.stdout=open(chatout_dir+"/chatout1","a+")
    a=user_proxy.initiate_chat(
    image_agent,
    message=f"""
    This is the standard template for papers.
    {templatestr}
    Please check if the template of the following paper meets the standards.
    <img src="{image_dir}/{pdfname}.jpg">.
    For whether a template is suitable, please pay attention to their layout and the relative positions of the title, author, and abstract.
    At last just need to reply YES or NO.
    """,
)
    sys.stdout=sys.__stdout__
    flag=a.chat_history[-1]["content"]
    return flag

def writeinfo(papername:str,score:str,comment:str)->str:
    with open(chatout_dir+"/first_round.txt", mode='a+') as filename:#a+(append) w+(from top)
        filename.write(papername)
        filename.write('\n')
        filename.write(score)
        filename.write('\n')
        filename.write(comment)
        filename.write('\n')
        filename.write('\n')
        return "Write Excute Success"

def search_google_scholar(keyword:str)->str:
    search = GoogleSearch({  
        "q":keyword, 
        "engine": "google_scholar",
        "hl": "en",
        "num":5,
        #"tbm": "", 
        "api_key":googleSearchKey  # https://serpapi.com/manage-api-key
    })
    result = search.get_dict()
    #print(result)
    return [item['snippet'] for item in result['organic_results']]

def review(pdf:list,retrieval_functions:dict):
    '''
    review the paper and record the conversation in chatout1
    '''
    assistant = AssistantAgent(
        name="assistant",
        llm_config=get_llm_config(),
    )

    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        #max_consecutive_auto_reply=4,
        code_execution_config=False,
        llm_config=get_llm_config(),
        system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
        Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
        #function_map={f"answer_{i}": retrieval_functions[pdf[i]] for i in range(len(pdf))}
    )
    for i in range(len(pdf)):
        register_function(
        retrieval_functions[pdf[i]],
        caller=assistant,
        executor=user_proxy,
        name=f"answer_{i}",
        description=f"useful when you want to answer questions about the paper named \"{pdf[i]}\"",
    )
    register_function(
        writeinfo,
        caller=assistant,
        executor=user_proxy,
        name="writeinfo",
        description="useful when need to write papername, corresponding score and review comments into designative txt file",
    )
    '''register_function(
        search_google_scholar,
        caller=assistant,
        executor=user_proxy,
        name="search_google_scholar",
        description="useful when need to see a paper's originality and innovation",
    )'''

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
    message=rf"""
    Assume you are a reviewer of a conference, your job is to review papers in {pdf} and give every paper a reasonable score.
    
    To find the paper related content, you are supposed to call answer functions. In your question, there must be the paper's name!
    You cannot ask vague questions. It is recommended that your questions based on each of the following standords. 
    
    To review the {workload} papers, you should check that if every paper in {pdf} meets each of the following standards one bye one: 
    {standards}
    Pay attention to using uniform evaluation standards for all papers.

    After evaluating all the standards, you must think step by step, compare all papers and decide a final score of every paper based on the responses of all tool calls. (The maximum score is 100, which should be accurate to two decimal places.) 
    The review comments of each paper should be personalized and pertinence and it should include the advantages and disadvantages of corresponding paper.

    At last, you just need to reply every paper's information.
    Here is an example of two papers' information:
{"comment": "This paper presents original and effective methodology for indoor localization, validated by extensive experiments. Further analysis on the algorithm's scalability could improve its contribution to the field.", "papername": "FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN", "score": "90.00"}
{"comment": "It contributes valuable solutions for blockchain integration, demonstrating effective approaches for merging diverse systems. Inclusion of additional real-world case studies would enhance its practical relevance.", "papername": "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems", "score": "80.00"}

    Start the work now.
    """
    
    sys.stdout=open(chatout_dir+"/chatout1","a+")
    user_proxy.initiate_chat(assistant,message=message)
    sys.stdout=sys.__stdout__


def testfunc():
    get_llm_config()
    pdf=["A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm",
         "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems",
         "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario",]
    retrieval_function=get_all_rag(pdf)
    review(pdf,retrieval_function)


testfunc()
    
import os,json,re
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

def review(pdf:list,retrieval_function:dict):
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
        is_termination_msg=lambda msg: "{\"comment\":" in str(msg["content"]),
    )
    for i in range(len(pdf)):
        register_function(
        retrieval_function,
        caller=assistant,
        executor=user_proxy,
        name=f"answer_{i}",
        description=f"useful when you want to answer questions about the paper named \"{pdf[i]}\"",
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
    message=f"""
    Assume you are a reviewer of a conference, your job is to review papers in {pdf} and give every paper a reasonable score.
    
    To find the paper related content, you are supposed to call answer functions. In your question, there must be the paper's name!
    You cannot ask vague questions. It is recommended that your questions based on each of the following standords. 
    
    To review the papers, you should check that if every paper in {pdf} meets each of the following standards one bye one: 
    {standards}
    Pay attention to using uniform evaluation standards for all papers.

    After evaluating all the standards, you must think step by step, compare all papers and decide a final score of every paper based on the responses of all tool calls. (The maximum score is 100, which should be accurate to two decimal places.) 
    The review comments of each paper should be personalized and pertinence and it should include the advantages and disadvantages of corresponding paper.

    At last, you just need to reply every paper's information.
    Here is an example of two papers' information:
{{"comment": "This paper presents original and effective methodology for indoor localization, validated by extensive experiments. Further analysis on the algorithm's scalability could improve its contribution to the field.", "papername": "FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN", "score": "90.00"}}
{{"comment": "It contributes valuable solutions for blockchain integration, demonstrating effective approaches for merging diverse systems. Inclusion of additional real-world case studies would enhance its practical relevance.", "papername": "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems", "score": "80.00"}}

    Start the work now.
    """
    
    sys.stdout=open(chatout_dir+"/chatout1","a+")
    a=user_proxy.initiate_chat(assistant,message=message)
    sys.stdout=sys.__stdout__

    s=""
    for i in range(-1,-5,-1):
        if "{\"comment\":" in a.chat_history[i]['content']:
            s=a.chat_history[i]['content']
            break
    
    pattern = r'\{.*?"comment".*?"papername".*?"score".*?\}'
    matches = re.findall(pattern, s)

    for element in matches:
        pdfdic=json.loads(element)
        writeinfo(pdfdic['papername'].replace(':',''),pdfdic['score'],pdfdic['comment'].replace('\n',''))

    return a



def testfunc():
    get_llm_config()
    pdf=["A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm",
         "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems",
         "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario",]
    retrieval_function=get_all_rag(pdf)
    review(pdf,retrieval_function)


'''d={'content': '{"comment": "This paper introduces a framework utilizing deep learning techniques to enhance data quality in mobile crowd sensing. It presents innovative solutions to current gaps related to data reliability, although specific details regarding the completeness of the paper structure and high-tech standards for experiments are lacking. The results are promising but require comprehensive validation. The conclusion presented is relevant, but its overall reliability needs further evaluation.", "papername": "A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm", "score": "78.00"}\n{"comment": "This paper effectively addresses the pressing issue of blockchain integration through two distinct methodologies. It provides a strong structure and clear analysis, successfully demonstrating the proposed solutions\' potential impact on blockchain interoperability. While the conclusion is valuable, further empirical validation would enhance its credibility. The contributions are significant and offer promising directions for future research in this thematic area.", "papername": "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems", "score": "85.00"}\n{"comment": "This paper proposes a novel approach to enhance physical layer security in mobile communication via cooperative jamming. While it provides significant contributions to the field and addresses key challenges, some details regarding the comprehensiveness of experimental validation were not assessed. Nevertheless, the conclusions drawn about the scheme\'s effectiveness are insightful and indicate a strong potential for future developments in secure transmission.", "papername": "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario", "score": "82.00"}', 'role': 'assistant'}
ss=d["content"]
pdfs=ss.split("\n")
print(pdfs)
dd1=json.loads(pdfs[0])
dd2=json.loads(pdfs[1])
dd3=json.loads(pdfs[2])
print(dd1['comment'])
print(dd1['score'])
print(dd1['papername'])'''
testfunc()
#is terminate msg[content]={"comment"
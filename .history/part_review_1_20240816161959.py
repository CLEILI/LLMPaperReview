import os
from autogen import AssistantAgent,UserProxyAgent,register_function
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from chromadb.utils import embedding_functions
import sys
from setenvrion import get_llm_config,template_dir,image_dir,chatout_dir,layout_config,googleSearchKey,workload,pdf_dir,ModelName
from serpapi import GoogleSearch
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from get_rag import get_all_rag
from langchain.text_splitter import RecursiveCharacterTextSplitter
RAGPROMPT='''
You're a retrieve augmented chatbot. You answer user's questions based on your own knowledge and the context provided by the user. You must think step-by-step.
First, please learn the following examples of context and question pairs and their corresponding answers.

Context:
Kurram Garhi: Kurram Garhi is a small village located near the city of Bannu, which is the part of Khyber Pakhtunkhwa province of Pakistan. Its population is approximately 35000.
Trojkrsti: Trojkrsti is a village in Municipality of Prilep, Republic of Macedonia.
Q: Are both Kurram Garhi and Trojkrsti located in the same country?
A: Kurram Garhi is located in the country of Pakistan. Trojkrsti is located in the country of Republic of Macedonia. Thus, they are not in the same country. So the answer is: no.


Context:
Early Side of Later: Early Side of Later is the third studio album by English singer- songwriter Matt Goss. It was released on 21 June 2004 by Concept Music and reached No. 78 on the UK Albums Chart.
What's Inside: What's Inside is the fourteenth studio album by British singer- songwriter Joan Armatrading.
Q: Which album was released earlier, What'S Inside or Cassandra'S Dream (Album)?
A: What's Inside was released in the year 1995. Cassandra's Dream (album) was released in the year 2008. Thus, of the two, the album to release earlier is What's Inside. So the answer is: What's Inside.


Context:
Maria Alexandrovna (Marie of Hesse): Maria Alexandrovna , born Princess Marie of Hesse and by Rhine (8 August 1824 – 3 June 1880) was Empress of Russia as the first wife of Emperor Alexander II.
Grand Duke Alexei Alexandrovich of Russia: Grand Duke Alexei Alexandrovich of Russia,(Russian: Алексей Александрович; 14 January 1850 (2 January O.S.) in St. Petersburg – 14 November 1908 in Paris) was the fifth child and the fourth son of Alexander II of Russia and his first wife Maria Alexandrovna (Marie of Hesse).
Q: What is the cause of death of Grand Duke Alexei Alexandrovich Of Russia's mother?
A: The mother of Grand Duke Alexei Alexandrovich of Russia is Maria Alexandrovna. Maria Alexandrovna died from tuberculosis. So the answer is: tuberculosis.


Context:
Laughter in Hell: Laughter in Hell is a 1933 American Pre-Code drama film directed by Edward L. Cahn and starring Pat O'Brien. The film's title was typical of the sensationalistic titles of many Pre-Code films.
Edward L. Cahn: Edward L. Cahn (February 12, 1899 – August 25, 1963) was an American film director.
Q: When did the director of film Laughter In Hell die?
A: The film Laughter In Hell was directed by Edward L. Cahn. Edward L. Cahn died on August 25, 1963. So the answer is: August 25, 1963.

Second, please complete the answer by thinking step-by-step.

Context:
{input_context}
Q: {input_question}
A:
'''
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

def review(pdf:list):
    '''
    review the paper and record the conversation in chatout1
    '''
    assistant = AssistantAgent(
        name="assistant",
        llm_config=get_llm_config(),
    )

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ["OPENAI_API_KEY"],
                api_base=os.environ["OPENAI_API_BASE"],
                model_name="text-embedding-ada-002",
            )
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000)

    ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    retrieve_config={
        "task": "qa",
        "docs_path": [
            f"{pdf_dir}/{name}.pdf" for name in pdf
        ],
        "embedding_function":openai_ef,
        "custom_text_split_function":text_splitter,
        "model": ModelName,
        "vector_db": "chroma",
        "overwrite": False,  # set to True if you want to overwrite an existing collection
        "get_or_create": True,  # set to False if don't want to reuse an existing collection
        "customized_prompt":RAGPROMPT,
    },
    code_execution_config=False,  # set to False if you don't want to execute the code
)

    register_function(
        writeinfo,
        caller=assistant,
        executor=ragproxyagent,
        name="writeinfo",
        description="useful when need to write papername, corresponding score and review comments into designative txt file",
    )


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
    
    To find the paper related content, you can ask ragproxyagent. In your question, there must be the paper's name!
    You cannot ask vague questions. It is recommended that your questions based on each of the following standords. 
    
    To review the {workload} papers, you should check that if every paper in {pdf} meets each of the following standards one bye one: 
    {standards}
    Pay attention to using uniform evaluation standards for all papers.

    After evaluating all the standards, please compare them and give a final score of every paper based on the responses of ragproxyagent. (The maximum score is 100, which should be accurate to two decimal places.) Then, write the papername, score, and the review comments of each paper into the designative txt file. 
    The review comments should be personalized and pertinence and it should include the advantages and disadvantages of corresponding paper. The review comments should not have a "\n". 

    Note that the assistant must call registered writeinfo function at the end of the conversation to write the above information and ragproxyagent execute the writeinfo function! Don't need to write code again! The papername that you wanna write should not have a ":".
    Please check if all papers have been written to the file. If so, just terminate the conversation.

    Start the work now.
    """
    
    sys.stdout=open(chatout_dir+"/chatout1","a+")
    ragproxyagent.initiate_chat(assistant,message=message)
    sys.stdout=sys.__stdout__


def testfunc():
    get_llm_config()
    pdf=["A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm",
         "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems",
         "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario",]
    retrieval_function=get_all_rag(pdf)
    review(pdf,retrieval_function)


#testfunc()
    
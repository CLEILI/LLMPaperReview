from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
#from langchain_community.document_loaders.pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
#from langchain.chains.conversational_retrieval.base
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.vectorstores import VectorStoreRetriever
#from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.llms import AnthropicLLM
from langchain.memory import ConversationBufferMemory,ConversationSummaryMemory
#from langchain.chains.conversational_retrieval.base 
#from langchain_community.document_loaders.pdf
#from langchain.chains.retrieval_qa.base
import os
from setenvrion import pdf_dir,md_dir,ModelName,closeModel,get_llm_config,ollamamodel,glmmodel,dashmodel,glmkey,glmurl,dashurl


def get_all_rag(allpdf:list):
    '''
    
    retrieval_functions(question)

    '''
    #loader[pdfname]=pypdfloader
    loaders={}
    for title in allpdf:
        loaders[title]=UnstructuredMarkdownLoader(f"{md_dir}/{title}/pdfs/{title}.pdf.md",mode="single")
    #vectorStores[pdfname]=vector
    vectorStores={}
    QA={}
    qaend=None
    i=0
    for pdfname,pdfloader in loaders.items():
        docs=[]
        docs.extend(pdfloader.load())
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000)
        docs=text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings(
                    openai_api_key=os.environ["OPENAI_API_KEY"],
                    openai_api_base=os.environ["OPENAI_API_BASE"],
                )
        #client=chromadb.HttpClient()#use "chroma run" first
        vectorstore=Chroma(collection_name="fullpdf",embedding_function=embeddings)

        vectorstore.add_documents(docs)
        #llm=ChatAnthropic(model_name="claude-3-5-sonnet-20240620",temperature=0,base_url="https://ai-yyds.com/v1")
        if ModelName in ollamamodel:
            llm=ChatOllama(model=ModelName)
        elif ModelName in glmmodel:
            llm=ChatZhipuAI(temperature=0.1,
                            api_key=glmkey,
                            model=ModelName,
                            base_url=glmurl,
                            )
        elif ModelName in dashmodel:
            llm=ChatOpenAI(model=ModelName,
                           base_url=dashurl,
                           api_key=os.environ["DASHSCOPE_API_KEY"],
                           temperature=0,
                           )
        elif ModelName=="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo":
            llm=ChatOpenAI(model=ModelName,
                base_url="https://api.aimlapi.com/v1",
                temperature=0,
                api_key="97891b4aa9044f8eb4ce07127d85c5bd",
                )
        elif ModelName in closeModel:
            llm=ChatOpenAI(model=ModelName,
                           base_url=os.environ["OPENAI_API_BASE"],
                           temperature=0,
                           api_key=os.environ["OPENAI_API_KEY"],
                           )
            
        qa=RetrievalQA.from_chain_type(
            llm, 
            retriever=vectorstore.as_retriever(),
        )
        #print(qa({"question":"what is the abstract of this paper?"})["answer"])
        QA[pdfname]=qa
        #print(qa({"question":"what is the contribution of \'A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems\'?"})["answer"])
        qaend=qa
        print(f"{i} embeded")
        i+=1

    #retrieval_functions[pdfname]=func
    '''retrieval_functions={}
    for pdfname_2,vecqa in QA.items():
        def func(question:str)->str:
            return vecqa({"question": question})["answer"]
        #print(func("What is the abstract of this paper?"))
        globals()[f"answer_{pdfname_2}"]=func
        retrieval_functions[pdfname_2]=func'''

    def func(question:str)->str:
        return qaend.run(question)
    globals()["funcqa"]=func
    return func

def testfunc():
    get_llm_config()
    pdf=[#"A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm",
         "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems",
         #"An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario",
         "FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN",
         #"BCPP-IAS Blockchain-Based Cross-Domain Identity Authentication Scheme for IoT with Privacy Protection",
         #"A DRL-Based Hierarchical Game for Physical Layer Security Aware Cooperative Communications",
         ]
    qafunc=get_all_rag(pdf)
    for p in pdf:
        print(qafunc(f"what is the contribution of {p}?"))

#testfunc()
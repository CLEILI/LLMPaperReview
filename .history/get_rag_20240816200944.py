from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_community.chat_models.ollama import ChatOllama
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
#from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.llms import AnthropicLLM
from langchain.memory import ConversationBufferMemory,ConversationSummaryMemory
#from langchain.chains.conversational_retrieval.base 
#from langchain_community.document_loaders.pdf
#from langchain.chains.retrieval_qa.base
import os
from setenvrion import pdf_dir,ModelName,closeModel,get_llm_config


def get_all_rag(allpdf:list)->dict:
    '''
    
    retrieval_functions[pdfname](question)

    '''
    #loader[pdfname]=pypdfloader
    loaders={}
    for title in allpdf:
        loaders[title]=PyMuPDFLoader(pdf_dir+f"/{title}.pdf")
    #vectorStores[pdfname]=vector
    vectorStores={}
    QA={}

    for pdfname,pdfloader in loaders.items():
        docs=[]
        docs.extend(pdfloader.load())
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000)
        docs=text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings(
                    openai_api_key="sk-hLujscYN1BoKClcIEe5aC103A1164909Ae2fBb1a7dE2DbC4",
                    openai_api_base="https://ai-yyds.com/v1",
                )
        #client=chromadb.HttpClient()#use "chroma run" first
        vectorstore=Chroma(collection_name="fullpdf",embedding_function=embeddings)

        vectorstore.add_documents(docs)
        #llm=ChatAnthropic(model_name="claude-3-5-sonnet-20240620",temperature=0,base_url="https://ai-yyds.com/v1")
        if ModelName not in closeModel:
            llm=ChatOllama(model=ModelName)
        else:
            llm=ChatOpenAI(model=ModelName,
                           base_url=os.environ["OPENAI_API_BASE"],
                           temperature=0,
                           api_key=os.environ["OPENAI_API_KEY"],
                           )
            llm1=ChatAnthropic(
                            model=ModelName,
                            api_key=os.environ["OPENAI_API_KEY"],
                            base_url=os.environ["OPENAI_API_BASE"],
                            temperature=0,
            )
        qa =ConversationalRetrievalChain.from_llm(
        llm,
        #OpenAI(temperature=0,openai_api_base="https://ai-yyds.com/v1",model_name="gpt-4-turbo"),
        vectorstore.as_retriever(),
        memory=ConversationBufferMemory(memory_key="chat_history",return_messages=True)
        )
        #print(qa({"question":"what is the abstract of this paper?"})["answer"])
        QA[pdfname]=qa
        
    #retrieval_functions[pdfname]=func
    retrieval_functions={}
    for pdfname_2,vecqa in QA.items():
        def func(question:str)->str:
            return vecqa({"question": question})["answer"]
        #print(func("What is the abstract of this paper?"))
        globals()[f"answer_{pdfname_2}"]=func
        retrieval_functions[pdfname_2]=func

    return retrieval_functions

def testfunc():
    get_llm_config()
    pdf=["A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm",
         "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems",
         "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario",]
    retrieval_function=get_all_rag(pdf)
    for i in range(0,5):
        for paper in pdf:
            print(retrieval_function[paper](f"what is the contribution of {paper}"))

#testfunc()
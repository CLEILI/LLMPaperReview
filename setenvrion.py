import os,math

AcceptRate=0.4#114/290,for the acceptrate,we design strategy like 5->3->2
#for ensuring the acceptrate,plz set the pdf numbers to be times of workload, current is 5x.

chatout_dir="./txt"
log_dir="./log"
execute_log="./executelog"
pdf_dir="./paper_pdfs copy"
#NOTE:this,recover check layout,global FirstNum,FinalNum

template_dir="./layout_template"
image_dir="./images"
xls_dir="./xls"
workload=10#num of reviewing paper per agent
random_round=1#num of repeat rounds for reviewing a group of papers
ModelName="gpt-4o-mini"

closeModel=["gpt-4o-2024-08-06","gpt-4o-mini","gpt-3.5-turbo",
            "gpt-4o","gpt-4o-mini-2024-07-18","o1-mini"]
ollamamodel=["llama3.1:8b","llama3.1:70b"]
glmmodel=["GLM-4-Plus","GLM-4-Flash","GLM-4-AllTools"]
dashmodel=["qwen2-72b-instruct","qwen-turbo","qwen2-57b-a14b-instruct","qwen2-1.5b-instruct","llama3.1-405b-instruct"]

glmurl="https://open.bigmodel.cn/api/paas/v4"
glmkey="3c2b712fc2f9af2ba23e535db9e23ca5.euNNHTo6PeoZm29V"#cant run,NoneType

os.environ["DASHSCOPE_API_KEY"]="sk-b3b1fb112de74a3db97b8ec467567c3c"
dashurl="https://dashscope.aliyuncs.com/compatible-mode/v1"#isok

layout_config={
    #"request_timeout": 180,
    "seed": 42,
    "config_list": [
    {
        "model": "gpt-4o",
        "base_url": "https://api.tata-api.com/v1",
        "api_key": "sk-xADQYFF4GtkR8FpA30E97684D7D34574BeF61c91833a1025",
    },
    ],
    "temperature": 0,
}
googleSearchKey="0ca78427c545e26205ece6b7ca4448555a77fecaeb753e4a4201a606feb86a2c"

def get_llm_config()->dict:
    '''
    set the temporary LLM variable environment
    '''
    
    os.environ["OPENAI_API_KEY"]="sk-88cKKnjijXIVqgAFE48c5b0775E9472d8c09111c4a5e8080"
    os.environ["OPENAI_API_BASE"] = "https://api.tata-api.com/v1"
    
    config={}
    config["gpt-4o-2024-08-06"] = [
    {
        "model": "gpt-4o-2024-08-06",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["gpt-4o"] = [
    {
        "model": "gpt-4o",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["o1-mini"] = [
    {
        "model": "o1-mini",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["gpt-4o-mini"] = [
    {
        "model": "gpt-4o-mini",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["gpt-3.5-turbo"] = [
    {
        "model": "gpt-3.5-turbo",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["llama3.1:8b"]= [
    {
        "model": "llama3.1:8b",
        "base_url": "http://localhost:11434/v1",
        "api_type":"ollama",
        "api_key": "ollama",
    },
    ]
    config["llama3.1:70b"]= [
    {
        "model": "llama3.1:70b",
        "base_url": "http://localhost:6006/v1",
        "api_type":"ollama",
        "api_key": "ollama",
    },
    ]
    config["gpt-4o-mini-2024-07-18"]=[
    {
        "model": "gpt-4o-mini-2024-07-18",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    ]
    config["claude-3-5-sonnet-20240620"]=[
    {
        "model": "claude-3-5-sonnet-20240620",
        "base_url": os.environ["OPENAI_API_BASE"],
        "api_key": os.environ["OPENAI_API_KEY"],
        "api_type":"anthropic",
    },
    ]
    config["GLM-4-Plus"]=[
    {
        "model": "GLM-4-Plus",
        "base_url": glmurl,
        "api_key": glmkey,
    },
    ]
    config["qwen2-1.5b-instruct"]=[
    {
        "model": "qwen2-1.5b-instruct",
        "base_url": dashurl,
        "api_key": os.environ["DASHSCOPE_API_KEY"],
    },
    ]
    config["qwen-turbo"]=[
    {
        "model": "qwen-turbo",
        "base_url": dashurl,
        "api_key": os.environ["DASHSCOPE_API_KEY"],
    },
    ]#ok
    
    config["qwen2-57b-a14b-instruct"]=[
    {
        "model": "qwen2-57b-a14b-instruct",
        "base_url": dashurl,
        "api_key": os.environ["DASHSCOPE_API_KEY"],
    },
    ]#ok
    config["qwen2-72b-instruct"]=[
    {
        "model": "qwen2-72b-instruct",
        "base_url": dashurl,
        "api_key": os.environ["DASHSCOPE_API_KEY"],
    },
    ]#ok
    config["llama3.1-405b-instruct"]=[
    {
        "model": "llama3.1-405b-instruct",
        "base_url": dashurl,
        "api_key": os.environ["DASHSCOPE_API_KEY"],
    },
    ]
    
    config["meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"]=[
    {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "base_url": "https://api.aimlapi.com/v1",
        "api_key": "97891b4aa9044f8eb4ce07127d85c5bd",#langchain is ok while autogen get wrong
    },
    ]
    llm_config = {
        "timeout": 120,
        "seed": 42,
        "config_list": config[ModelName],
        "temperature": 1,
        #for the 4o,4o-mini... may set 0.5,while 3.5-turbo should be 0 because it will ask random questions if set 0.5.
        #"stream":False
    }
    return llm_config


def ComputeNum():

    count=0
    for filename in os.listdir(pdf_dir):#read all pdf names
        if filename.endswith('.pdf'):
            count+=1
    #print(count)
    return count


TotalNum=ComputeNum()
FirstNum=174
#FirstNum=int(TotalNum*0.6)#290*0.6
#FinalNum=math.ceil(TotalNum*AcceptRate)
FinalNum=116
# the wrong layout papers' propotion should not be more than 40%
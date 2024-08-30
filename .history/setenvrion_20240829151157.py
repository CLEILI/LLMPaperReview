import os,math

AcceptRate=0.4#114/290,for the acceptrate,we design strategy like 5->3->2
#for ensuring the acceptrate,plz set the pdf numbers to be times of workload, current is 5x.

chatout_dir="./txt"
log_dir="./log"
execute_log="./executelog"
pdf_dir="./pdfs1"
template_dir="./layout_template"
image_dir="./images"
xls_dir="./xls"
workload=5#num of reviewing paper per agent
random_round=3#num of repeat rounds for reviewing a group of papers
ModelName="gpt-3.5-turbo"

closeModel=["gpt-4o-2024-08-06","gpt-4o-mini","gpt-3.5-turbo",
            "gpt-4o","gpt-4o-mini-2024-07-18",]
layout_config={
    #"request_timeout": 180,
    "seed": 42,
    "config_list": [
    {
        "model": "gpt-4o",
        "base_url": "https://ai-yyds.com/v1",
        "api_key": "sk-hLujscYN1BoKClcIEe5aC103A1164909Ae2fBb1a7dE2DbC4",
    },
    ],
    "temperature": 0,
}
googleSearchKey="0ca78427c545e26205ece6b7ca4448555a77fecaeb753e4a4201a606feb86a2c"

def get_llm_config()->dict:
    '''
    set the temporary LLM variable environment
    '''
    
    os.environ["OPENAI_API_KEY"]="sk-xADQYFF4GtkR8FpA30E97684D7D34574BeF61c91833a1025"
    os.environ["OPENAI_API_BASE"] = "https://api.tata-api.com/v1"
    
    '''os.environ["OPENAI_API_KEY"]="sk-hLujscYN1BoKClcIEe5aC103A1164909Ae2fBb1a7dE2DbC4"
    os.environ["OPENAI_API_BASE"] = "https://ai-yyds.com/v1"'''
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
    llm_config = {
        "timeout": 120,
        "seed": 42,
        "config_list": config[ModelName],
        "temperature": 0,
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
FirstNum=int(TotalNum*0.6)
FinalNum=math.ceil(TotalNum*AcceptRate)
# the wrong layout papers' propotion should not be more than 40%
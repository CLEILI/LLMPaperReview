'''
Each successfully execution's log may like:

llm_config
workload:5,random_round:1
2024.7.17
pdfs
1_round_0
shuffled pdfs
1_round_1
shuffled pdfs
1_round_2
first_round_pdfs
2_round_0
shuffled pdfs
2_round_1
shuffled pdfs
2_round_2
finalpdfs
duration time
Similarity is 
successful
'''
# if there is a line named 2_round_1, that shows the 2_round_1 has been successfully executed 
from setenvrion import log_dir,execute_log
from primary_screen import random_round
import os,re
def read_log():#recover need clear chatout and rank file
    '''
    read the log
    '''
    issuccess=True
    pdfs=[]
    successround=0
    if os.path.getsize(execute_log+"/record.log")==0:
        return issuccess,pdfs,0
    with open(execute_log+"/record.log","r") as f:
        lines=f.readlines()
        #there may have the situation that LLM forget to write the "-" in the papername. It request hands on change
        if lines[-1][:-1]!="successful":
            issuccess=False
            for i in range(-1,-(len(lines)),-1):
                if len(lines[i])>=1000:
                    pdfs=lines[i].split("#")
                    pdfs=pdfs[:-1]
                    break
            for i in range(-1,-(len(lines)),-1):
                if bool(re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$",lines[i][0:-1])):
                    return False,pdfs,0
                if lines[i][0]=='1' or lines[i][0]=='2':
                    successround=int(lines[i][0])
                    break
    return issuccess,pdfs,successround





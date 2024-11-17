#todo:it need a re-order code 
from primary_screen import ReviewedPaper
from setenvrion import log_dir,workload,random_round,workspace
from dealfile import conversation_log
import os
def secondary_screen_1()->list:
    selectedpdfs=[]
    for filename in os.listdir(workspace+"/out"):#read all out file
        if filename[0]=="2":
            f=open(f"{workspace}/out/{filename}","r")
            temp=[]
            lines=f.readlines()
            size=4
            r=0
            for i in range(0,len(lines),size):
                data=lines[i:i+size]
                a=ReviewedPaper()
                a.name=data[0][0:-1]#delete \n
                a.name=a.name.replace(':','')#delete ":"
                a.score=data[1][0:-1]
                a.comment=data[2][0:-1]
                a.rank=r
                temp.append(a)
                r=(r+1)%workload
            order_temp=sorted(temp,reverse=True)
            for i in range(0,2):
                if order_temp[i].comment!="":
                    selectedpdfs.append(order_temp[i].name)
    return selectedpdfs
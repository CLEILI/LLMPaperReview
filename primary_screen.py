from setenvrion import log_dir,workload,random_round,workspace
from dealfile import conversation_log
import os

class ReviewedPaper:
    def __init__(self):
        self.name=""
        self.score=""
        self.rank=""
        self.comment=""
    def __lt__(self, other):
        if self.score==other.score:
            return self.rank>other.rank
        return self.score<other.score
    
def cmp(r1:ReviewedPaper,r2:ReviewedPaper):
    if r1.score==r2.score:
        if r1.rank<r2.rank:
            return 1
        else:
            return -1
    else:
        if r1.score<r2.score:
            return 1
        else:
            return -1
def primary_screen_1()->list:

    selectedpdfs=[]
    for filename in os.listdir(workspace+"/out"):#read all out file
        if filename[0]=="1":
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
            for i in range(0,3 if len(order_temp)>=3 else len(order_temp)):
                if order_temp[i].comment!="":
                    selectedpdfs.append(order_temp[i].name)
    return selectedpdfs
            
def getpdfs(path:str):
    pdfset=set()
    with open(path, 'r') as f:
        lines=f.readlines()
        size=4
        for i in range(0,len(lines),size):
            data=lines[i:i+size]
            pdfname=data[0][0:-1]
            pdfname=pdfname.replace(":","")
            pdfset.add(pdfname)
    pdflist=list(pdfset)
    return pdflist


def testfunc():
    l=primary_screen_1()
    print("-----")
    print(l)
    print(len(l))

#testfunc()
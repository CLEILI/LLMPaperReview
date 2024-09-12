from setenvrion import chatout_dir,log_dir,workload,random_round,FirstNum
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

def primary_screen()->list:
    '''
    resort the paper rank and get the 60% as the first round outcome
    '''
    dictlist=[]#dictlist[0][name]=reviewedpaper
    for k in range(0,random_round):
        f=open(f"{chatout_dir}/first_round_{k}.txt","r")
        paper={}
        struct=[]#all struct
        struct_1=[]#new all struct
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
            struct.append(a)
            r=(r+1)%workload
        for i in range(0,len(struct),workload):
            temp=struct[i:i+workload]
            order_temp=sorted(temp,reverse=True)
            for j in range(0,len(order_temp)):
                order_temp[j].rank=j#重新处理一下排序，防止agent排序出错
                struct_1.append(order_temp[j])
        
        for t in struct_1:
            if t.name not in paper:#sometime agent may write the difference info again.
                paper[t.name]=t
        dictlist.append(paper)
        print(f"{k} lenth is {len(paper)}")
    struct_2=[]
    maxi=0
    maxlen=len(dictlist[0])
    for i in range(0,len(dictlist)):
        if len(dictlist[i])>maxlen:
            maxi=i
        
    for name in dictlist[maxi]:#dictlist[0] is a dict like dict[name]=class
        totalscore=0
        totalrank=0
        totalcomment=""
        for i in range(0,len(dictlist)):
            """print(dictlist[i])
            print(name)
            print(name in dictlist[i])
            
            print(dictlist[i][name].score)
            print(type(dictlist[i][name].score)) 
            """
            if name in dictlist[i]:
                totalscore+=float(dictlist[i][name].score)
                totalrank+=float(dictlist[i][name].rank)
                totalcomment=totalcomment+dictlist[i][name].comment+"|"
            else:
                totalscore+=float(dictlist[maxi][name].score)
                totalrank+=float(dictlist[maxi][name].rank)
                totalcomment=totalcomment+dictlist[maxi][name].comment+"|"
        a=ReviewedPaper()
        a.name=name
        a.score=str(round(float(totalscore/random_round),2))
        a.rank=str(round(float(totalrank/random_round),2))
        a.comment=totalcomment

        if not any(ele.name==a.name for ele in struct_2):
            struct_2.append(a)
    print(f"final lenth {len(struct_2)}")
    sorted_struct_2=sorted(struct_2,reverse=True)
    if os.path.getsize(f"{chatout_dir}/first_round_final.txt")==0:
        with open(f"{chatout_dir}/first_round_final.txt","w+") as f:
            for temp in sorted_struct_2:
                f.write(temp.name)
                f.write("\n")
                f.write(temp.score)
                f.write("\n")
                f.write(temp.rank)
                f.write("\n")
                f.write(temp.comment)
                f.write("\n")
                f.write("\n")
    pdfs=[]
    for i in range(0,FirstNum):
        pdfs.append(sorted_struct_2[i].name)
    conversation_log(f"{chatout_dir}/first_round_final.txt",log_dir,"first_round_final")
    return pdfs

def getpdfs(path:str):
    pdfset=set()
    with open(path, 'r') as f:
        lines=f.readlines()
        size=4
        for i in range(0,len(lines),size):
            data=lines[i:i+size]
            pdfname=data[0][0:-1]
            pdfname=pdfname.replace(":"," ")
            pdfset.add(pdfname)
    pdflist=list(pdfset)
    return pdflist


def testfunc():
    l=primary_screen()
    print("-----")
    print(l)
    print(len(l))

#testfunc()
from get_rag import get_all_rag
#from get_ag_rag import get_all_rag_1
from part_review import review,check_layout
from setenvrion import get_llm_config,log_dir,pdf_dir,workload,random_round,workspace,processnum
from primary_screen import primary_screen_1,getpdfs,ReviewedPaper
from secondary_screen import secondary_screen_1
from groupchat import group_chat
from dealfile import copy_file,clear_file,conversation_log,write_log,durationtime,copyworkspace2log,clear_folder
from recover import read_log
from readxls import similarity
import os,random,datetime,threading,multiprocessing

RED="\033[31m"
MAGENTA = "\033[35m"
RESET = "\033[0m"#set for observing the terninal output information

#the api may full load and dont review some paper.
def check(allpdfs:list,round:int):
    if round==1:
        reviewedpdfs=[]
        needreview=[]
        for filename in os.listdir(workspace+"/out"):#read all out file
            if filename[0]=="1":
                f=open(f"{workspace}/out/{filename}","r")
                temp=[]
                lines=f.readlines()
                size=4
                r=0
                for i in range(0,len(lines),size):
                    data=lines[i:i+size]
                    reviewedpdfs.append(data[0][0:-1].replace(':',''))
        needreview=list(set(allpdfs).difference(set(reviewedpdfs)))

        for j in range(0,len(needreview),workload*10):# one loop at most 50 papers->10 process to reduce the load2api
            process1=[]
            for i in range(j,j+workload*10 if j+workload*10<len(needreview) else len(needreview),workload):#loop workload 
                pdf=needreview[i:i+workload]
                number=int(i/workload)
                process=multiprocessing.Process(target=retryreview,args=(1000+number,pdf,10000+i))
                #1003,10003 represent the checked review.
                process1.append(process)
                process.start()

            for process in process1:
                process.join()
        
    if round==2:
        reviewedpdfs=[]
        needreview=[]
        for filename in os.listdir(workspace+"/out"):#read all out file
            if filename[0]=="2":
                f=open(f"{workspace}/out/{filename}","r")
                lines=f.readlines()
                size=4
                for i in range(0,len(lines),size):
                    data=lines[i:i+size]
                    reviewedpdfs.append(data[0][0:-1].replace(':',''))
        needreview=list(set(allpdfs).difference(set(reviewedpdfs)))

        for j in range(0,len(needreview),workload*6):
                process2=[]
                for i in range(j,j+workload*6 if j+workload*6<len(needreview) else len(needreview),int(workload*0.6)):
                    pdf=needreview[i:i+int(workload*0.6)]
                    number=int(i/int(workload*0.6))
                    process=multiprocessing.Process(target=retrygroupchat,args=(1000+number,pdf,10000+i))
                    process2.append(process)
                    process.start()

                for process in process2:
                    process.join()

def retryreview(number:int,pdf:list,i:int):
    retrieval_function=get_all_rag(pdf)
    retry=10
    tag=False
    while not tag:
        tag=review(number,pdf,retrieval_function)#to prevent gpt just pre return {"comment" and get less paper outcome
        retry-=1
        if retry==0:
            break
    print(f"{MAGENTA}{i}-{i+len(pdf)} papers down{RESET}")

def retrygroupchat(number:int,pdf:list,i:int):
    retrieval_function=get_all_rag(pdf)
    retry=10
    tag=False
    while not tag:
        tag=group_chat(number,pdf,retrieval_function)
        retry-=1
        if retry==0:
            break
    print(f"{MAGENTA}{i}-{i+len(pdf)} papers down{RESET}")

def reviewallpaper():
    config=get_llm_config()#to set environment variable

    write_log(str(config))
    write_log(f"WorkLoad:{workload},RandomRound:{random_round}")
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    write_log(current_timestamp)

    pdfs=[]
    pdfs_path=pdf_dir
    for filename in os.listdir(pdfs_path):#read all pdf names
        if filename.endswith('.pdf'):
            new_filename,_ = os.path.splitext(filename)
            pdfs.append(new_filename)

    random.shuffle(pdfs)
    #NOTE: recover this section code
    '''for i in range(len(pdfs) - 1, -1, -1):
        if check_layout(pdfs[i])=="NO":
            print(f"{pdfs[i]} layout wrong")
            pdfs.remove(pdfs[i])#The num of wrong layout should be less that 40%
        print(f"{i} check down")'''
    write_log(pdfs)
    #retrieval_function=get_all_rag(pdfs)

    #TODO:add a function to deal with papers less than 5

    for j in range(0,len(pdfs),workload*processnum):# one loop at most 50 papers->10 process to reduce the load2api
        process1=[]
        for i in range(j,j+workload*processnum if j+workload*processnum<len(pdfs) else len(pdfs),workload):#loop workload 
            pdf=pdfs[i:i+workload]
            number=int(i/workload)
            process=multiprocessing.Process(target=retryreview,args=(number,pdf,i))
            process1.append(process)
            process.start()

        for process in process1:
            process.join()

    check(pdfs,1)
    write_log("1")

    first_round_pdfs=primary_screen_1()
    print(first_round_pdfs)
    print(len(first_round_pdfs))
    firsimilarity=similarity(first_round_pdfs)
    print(f"{MAGENTA}First round similarity is {firsimilarity}{RESET}")
    #TODO:for all pdfs
    #if firsimilarity<0.9:
    #    exit()
    write_log(f"firsimilarity is {firsimilarity}")
    write_log(first_round_pdfs)

    for j in range(0,len(first_round_pdfs),int(workload*0.6*processnum)):
        process2=[]
        for i in range(j,j+workload*0.6*processnum if j+workload*0.6*processnum<len(first_round_pdfs) else len(first_round_pdfs),int(workload*0.6)):
            pdf=first_round_pdfs[i:i+int(workload*0.6)]
            number=int(i/int(workload*0.6))
            process=multiprocessing.Process(target=retrygroupchat,args=(number,pdf,i))
            process2.append(process)
            process.start()

        for process in process2:
            process.join()

    
    check(first_round_pdfs,2)
    #write_log("2")

    internal=durationtime()
    final_pdfs=secondary_screen_1()
    print(f"Selected pdfs are \n{final_pdfs}")

    result=similarity(final_pdfs)
    print(f"Duration Time is {internal}")
    print(f"The result of this execution is {result}")

    write_log(final_pdfs)
    write_log(f"Duration Time is {internal}")
    write_log(f"Similarity is {result*100}%")
    write_log("successful")

    copyworkspace2log()
    clear_folder(f"{workspace}/chat")
    clear_folder(f"{workspace}/out")

def recover(pdfs:list,successround:int):
    get_llm_config()
    reviewed=[]
    load=0
    if successround==0:
        load=5
    else:
        load=3
    for filename in os.listdir(workspace+"/out"):#read all out file
        if filename[0]==str(successround+1):
            f=open(f"{workspace}/out/{filename}","r")
            lines=f.readlines()
            size=4
            r=0

            if len(lines)<(size*load):
                clear_file(f"{workspace}/out/{filename}")
                continue
            for i in range(0,len(lines),size):
                data=lines[i:i+size]
                a=ReviewedPaper()
                a.name=data[0][0:-1]#delete \n
                a.name=a.name.replace(':','')#delete ":"
                a.score=data[1][0:-1]
                a.comment=data[2][0:-1]
                a.rank=r
                reviewed.append(a.name)
                r=(r+1)%workload
    needreview=list(set(pdfs).difference(set(reviewed)))
    #retrieval_function=get_all_rag(needreview)

    if successround==0:
        for j in range(0,len(needreview),workload*processnum):
            process1=[]
            for i in range(j,j+workload*processnum if j+workload*processnum<len(needreview) else len(needreview),workload):#loop workload 
                pdf=needreview[i:i+workload]
                number=int(len(reviewed)/workload)+int(i/workload)
                process=multiprocessing.Process(target=retryreview,args=(number,pdf,i+len(reviewed)))
                process1.append(process)
                process.start()

            for process in process1:
                process.join()

        check(pdfs,1)
        write_log("1")
        first_round_pdfs=primary_screen_1()
        print(first_round_pdfs)
        print(len(first_round_pdfs))
        print(f"{MAGENTA}First round similarity is {similarity(first_round_pdfs)}{RESET}",)
        write_log(first_round_pdfs)

        for j in range(0,len(first_round_pdfs),int(workload*0.6*processnum)):
            process2=[]
            for i in range(j,j+workload*0.6*processnum if j+workload*0.6*processnum<len(first_round_pdfs) else len(first_round_pdfs),int(workload*0.6)):
                pdf=first_round_pdfs[i:i+int(workload*0.6)]
                number=int(i/int(workload*0.6))
                process=multiprocessing.Process(target=retrygroupchat,args=(number,pdf,i))
                process2.append(process)
                process.start()

            for process in process2:
                process.join()
        
        check(first_round_pdfs,2)
        internal=durationtime()
        final_pdfs=secondary_screen_1()
        print(f"Selected pdfs are \n{final_pdfs}")

        result=similarity(final_pdfs)
        print(f"Duration Time is {internal}")
        print(f"The result of this execution is {result}")

        write_log(final_pdfs)
        write_log(f"Duration Time is {internal}")
        write_log(f"Similarity is {result*100}%")
        write_log("successful")

        copyworkspace2log()
        clear_folder(f"{workspace}/chat")
        clear_folder(f"{workspace}/out")

    else:
        
        first_round_pdfs=primary_screen_1()
        print(f"{MAGENTA}First round similarity is {similarity(first_round_pdfs)}{RESET}",)
        write_log(first_round_pdfs)
        for j in range(0,len(needreview),int(workload*0.6*processnum)):
            process2=[]
            for i in range(j,int(j+workload*0.6*processnum) if j+workload*0.6*processnum<len(needreview) else len(needreview),int(workload*0.6)):
                pdf=needreview[i:i+int(workload*0.6)]
                number=int(len(reviewed)/3)+int(i/int(workload*0.6))
                process=multiprocessing.Process(target=retrygroupchat,args=(number,pdf,i+len(reviewed)))
                process2.append(process)
                process.start()

            for process in process2:
                process.join()
        
        check(pdfs,2)
        internal=durationtime()
        final_pdfs=secondary_screen_1()
        print(f"Selected pdfs are \n{final_pdfs}")

        result=similarity(final_pdfs)
        print(f"Duration Time is {internal}")
        print(f"The result of this execution is {result}")

        write_log(final_pdfs)
        write_log(f"Duration Time is {internal}")
        write_log(f"Similarity is {result*100}%")
        write_log("successful")

        copyworkspace2log()
        clear_folder(f"{workspace}/chat")
        clear_folder(f"{workspace}/out")
    
def main():
    issuccess,pdfs,successround=read_log()
    if issuccess:
        reviewallpaper()
    else:
        recover(pdfs,successround)


if __name__ == '__main__':
    main()
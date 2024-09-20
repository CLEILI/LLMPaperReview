from get_rag_1 import get_all_rag
#from get_ag_rag import get_all_rag_1
from part_review_2 import review,check_layout
from setenvrion import get_llm_config,chatout_dir,log_dir,pdf_dir,workload,random_round
from primary_screen import primary_screen,getpdfs
from secondary_screen import secondary_screen
from groupchat_1 import group_chat
from dealfile import copy_file,clear_file,conversation_log,write_log,chatoutclear,durationtime
from recover import read_log
from readxls import similarity
import os,random,datetime

RED="\033[31m"
MAGENTA = "\033[35m"
RESET = "\033[0m"#set for observing the terninal output information

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

    #NOTE: recover this section code
    '''for i in range(len(pdfs) - 1, -1, -1):
        if check_layout(pdfs[i])=="NO":
            print(f"{pdfs[i]} layout wrong")
            pdfs.remove(pdfs[i])#The num of wrong layout should be less that 40%
        print(f"{i} check down")'''

    write_log(pdfs)
    retrieval_function=get_all_rag(pdfs)

    #TODO:add a function to deal with papers less than 5

    for j in range(0,random_round):
        write_log(pdfs)

        for i in range(0,len(pdfs),workload):#loop workload 
            pdf=pdfs[i:i+workload]
            retry=10
            tag=False
            while not tag:
                tag=review(pdf,retrieval_function)#to prevent gpt just pre return {"comment" and get less paper outcome
                retry-=1
                if retry==0:
                    break
            print(f"{MAGENTA}First round {j} times {i}-{i+len(pdf)} papers down{RESET}")

        copy_file(chatout_dir+"/chatout1",chatout_dir+f"/chatout1_{j}")
        conversation_log(chatout_dir+"/chatout1",log_dir,f"chatout1_{j}")
        copy_file(chatout_dir+"/first_round.txt",chatout_dir+f"/first_round_{j}.txt")
        conversation_log(chatout_dir+"/first_round.txt",log_dir,f"first_round_{j}")
        clear_file(chatout_dir+"/chatout1")
        clear_file(chatout_dir+"/first_round.txt")
        #print(pdfs)
        random.shuffle(pdfs)
        write_log(f"1_round_{j}")

    first_round_pdfs=primary_screen()
    print(first_round_pdfs)
    print(len(first_round_pdfs))

    for j in range(0,random_round):
        write_log(first_round_pdfs)

        for i in range(0,len(first_round_pdfs),int(workload*0.6)):
            pdf=first_round_pdfs[i:i+int(workload*0.6)]
            retry=10
            tag=False
            while not tag:
                tag=group_chat(pdf,retrieval_function)
                retry-=1
                if retry==0:
                    break
            print(f"{MAGENTA}Second round {j} times {i}-{i+len(pdf)} papers down{RESET}")

        copy_file(chatout_dir+"/chatout2",chatout_dir+f"/chatout2_{j}")
        conversation_log(chatout_dir+"/chatout2",log_dir,f"chatout2_{j}")
        copy_file(chatout_dir+"/second_round.txt",chatout_dir+f"/second_round_{j}.txt")
        conversation_log(chatout_dir+"/second_round.txt",log_dir,f"second_round_{j}")
        clear_file(chatout_dir+"/chatout2")
        clear_file(chatout_dir+"/second_round.txt")
        #print(first_round_pdfs)
        random.shuffle(first_round_pdfs)
        write_log(f"2_round_{j}")
    
    internal=durationtime()
    final_pdfs=secondary_screen()
    print(f"Selected pdfs are \n{final_pdfs}")

    result=similarity(final_pdfs)
    print(f"Duration Time is {internal}")
    print(f"The result of this execution is {result}")

    write_log(final_pdfs)
    write_log(f"Duration Time is {internal}")
    write_log(f"Similarity is {result*100}%")
    write_log("successful")

    chatoutclear()

def recover_from_log(pdfs:str,successround:int):


    get_llm_config()
    

    round=int(successround/random_round)
    recoverbegin=successround%random_round
    firstbegin=0
    secondbegin=0
    firstend=0
    secondend=0
    reviewedpdfs=[]
    if round==0:
        reviewedpdfs=getpdfs(chatout_dir+"/first_round.txt")
        firstbegin=recoverbegin
        firstend=random_round
        secondbegin=0
        secondend=random_round

    elif round==1:
        reviewedpdfs=getpdfs(chatout_dir+"/second_round.txt")
        firstbegin=0
        firstend=0
        secondbegin=recoverbegin
        secondend=random_round

    
    needreviewed=list(set(pdfs).difference(set(reviewedpdfs)))
    print(f"recover begin {round+1}_{recoverbegin}")
    if successround==random_round*2-1:
        retrieval_function=get_all_rag(needreviewed)
    elif successround==random_round*2:
        print("Dont need embeding")
    else:
        retrieval_function=get_all_rag(pdfs)

    for j in range(firstbegin,firstend):
        write_log(pdfs)
        if round==0 and j==firstbegin:
            for i in range(0,len(needreviewed),workload):#loop workload 
                pdf=needreviewed[i:i+workload]
                retry=10
                tag=False
                while not tag:
                    tag=review(pdf,retrieval_function)
                    retry-=1
                    if retry==0:
                        break
                print(f"{RED}First round {j} times {i+len(reviewedpdfs)}-{i+len(pdf)+len(reviewedpdfs)} papers down{RESET}")
        else:
            for i in range(0,len(pdfs),workload):#loop workload 
                pdf=pdfs[i:i+workload]
                retry=10
                tag=False
                while not tag:
                    tag=review(pdf,retrieval_function)
                    retry-=1
                    if retry==0:
                        break
                print(f"{RED}First round {j} times {i}-{i+len(pdf)} papers down{RESET}")
        copy_file(chatout_dir+"/chatout1",chatout_dir+f"/chatout1_{j}")
        conversation_log(chatout_dir+"/chatout1",log_dir,f"chatout1_{j}")
        copy_file(chatout_dir+"/first_round.txt",chatout_dir+f"/first_round_{j}.txt")
        conversation_log(chatout_dir+"/first_round.txt",log_dir,f"first_round_{j}")
        clear_file(chatout_dir+"/chatout1")
        clear_file(chatout_dir+"/first_round.txt")
        print(pdfs)
        random.shuffle(pdfs)
        write_log(f"1_round_{j}")

    first_round_pdfs=primary_screen()
    #first_round_pdfs=pdfs
    print(first_round_pdfs)
    print(f"length of first round pdfs is {len(first_round_pdfs)}")
    write_log(first_round_pdfs)
    for j in range(secondbegin,secondend):
        write_log(first_round_pdfs)
        if round==1 and j==secondbegin:
            for i in range(0,len(needreviewed),int(workload*0.6)):#loop workload 
                pdf=needreviewed[i:i+int(workload*0.6)]
                retry=10
                tag=False
                while not tag:
                    tag=group_chat(pdf,retrieval_function)
                    retry-=1
                    if retry==0:
                        break    
                print(f"{RED}Second round {j} times {i+len(reviewedpdfs)}-{i+len(pdf)+len(reviewedpdfs)} papers down{RESET}")
        else:
            for i in range(0,len(first_round_pdfs),int(workload*0.6)):
                pdf=first_round_pdfs[i:i+int(workload*0.6)]
                retry=10
                tag=False
                while not tag:
                    tag=group_chat(pdf,retrieval_function)
                    retry-=1
                    if retry==0:
                        break
                print(f"{RED}Second round {j} times {i}-{i+len(pdf)} papers down{RESET}")
        copy_file(chatout_dir+"/chatout2",chatout_dir+f"/chatout2_{j}")
        conversation_log(chatout_dir+"/chatout2",log_dir,f"chatout2_{j}")
        copy_file(chatout_dir+"/second_round.txt",chatout_dir+f"/second_round_{j}.txt")
        conversation_log(chatout_dir+"/second_round.txt",log_dir,f"second_round_{j}")
        clear_file(chatout_dir+"/chatout2")
        clear_file(chatout_dir+"/second_round.txt")
        print(first_round_pdfs)
        random.shuffle(first_round_pdfs)
        write_log(f"2_round_{j}")
    
    internal=durationtime()
    final_pdfs=secondary_screen()
    print(f"Selected pdfs are \n{final_pdfs}")

    result=similarity(final_pdfs)
    print(f"Duration Time is {internal}")
    print(f"The result of this execution is {result}")

    write_log(final_pdfs)
    write_log(f"Duration Time is {internal}")
    write_log(f"Similarity is {result*100}%")
    write_log("successful")

    chatoutclear()
    
def main():
    issuccess,pdfs,successround=read_log()
    if issuccess:
        reviewallpaper()
    else:
        recover_from_log(pdfs,successround)


if __name__ == '__main__':
    main()
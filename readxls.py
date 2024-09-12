import pandas as pd
from setenvrion import xls_dir
import difflib

def ele_similar(str1,str2):
    threshold=0.9
    similarity = difflib.SequenceMatcher(None, str1, str2).ratio()
    return similarity>=threshold

def similarity(finalpdfs):

    df = pd.read_excel(f'{xls_dir}/WASAPaperList.xls',usecols=[1])
    # 打印DataFrame
    acceptpdfs=[]
    #print(df)
    #print(df.values[2,0])
    for i in range(2,116):
        acceptpdfs.append(df.values[i,0].replace(':',''))
    
    commonpdfs = []
    for str1 in acceptpdfs:
        for str2 in finalpdfs:
            if ele_similar(str1,str2):
                commonpdfs.append(str1)
    #print(acceptpdfs)
    #commonpdfs=[pdf for pdf in acceptpdfs if pdf in finalpdfs]

    return round(float(len(commonpdfs)/len(acceptpdfs)),4)

def test():
    finalstr='''

'''
    pdfs=finalstr.split('#')[:-1]
    print(similarity(pdfs))


#test()
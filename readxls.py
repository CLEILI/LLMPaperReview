import pandas as pd
from setenvrion import xls_dir
# 读取文件并得到DataFrame
def similarity(finalpdfs):

    df = pd.read_excel(f'{xls_dir}/WASAPaperList.xls',usecols=[1])
    # 打印DataFrame
    acceptpdfs=[]
    #print(df)
    #print(df.values[2,0])
    for i in range(2,116):
        acceptpdfs.append(df.values[i,0].replace(':',''))
        
    #print(acceptpdfs)
    commonpdfs=[pdf for pdf in acceptpdfs if pdf in finalpdfs]

    return round(float(len(commonpdfs)/len(acceptpdfs)),4)
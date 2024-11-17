import datetime,os,re,shutil
from setenvrion import log_dir,execute_log,workspace

def copy_file(source_file, destination_file):
    with open(source_file, 'r') as source:
        data = source.read()
    with open(destination_file, 'w+') as destination:
        destination.write(data)

def clear_file(source_file):
    with open(source_file, 'w+') as source:
        source.truncate(0)

def clear_folder(folder_path):

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
        
def conversation_log(source_file, destination_path,name):
    '''
    record all execution outcome with a timestamp
    '''
    with open(source_file, 'r') as source:
        data = source.read()
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    filename=destination_path+"/"+current_timestamp+"_"+name+".txt"
    with open(filename, 'w+') as f:
        f.write(data)
def write_log(content):
    '''
    write paper list or complete str into the log file
    '''
    if type(content) is list:
        with open(execute_log+"/record.log","a+") as f:
            for papername in content:
                f.write(papername+"#")# use # as a seperater
            f.write("\n")
    elif type(content) is str:
        with open(execute_log+"/record.log","a+") as f:
            f.write(content)
            f.write("\n")

def durationtime():
    startime=""
    with open(execute_log+"/record.log","r") as f:
        lines=f.readlines()
        for i in range(-1,-(len(lines)),-1):
            if bool(re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$",lines[i][0:-1])):
                startime=lines[i][0:-1]
                break
    start = datetime.datetime.strptime(startime, "%Y-%m-%d %H:%M:%S.%f")
    now=datetime.datetime.now()

    internal=now-start

    return str(internal)

def copyworkspace2log():
    new_name=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    dst_path = os.path.join(log_dir, new_name)
    shutil.copytree(workspace, dst_path)

def test():
    conversation_log("./ai_review/txt/chatout1_0","./ai_review/log","chatout1_0")
    write_log("666")
#test()


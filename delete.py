import os

def delete_files(dir_path):
  """递归删除指定目录下的所有文件"""
  for root, dirs, files in os.walk(dir_path):
      for file in files:
          os.remove(os.path.join(root, file))

# 要删除的目录
dir_path = "./agentlog"
delete_files(dir_path)

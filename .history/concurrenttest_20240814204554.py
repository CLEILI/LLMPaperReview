import sys
import time
import contextlib
from concurrent.futures import ProcessPoolExecutor
from setenvrion import FirstNum,ComputeNum,TotalNum,FinalNum
def a():
    for i in range(5):
        print(f"Function a is working: {i}")
        time.sleep(1)

def b(output_file):
    with open(output_file, 'w') as f:
        with contextlib.redirect_stdout(f):
            a()  # 调用 a 函数，输出会被重定向到文件

def main():
    print(FirstNum)
    print(TotalNum)
    print(FinalNum)

if __name__ == "__main__":
    main()

import subprocess
import time
import os

def main():
    os.system("./encoder 23 1 &")

    for i in range(10):
        print(i)
        time.sleep(1)

main()
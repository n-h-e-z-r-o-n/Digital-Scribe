import time
from multiprocessing import Process

def f(name):
    time.sleep(4)
    print('hello', name)

if __name__ == '__main__':
    Process(target=f, args=('bob',)).start()
    print("hezron")
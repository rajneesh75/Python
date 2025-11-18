from multiprocessing import Process
from time import sleep


def task1():
    for i in range(5):
        print("task1 " + str(i))
        sleep(0.5)


def task2():
    for i in range(5):
        print("task2 " + str(i))
        sleep(0.5)


if __name__ == '__main__':
    p1 = Process(target=task1)
    p2 = Process(target=task2)
    p1.start()
    p2.start()
    print("hello")
    p1.join()
    p2.join()
    print("Both processes completed!")

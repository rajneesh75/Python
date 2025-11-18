import threading


def task():
    print("Task running...")


t1 = threading.Thread(target=task)
t1.start()
print("hello")
t1.join()

import threading


def count():
    for i in range(10):
        print("thread")


threads = [threading.Thread(target=count) for _ in range(4)]
for t in threads: t.start()
print("hello")
for t in threads: t.join()

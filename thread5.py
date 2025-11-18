import threading

shared_counter = 0


def increment():
    global shared_counter
    for _ in range(1000):
        with lock:  # Ensures only one thread modifies the counter at a time
            shared_counter += 1
    print(shared_counter)


t1 = threading.Thread(target=increment)
lock = threading.Lock()
t2 = threading.Thread(target=increment)
t2.start()
print("t2")
t1.start()
print("t1")

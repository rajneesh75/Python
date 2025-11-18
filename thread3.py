import threading
import time


def task1():
    for i in range(5):
        print(f"Task 1 → Step {i + 1}")
        time.sleep(1)  # simulate some work


def task2():
    for i in range(5):
        print(f"Task 2 → Step {i + 1}")
        time.sleep(1)  # simulate some work


if __name__ == '__main__':
    # Create threads
    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)

    # Start threads
    t1.start()
    t2.start()

    # Wait for both threads to complete
    t1.join()
    t2.join()

    print("✅ Both tasks completed!")

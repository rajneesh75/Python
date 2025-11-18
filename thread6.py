from concurrent.futures import ThreadPoolExecutor


def task(n):
    print(f"Processing {n}")


with ThreadPoolExecutor(max_workers=3) as executor:
    for i in range(5):
        executor.submit(task, i)

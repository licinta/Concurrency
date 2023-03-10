import threading
from threading import Thread

count = 0
count_lock = threading.Lock()
print_lock = threading.Lock()


def safe_print(*s):
    global print_lock
    print_lock.acquire()
    print(*s)
    print_lock.release()


def add(x):
    global count, count_lock
    count_lock.acquire()
    count += x
    count_lock.release()


def f(thread):
    for i in range(10):
        bef = count
        add(i)
        safe_print(f"[{thread}:{i}]".ljust(10), f"{bef}+{i}={count}".ljust(20))


a = Thread(target=f, args=("Chen",))
b = Thread(target=f, args=("Xu",))

a.start()
b.start()

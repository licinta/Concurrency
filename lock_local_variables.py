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
    count += x


def f(thread):
    for i in range(10):
        bef = count
        count_lock.acquire()
        add(i)
        count_lock.release()
        safe_print(f"[{thread}:{i}]".ljust(10), f"{bef}+{i}={count}".ljust(20))


a = Thread(target=f, args=("Chen",))
b = Thread(target=f, args=("Xu",))

a.start()
b.start()

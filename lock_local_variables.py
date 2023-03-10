import threading
from threading import Thread

count = 0


def add(x):
    threading.Lock().locked()
    count += x
    threading.Lock().release()


def f(thread):
    for i in range(10):
        add(i)
        print(f"[{thread}:i={i}] after adding {i} , current count value is {count}!")


a = Thread(target=f, args=("Chen",))
b = Thread(target=f, args=("Xu",))

a.start()
b.start()

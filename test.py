import threading
from threading import Thread
import collections
import queue
import time


class mylist(list):
    def __str__(self):
        rt = ""
        rt += "["
        for i in self:
            rt += str(i).rjust(5)
        rt += "]"
        return rt


print_lock = threading.Lock()
n = 10
pin, pout = 0, 0
full, empty = 0, n
needed = 20
needed_lock = threading.Lock()
pool_lock = threading.Lock()
full_lock = threading.Lock()
empty_lock = threading.Lock()
pool = mylist([-1 for i in range(n)])


def safe_print(*x):
    print_lock.acquire()
    print(*x)
    print_lock.release()


def produce():
    global empty, empty_lock, pool, pool_lock, full, full_lock, pin, pout, needed
    full_lock.acquire()
    empty_lock.acquire()
    if full == n or pool[pin] != -1:
        full_lock.release()
        empty_lock.release()
        return -1

    full += 1
    empty -= 1
    pool[pin] = pin
    pin = (pin+1) % n
    full_lock.release()
    empty_lock.release()
    return 0


def costum():
    global empty, empty_lock, pool, pool_lock, full, full_lock, pin, pout, needed
    empty_lock.acquire()
    full_lock.acquire()
    good = pool[pout]
    if good == -1 or empty == n:
        empty_lock.release()
        full_lock.release()
        pout = (pout+1) % n
        return 0
    else:
        full -= 1
        empty += 1
        needed_lock.acquire()
        needed -= 1
        needed_lock.release()
        pool[pout] = -1
        pout = (pout+1) % n
        empty_lock.release()
        full_lock.release()
        return 1


def chen():
    global needed, pool_lock, needed_lock
    while needed:
        pool_lock.acquire()
        produce()
        pool_lock.release()
        time.sleep(0.1)


def xu():
    global needed, pool_lock, needed_lock
    while needed:
        pool_lock.acquire()
        costum()
        pool_lock.release()
        time.sleep(0.1)



Thread(target=chen, args=()).start()
Thread(target=xu, args=()).start()

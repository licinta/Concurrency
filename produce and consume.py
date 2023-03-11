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
    if full == n:
        return

    full_lock.acquire()
    empty_lock.acquire()
    full += 1
    empty -= 1
    pool_lock.acquire()
    pool[pin] = pin
    safe_print(f"[needed={needed},full={full},empty={empty}] produce a good {pin}".ljust(
        60), f"pool = {pool}")
    pin = (pin+1) % n
    pool_lock.release()
    full_lock.release()
    empty_lock.release()


def costum():
    global empty, empty_lock, pool, pool_lock, full, full_lock, pin, pout, needed
    if empty == 0:
        return
    empty_lock.acquire()
    full_lock.acquire()
    pool_lock.acquire()
    good = pool[pout]
    if good == -1:
        safe_print(
            f"[needed={needed},full={full},empty={empty}] {pout} hasn't been produced")
    else:
        full -= 1
        empty += 1
        needed_lock.acquire()
        needed -= 1
        needed_lock.release()
        safe_print(f"[needed={needed},full={full},empty={empty}] custom a good {good}".ljust(
            60), f"pool = {pool}")
        pool[pout] = -1
    pout += 1
    pout %= n
    pool_lock.release()
    empty_lock.release()
    full_lock.release()


def chen():
    global needed
    while needed:
        produce()
        time.sleep(0.1)


def xu():
    global needed
    while needed:
        costum()
        time.sleep(0.1)


Thread(target=chen, args=()).start()
Thread(target=xu, args=()).start()

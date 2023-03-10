import threading
from threading import Thread
n = 10
cache = [0 for i in range(n)]


def say_hello(x):
    print(f"hello, {x}!")


def say_bye(x):
    print(f"goodbye, {x}!")


def loop(func, args, times):
    for i in range(times):
        func(args)

    print(f"function {func} ends.")


a = Thread(target=loop, args=(say_hello, "Chen", 10))
b = Thread(target=loop, args=(say_bye, "Xu", 10))

a.start()
b.start()

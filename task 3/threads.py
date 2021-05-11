from threading import Thread
import threading

a = 0
lock = threading.Lock()

def function(arg):
    global a
    with lock:
        for _ in range(arg):
            a += 1


def main():
    threads = []
    
    for _ in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(a)


main()
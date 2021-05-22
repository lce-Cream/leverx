import threading
from concurrent.futures import ThreadPoolExecutor
# for some reason I can't figure out how to pass my argument
# in a thread by reference, neither dict or list work


class Argument:
    lock = threading.Lock()

    def __init__(self, value=0, count=1000000):
        self.value = value
        self.count = count


def function(arg):
    for _ in range(arg.count):
        with arg.lock:
            arg.value += 1
    return arg.value


def main():
    arg = Argument()

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(function, arg) for _ in range(5)]

    print('values at the end of every thread:', [res.result() for res in results])
    print('result:', arg.value)


main()

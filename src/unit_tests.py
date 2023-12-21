from os import remove as os_remove
from os.path import isfile as os_isfile
from typing import Callable
from DBConnection import DBConnect


class Testing:
    tests = []

    @classmethod
    def add_test(cls, func: Callable[[], bool]):
        cls.tests.append(func)
        return func

    @staticmethod
    def try_except[T](func: Callable[[], T]) -> T | Exception:
        try:
            return func()
        except Exception as E:
            return E

    @classmethod
    def run(cls):
        answ = ("-", "+", "!")
        for func in cls.tests:
            res = Testing.try_except(func)
            postfix = ""
            if isinstance(res, Exception):
                postfix, res = f": {res}", 2

            print(f"[{answ[res]}] {func.__name__} {postfix}")


if __name__ == "__main__":
    Testing.run()

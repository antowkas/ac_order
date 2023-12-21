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
            
@Testing.add_test
def adding_test():
    db = DBConnect("_test.db")

    res = db.show_category() + db.show_order() + db.show_product() + db.show_fabricator()

    return ['Макаронные изделия', 'Молочные изделия', 'Кондитерские изделия', 'Полуфабрикаты',
            (1, 'Улица Пушника, Дом колотушкина', '25.11.2023'), (2, 'Алькатрасс', '26.11.2023'),
            (3, 'Богородское', '13.12.2023'), (9, 'Тимирязева 23', '14.12.2023'), (10, 'Тимирязева 23', '14.12.2023'),
            (11, 'Аскабар', '14.12.2023'), ('Макаронные изделия', 'Barilla', 'Макароны Барилла'),
            ('Макаронные изделия', 'MAKFA', 'Макароны Макфа'), ('Молочные изделия', 'Весёлый молочник', 'Сливки'),
            ('Кондитерские изделия', 'Milka', 'Мятный шоколад Milka'), 'MAKFA', 'Barilla', 'Весёлый молочник',
            'Milka'] == res

if __name__ == "__main__":
    Testing.run()

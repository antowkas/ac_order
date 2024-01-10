# Удаляет файл
from os import remove as os_remove
# проверка существует ли файл
from os.path import isfile as os_isfile
# Украшательство для PyCharm
from typing import Callable
# Наше подключение к дб, которое мы тестируем юнит-тестами
from DBConnection import DBConnect


class Testing:
    # тесты
    tests = []

    # Декоратор, который добавляет тест
    @classmethod
    def add_test(cls, func: Callable[[], bool]):
        # добавление теста в переменнтую тестов
        cls.tests.append(func)
        return func

    @staticmethod
    def try_except[T](func: Callable[[], T]) -> T | Exception:
        # Отлов ошибок
        try:
            # Возвращение ответа функции
            return func()
        except Exception as E:
            # Возвращение ошибки
            return E

    # Проверка всех тестов
    @classmethod
    def run(cls):
        # Возможные символы
        answ = ("-", "+", "!")
        for func in cls.tests:
            # Получаем результат теста
            res = Testing.try_except(func)
            # То, что мы пишем в самом конце
            postfix = ""
            # Если ответ это ошибка, то
            if isinstance(res, Exception):
                # В постфикс записываем эту ошибку
                postfix, res = f": {res}", 2
            # Выводим в терминал ответ теста
            print(f"[{answ[res]}] {func.__name__} {postfix}")


@Testing.add_test
def criteria_test():
    # Подключение к тестовой базе данных
    db = DBConnect("_test.db")

    # Выполенение запроса на выборку с фильтром
    res = db.search_by_criteria("1", "Макароны Барилла", "4", "Barilla", "Макаронные изделия")

    # Возвращение True или False в зависимости от резульатта теста
    return [(1, 'Улица Пушника, Дом колотушкина', '25.11.2023',
             'Макароны Барилла', 4, 'Barilla', 'Макаронные изделия')] == res


@Testing.add_test
def view_test():
    # Подключаемся к тестовой базе данных
    db = DBConnect("_test.db")

    # Складываем ответы запросов
    res = db.show_category() + db.show_order() + db.show_product() + db.show_fabricator()

    # Проверяем равны ли ответы сложенным запросам
    return ['Макаронные изделия', 'Молочные изделия', 'Кондитерские изделия', 'Полуфабрикаты',
            (1, 'Улица Пушника, Дом колотушкина', '25.11.2023'), (2, 'Алькатрасс', '26.11.2023'),
            (3, 'Богородское', '13.12.2023'), (9, 'Тимирязева 23', '14.12.2023'), (10, 'Тимирязева 23', '14.12.2023'),
            (11, 'Аскабар', '14.12.2023'), ('Макаронные изделия', 'Barilla', 'Макароны Барилла'),
            ('Макаронные изделия', 'MAKFA', 'Макароны Макфа'), ('Молочные изделия', 'Весёлый молочник', 'Сливки'),
            ('Кондитерские изделия', 'Milka', 'Мятный шоколад Milka'), 'MAKFA', 'Barilla', 'Весёлый молочник',
            'Milka'] == res


@Testing.add_test
def adding_test():
    # Проверяем не существует ли такой бд, если существует удаляем
    if os_isfile("adding_test.db"):
        os_remove("adding_test.db")

    # Подключаемся к бд
    db = DBConnect("adding_test.db")

    # Вставляем в категории категорию "category"
    db.insert_category("category")

    # Вставляем в производителей производителя "fabricator"
    db.insert_fabricator("fabricator")

    # Дальше по аналогии
    order_id = db.insert_order("address", "01.01.2023")
    db.insert_product("category", "fabricator", "product")
    db.insert_journal(order_id, "product", 1)
    db.create_order("address2", "02.01.2023", [("product", 1)])

    # Выполняем запрос
    res = db.execute("""
        SELECT *
        FROM `Journal`
        JOIN `Order` ON `Journal`.`order_id` = `Order`.`order_id`
        JOIN `Product` ON `Journal`.`product_id` = `Product`.`product_id`
        JOIN `Category` ON `Product`.`category_id` = `Category`.`category_id`
        JOIN `Fabricator` ON `Product`.`fabricator_id` = `Fabricator`.`fabricator_id`;""")

    # Проверяем равнен ли ответ запроса эталонному ответу
    return [(1, 1, 1, 1, 1, 'address', '01.01.2023', 1, 1, 1, 'product', 1, 'category', 1, 'fabricator'),
            (2, 2, 1, 1, 2, 'address2', '02.01.2023', 1, 1, 1, 'product', 1, 'category', 1, 'fabricator')] == res


# Если файл является исполнимым, то запускаем тестирование
if __name__ == "__main__":
    Testing.run()

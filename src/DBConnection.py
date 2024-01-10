# Для работы с бд
import sqlite3
# Проверка существования файла
from os.path import isfile
# Визуальный класс для PyCharm чтобы он предупреждал об ошибках во время программирования
from sqlite3.dbapi2 import Cursor
# Для проверки строки
from re import match as re_match


class DBConnect:
    # Путь до файла
    path_db: str
    # Включён ли дебаг
    debug: bool

    # Метод инициализации (создание объекта подключения)
    def __init__(self, path_db: str, debug=False):
        self.path_db = path_db
        self.debug = debug
        if not isfile(path_db):
            self.execute_script_from_file("sql/create_db.sql")

    @staticmethod
    def cursor_decorator(func):
        """
        Это чтобы долго и нудно каждый раз не открывать и не закрывать подключение к DB
        """

        def wrapper(self, *args, **kwargs):
            # Создание подключения к бд
            con = sqlite3.connect(self.path_db)
            # Создание курсора
            cur = con.cursor()
            # Отлов ошибок
            try:
                # Вызов декорируемой функции и запоминание результата
                res = func(self, *args, cur=cur, **kwargs)
                con.commit()
            except Exception as E:
                # Аккуратно закрываем бд
                # Выключаем курсор
                cur.close()
                # Закрываем подключение
                con.close()
                print("Connection closed")
                # Вызов ошибки
                raise E
            # Закрываем бд
            cur.close()
            con.close()
            # Возвращение результата
            return res

        return wrapper

    def execute_script_from_file(self, path: str) -> None:
        # Вызов метода для выполнения скрипта, но в качестве аргумента открываем и читаем файлик по переданному пути
        self.execute_script(open(path, encoding="UTF-8").read())

    @cursor_decorator
    def execute_script(self, script: str, cur: Cursor) -> None:
        # Если дебаг включён, то мы пишем скрипт в консоль
        if self.debug:
            print(script)
        cur.executescript(script)

    def execute_from_file(self, path: str) -> list:
        # Вызывает одиночный запрос к бд по пути файла
        return self.execute(open(path, encoding="UTF-8").read())

    @cursor_decorator
    def execute(self, request: str, cur: Cursor) -> list:
        # Если дебаг включён, то мы пишем скрипт в консоль
        if self.debug:
            print(request)
        # Вызывает одиночный запрос к бд
        return cur.execute(request).fetchall()

    # Проверка строки
    @staticmethod
    def test_string(string: str) -> bool:
        """
        True - хорошая строка
        False - плохая строка
        """
        pattern = r'^[^;\'"\\]*$'
        return bool(re_match(pattern, string))

    # Вставска в бд
    def insert(self, table: str, values_list, columns_name: tuple = None) -> None:
        # Если строка не проходит тестирование, то ошибка
        if not self.test_string(table):
            raise ValueError("Bad table name:", table)

        # Начало запроса
        request = f"INSERT INTO \"{table}\" "
        # Проверка вставлять в определённые столбцы или нет
        if columns_name is not None:
            request += f"({', '.join(columns_name)}) "
        # продолжение запроса
        request += "VALUES ("
        # repr - закрывает в кавычки строки, а числа нет
        request += ', '.join(map(repr, values_list)) + ')'
        # Вызов созданного запроса
        self.execute(request)

    # Поиск в журнале по критериям
    def search_by_criteria(self, order_id="", product_name="", quantity="", fabricator_name="", category_name=""):
        # Каждый аргумент тестируем, если не проходит - ошибка
        if not self.test_string(order_id):
            raise ValueError("Bad order_id:", order_id)
        if not self.test_string(product_name):
            raise ValueError("Bad product_name:", product_name)
        if not self.test_string(quantity):
            raise ValueError("Bad quantity:", quantity)
        if not self.test_string(fabricator_name):
            raise ValueError("Bad fabricator_name:", fabricator_name)
        if not self.test_string(category_name):
            raise ValueError("Bad category_name:", category_name)
        with open("sql/TermCriteriaF.sql") as file:
            script = file.read()
        # Вставляем в прочитанный скрипт из файла наши проверенные аргументы
        script = script.format(order_id, product_name, quantity, fabricator_name, category_name)
        # Выполняем запрос и возвращаем ответ
        return self.execute(script)

    def show_category(self):
        # Возвращаем все названия категорий
        return [el[0] for el in self.execute("SELECT category_name FROM Category")]

    def show_order(self):
        # Возвращаем нужные колонки из таблицы Order
        return [el for el in self.execute("SELECT order_id, order_address, order_date FROM \"Order\"")]

    def show_product(self):
        #
        return [el for el in
                self.execute("SELECT Category.category_name, Fabricator.fabricator_name,"
                             "       Product.product_name "
                             "FROM Product "
                             "JOIN Category ON Product.category_id = Category.category_id "
                             "JOIN Fabricator ON Product.fabricator_id = Fabricator.fabricator_id")]

    def show_fabricator(self):
        # Показать производителя
        return [el[0] for el in self.execute("SELECT fabricator_name FROM Fabricator")]

    def insert_category(self, category_name):
        # Тестируем аргумент, если не проходит - ошибка
        if not self.test_string(category_name):
            raise ValueError("Bad category name:", category_name)
        # Вставляем значение в таблицу категория без возвращения
        self.insert("Category", [category_name], ("category_name",))

    def insert_fabricator(self, fabricator_name):
        # Тестируем аргумент, если не проходит - ошибка
        if not self.test_string(fabricator_name):
            raise ValueError("Bad fabricator name:", fabricator_name)
        # Вставляем значение в таблицу фабрикатор без возвращения
        self.insert("Fabricator", [fabricator_name], ("fabricator_name",))

    def insert_product(self, category_name, fabricator_name, product_name):
        # Тестируем аргументы, если не проходит - ошибка
        if not self.test_string(category_name):
            raise ValueError("Bad category name:", category_name)
        if not self.test_string(fabricator_name):
            raise ValueError("Bad fabricator name:", fabricator_name)
        if not self.test_string(product_name):
            raise ValueError("Bad product name:", product_name)

        # Существует ли такая категория?
        if category_id := self.execute(f"SELECT category_id FROM Category WHERE category_name = \"{category_name}\""):
            category_id = category_id[0][0]
        else:
            raise ValueError("Not find category name in DB: ", category_name)

        # Существует ли такой производитель?
        if fabricator_id := self.execute(
                f"SELECT fabricator_id FROM Fabricator WHERE fabricator_name = \"{fabricator_name}\""):
            fabricator_id = fabricator_id[0][0]
        else:
            raise ValueError("Not find fabricator name in DB: ", fabricator_name)

        # Вставляем значение в таблицу фабрикатор без возвращения
        self.insert("Product", [category_id, fabricator_id, product_name],
                    ("category_id", "fabricator_id", "product_name"))

    def insert_order(self, address: str, date: str):
        # Тестируем аргументы, если не проходит - ошибка
        if not self.test_string(address):
            raise ValueError("Bad address name:", address)
        if not self.test_string(date):
            raise ValueError("Bad date:", date)
        self.insert("Order", [address, date],
                    ("order_address", "order_date"))

        # Вставка с возвращением id строки
        return self.execute('SELECT max("Order"."order_id") FROM "Order"')[0][0]

    def insert_journal(self, order_id: int, product_name: str, quantity: int | str):
        # Проверка типа данных
        if isinstance(quantity, str):
            # Если у нас quantity записан строкой, но фактически число ("123" - > 123)
            if quantity.isdigit():
                quantity = int(quantity)
            else:
                # Если строка не число ("123g55jr87io")
                raise ValueError(f"Bad quantity: {quantity}")
        # тестррование аргументов
        if not self.test_string(product_name):
            raise ValueError("Bad product name:", product_name)
        # Есть ли в нашей бд введёный продукт, если нет - ошибка
        if product_id := self.execute(f"SELECT product_id FROM Product WHERE product_name = \"{product_name}\""):
            product_id = product_id[0][0]
        else:
            raise ValueError("Not find product name in DB: ", product_name)

        # Существует ли заказ с таким номером
        if not self.execute(f"SELECT order_id FROM \"Order\" WHERE order_id = {order_id}"):
            raise ValueError("Not find order_id name in DB: ", order_id)
        # Вставляем в журнал наши покупки
        self.insert("Journal", [order_id, product_id, quantity],
                    ("order_id", "product_id", "quantity"))

    # Добаление в журнал наших покупок
    def create_order(self, address: str, date: str, products_quantity: list):
        # Получаем номер покупки
        order_id = self.insert_order(address, date)
        # Вызываем метод insert_journal для каждого товара
        for product, quantity in products_quantity:
            self.insert_journal(order_id, product, quantity)


if __name__ == '__main__':
    db = DBConnect("test.db")
    # db.create_order("Богородское", "13.12.2023", [["Макароны Барилла", 2], ["Сливки", 15]])

    # db.insert_journal(1000, "Макароны Барилла", 1)
    # print(db.insert_order("123", "123"))
    # print(db.search_by_criteria(product_name="Макароны Барилла"))
    print(db.show_order())
    # print(db.execute("""
    #     SELECT *
    #     FROM `Journal`
    #     JOIN `Order` ON `Journal`.`order_id` = `Order`.`order_id`
    #     JOIN `Product` ON `Journal`.`product_id` = `Product`.`product_id`
    #     JOIN `Category` ON `Product`.`category_id` = `Category`.`category_id`
    #     JOIN `Fabricator` ON `Product`.`fabricator_id` = `Fabricator`.`fabricator_id`;"""))

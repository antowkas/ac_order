import sqlite3
from os.path import isfile
from sqlite3.dbapi2 import Cursor
from re import match as re_match


class DBConnect:
    path_db: str

    def __init__(self, path_db: str):
        self.path_db = path_db
        if not isfile(path_db):
            self.execute_script_from_file("sql/create_db.sql")

    @staticmethod
    def cursor_decorator(func):
        """
        Это чтобы долго и нудно каждый раз не открывать и не закрывать подключение к DB
        """

        def wrapper(self, *args, **kwargs):
            con = sqlite3.connect(self.path_db)
            cur = con.cursor()
            try:
                res = func(self, *args, cur=cur, **kwargs)
                con.commit()
            except Exception as E:
                cur.close()
                con.close()
                print("Connection closed")
                raise E
            cur.close()
            con.close()
            return res

        return wrapper

    def execute_script_from_file(self, path: str) -> None:
        self.execute_script(open(path, encoding="UTF-8").read())

    @cursor_decorator
    def execute_script(self, script: str, cur: Cursor) -> None:
        cur.executescript(script)

    def execute_from_file(self, path: str) -> list:
        return self.execute(open(path, encoding="UTF-8").read())

    @cursor_decorator
    def execute(self, request: str, cur: Cursor) -> list:
        return cur.execute(request).fetchall()

    @staticmethod
    def test_string(string) -> bool:
        """
        True - хорошая строка
        False - плохая строка
        """
        pattern = r'^[^;\'"\\]*$'
        return bool(re_match(pattern, string))

    def insert(self, table: str, values_list: list[tuple], columns_name: tuple = None) -> None:
        if not self.test_string(table):
            raise ValueError("Bad table name:", table)
        request = f"INSERT INTO {table} "
        if columns_name is not None:
            request += f"({', '.join(columns_name)}) "
        request += "VALUES "
        # for values in values_list:
        #     for value in values:
        #         if isinstance(value, str) and not self.test_string(value):
        #             raise ValueError("Bad value:", value)
        request += ', '.join(map(repr, values_list))
        self.execute(request)

    def search_by_criteria(self, order_id="", product_name="", quantity="", fabricator_name="", category_name=""):
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
        product_name.lower()
        with open("sql/TermCriteriaF.sql") as file:
            script = file.read()
        script = script.format(order_id, product_name, quantity, fabricator_name, category_name)
        return self.execute(script)



if __name__ == '__main__':
    db = DBConnect("test.db")
    print(db.search_by_criteria(product_name="Макароны Барилла"))
    # print(db.execute("""
    #     SELECT *
    #     FROM `Journal`
    #     JOIN `Order` ON `Journal`.`order_id` = `Order`.`order_id`
    #     JOIN `Product` ON `Journal`.`product_id` = `Product`.`product_id`
    #     JOIN `Category` ON `Product`.`category_id` = `Category`.`category_id`
    #     JOIN `Fabricator` ON `Product`.`fabricator_id` = `Fabricator`.`fabricator_id`;"""))

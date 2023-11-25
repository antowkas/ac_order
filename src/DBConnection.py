import sqlite3
from os.path import isfile
from sqlite3.dbapi2 import Cursor


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
            except Exception as E:
                cur.close()
                con.close()
                raise E
            cur.close()
            con.close()
            print("Connection closed")
            return res
        return wrapper

    def execute_script_from_file(self, path: str) -> None:
        self.execute_script(open(path, encoding="UTF-8").read())

    @cursor_decorator
    def execute_script(self, script: str, cur: Cursor):
        cur.executescript(script)

    @cursor_decorator
    def execute(self, response: str, cur: Cursor) -> list:
        return cur.execute(response).fetchall()


if __name__ == '__main__':
    db = DBConnect("test.db")
    print(db.execute("""
        SELECT *
        FROM `Journal`
        JOIN `Order` ON `Journal`.`order_id` = `Order`.`order_id`
        JOIN `Product` ON `Journal`.`product_id` = `Product`.`product_id`
        JOIN `Category` ON `Product`.`category_id` = `Category`.`category_id`
        JOIN `Fabricator` ON `Product`.`fabricator_id` = `Fabricator`.`fabricator_id`;"""))

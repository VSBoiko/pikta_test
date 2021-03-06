import sqlite3


class PiktaDb:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = None

    def init_db(self, add_data: bool = False):
        """
        Создает базу данныx и добавляет в нее таблицы

        :param add_data: заполнить или нет таблицы данными
        """
        self.__connection_open()
        self.__add_tables()
        if add_data:
            self.__add_data()
        self.__connection_close()

    def get_clients_amount(self) -> list:
        """
        Возвращает список клиентов с общей суммой их покупки

        :return: список клиентов с общей суммой их покупки
        Например:
        [
            {
                "client_name": "Иван",
                "amount": 100.10
            },
            {
                "client_name": "Петр",
                "amount": 200.00
            },
        ]
        """
        self.__connection_open()
        cur = self.db.cursor()
        select_sql = """SELECT
            cl.client_name AS client_name,
            SUM(pr.product_price) AS amount
        FROM clients cl
            JOIN orders ord ON cl.client_id = ord.client_id
            JOIN products pr ON ord.product_id = pr.product_id
        group by client_name
        """
        cur.execute(select_sql)
        results_sql = cur.fetchall()
        result = []
        for row in results_sql:
            result.append({
                "client_name": row["client_name"],
                "amount": round(row["amount"], 2)
            })
        self.__connection_close()

        return result

    def get_who_bought_phone(self) -> list:
        """
        Возвращает список клиентов, которые купили телефон

        :return: список клиентов, которые купили телефон
        Например:
        [
            {
                "client_name": "Иван",
            },
            {
                "client_name": "Петр",
            },
        ]
        """
        self.__connection_open()
        cur = self.db.cursor()
        select_sql = """SELECT
            cl.client_name AS client_name
        FROM clients cl
            JOIN orders ord ON cl.client_id = ord.client_id
            JOIN products pr ON ord.product_id = pr.product_id
        WHERE pr.product_name = 'Телефон'
        """
        cur.execute(select_sql)
        results_sql = cur.fetchall()
        result = []
        for row in results_sql:
            result.append({
                "client_name": row["client_name"],
            })
        self.__connection_close()

        return result

    def get_products_order_quantity(self) -> list:
        """
        Возвращает список товаров с количеством их заказа

        :return: список товаров с количеством их заказа
        Например:
        [
            {
                "product_name": "Ручка",
                "orders_count": 10,
            },
            {
                "client_name": "Книжка",
                "orders_count": 7,
            },
        ]
        """
        self.__connection_open()
        cur = self.db.cursor()
        select_sql = """SELECT
            pr.product_name AS product_name,
            COUNT(ord.product_id) AS orders_count
        FROM orders ord
            JOIN products pr ON ord.product_id = pr.product_id
        GROUP BY product_name
        """
        cur.execute(select_sql)
        results_sql = cur.fetchall()
        result = []
        for row in results_sql:
            result.append({
                "product_name": row["product_name"],
                "orders_count": row["orders_count"]
            })
        self.__connection_close()

        return result

    def __add_data(self):
        clients = [
            {"name": "Иван"},
            {"name": "Константин"},
            {"name": "Дмитрий"},
            {"name": "Александр"}
        ]
        products = [
            {"name": "Мяч", "price": 299.99},
            {"name": "Ручка", "price": 18},
            {"name": "Кружка", "price": 159.87},
            {"name": "Монитор", "price": 18000},
            {"name": "Телефон", "price": 9999.9},
            {"name": "Кофе", "price": 159},
        ]
        orders = [
            {"client_id": 2, "product_id": 2, "name": "Закупка 1"},
            {"client_id": 2, "product_id": 5, "name": "Закупка 2"},
            {"client_id": 2, "product_id": 1, "name": "Закупка 3"},
            {"client_id": 1, "product_id": 1, "name": "Закупка 4"},
            {"client_id": 1, "product_id": 3, "name": "Закупка 5"},
            {"client_id": 1, "product_id": 6, "name": "Закупка 6"},
            {"client_id": 1, "product_id": 2, "name": "Закупка 7"},
            {"client_id": 4, "product_id": 5, "name": "Закупка 8"},
            {"client_id": 3, "product_id": 6, "name": "Закупка 9"},
            {"client_id": 3, "product_id": 3, "name": "Закупка 10"},
            {"client_id": 1, "product_id": 5, "name": "Закупка 11"}
        ]

        try:
            for client in clients:
                self.__create_client(**client)

            for product in products:
                self.__create_product(**product)

            for order in orders:
                self.__create_order(**order)

            self.db.commit()
        except:
            self.db.rollback()
            raise RuntimeError("An error occurred.")

    def __add_tables(self):
        try:
            self.__create_table_clients()
            self.__create_table_products()
            self.__create_table_orders()
            self.db.commit()
        except:
            self.db.rollback()
            raise RuntimeError("An error occurred.")

    def __connection_close(self):
        self.db.close()

    def __connection_open(self):
        db = sqlite3.connect(self.db_path)
        db.row_factory = sqlite3.Row
        self.__set_db(db)

    def __create_table_clients(self):
        cur = self.db.cursor()
        create_table_sql = """CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL
        )"""
        cur.execute(create_table_sql)

    def __create_table_orders(self):
        cur = self.db.cursor()
        create_table_sql = """CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            order_name TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (client_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )"""
        cur.execute(create_table_sql)

    def __create_table_products(self):
        cur = self.db.cursor()
        create_table_sql = """CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL
        )"""
        cur.execute(create_table_sql)

    def __create_client(self, name):
        insert_sql = "INSERT INTO clients (client_name) VALUES (?)"
        cur = self.db.cursor()
        cur.execute(insert_sql, (name,))
        return cur.lastrowid

    def __create_order(self, client_id, product_id, name):
        insert_sql = """INSERT INTO orders 
            (client_id, product_id, order_name) 
            VALUES (?, ?, ?)"""
        cur = self.db.cursor()
        cur.execute(insert_sql, (client_id, product_id, name))
        return cur.lastrowid

    def __create_product(self, name, price):
        insert_sql = "INSERT INTO products (product_name, product_price) VALUES (?, ?)"
        cur = self.db.cursor()
        cur.execute(insert_sql, (name, price))
        return cur.lastrowid

    def __get_db(self):
        if self.db is None:
            self.init_db()
        return self.db

    def __set_db(self, db):
        self.db = db

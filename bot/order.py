# @Description : Structures for keeping orders from users.

import sqlite3

DEFAULT_DB_PATH = "/tmp/preo-bot.db"

class OrderQuery:
    INIT_SCHEMA = """
            CREATE TABLE IF NOT EXISTS orders (
            room_id  CHAR(128) NOT NULL,
			user_id CHAR(128) NOT NULL,
			item_name VARCHAR(255) NOT NULL,
			amount INT NOT NULL,
			CONSTRAINT PK_Order PRIMARY KEY (room_id, user_id, item_name));
            """

    SET_ORDER = """
        INSERT OR REPLACE INTO orders (room_id, user_id, item_name, amount)
        VALUES (?,?,?,?)"""

    DEL_ORDER = "DELETE FROM orders WHERE room_id = ? and user_id = ? and item_name = ?"

    SELECT_ALL_ORDER = "SELECT * FROM orders"
    SELECT_ORDER_BY_ROOM = "SELECT * FROM orders WHERE room_id = ?"
    SELECT_ORDER_BY_USER = "SELECT * FROM orders WHERE room_id = ? and user_id = ?"
    SELECT_ORDER_BY_ITEM = "SELECT *, count(amount) FROM orders WHERE room_id = ? and item_name = ?"

class Order:
    "Order model for managing orders table"

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db = sqlite3.connect(db_path)
        self.__create_schema()

    def __create_schema(self):
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.INIT_SCHEMA)
        self.db.commit()

    def set_order(self, room_id, user_id, item_name, amount):
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SET_ORDER, [room_id, user_id, item_name, amount])
        self.db.commit()

    def del_order(self, room_id, user_id, item_name):
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.DEL_ORDER, [room_id, user_id, item_name])
        self.db.commit()

    def list_all(self):
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ALL_ORDER)
        rows = cursor.fetchall()
        return rows

    def get_room_order(self, room_id):
        pass

    def get_user_order(self, room_id, user_id):
        pass

    def get_item_order(self, room_id, item_name):
        pass

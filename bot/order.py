# @Description : Structures for keeping orders from users.

class OrderQuery:
    "SQL Queries for Order class"
    INIT_ROOM_SCHEMA = """
            CREATE TABLE IF NOT EXISTS rooms (
            room_id  CHAR(128) NOT NULL,
			is_enable INT NOT NULL CHECK(is_enable == 0 OR is_enable == 1),
			CONSTRAINT PK_Room PRIMARY KEY (room_id));
            """

    INIT_ITEM_SCHEMA = """
            CREATE TABLE IF NOT EXISTS orders (
            room_id  CHAR(128) NOT NULL,
			user_name CHAR(128) NOT NULL,
			item_name VARCHAR(255) NOT NULL,
			amount INT NOT NULL CHECK(amount > 0),
			CONSTRAINT PK_Order PRIMARY KEY (room_id, user_name, item_name));
            """

    NEW_ROOM_STATUS = "INSERT INTO rooms (room_id, is_enable) VALUES (?, 1)"
    SET_ROOM_ENABLE = "REPLACE INTO rooms (room_id, is_enable) VALUES (?, 1)"
    SET_ROOM_DISABLE = "REPLACE INTO rooms (room_id, is_enable) VALUES (?, 0)"
    SELECT_ROOM_STATUS = "SELECT room_id, is_enable FROM rooms WHERE room_id = ?"
    DEL_ROOM_STATUS = "DELETE FROM rooms WHERE room_id = ?"

    SET_ORDER = """
        INSERT OR REPLACE INTO orders (room_id, user_name, item_name, amount)
        VALUES (?,?,?,?)"""

    DEL_ORDER_BY_USER = "DELETE FROM orders WHERE room_id = ? and user_name = ? and item_name = ?"
    DEL_ORDER_BY_ROOM = "DELETE FROM orders WHERE room_id = ?"

    SELECT_ALL_ORDER = "SELECT room_id, user_name, item_name, amount FROM orders"
    SELECT_ORDER_BY_ROOM = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ?"
    SELECT_ORDER_BY_USER = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ? and user_name = ?"
    SELECT_ORDER_BY_ITEM = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ? and item_name = ?"
    SELECT_ORDER_BY_USER_AND_ITEM = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ? and user_name = ? and item_name = ?"

class RoomStatus:
    "An instance for storing room status"

    def __init__(self, **kwargs):
        self.room_id = kwargs['room_id']
        self.is_enable = kwargs['is_enable']

    @classmethod
    def from_db_rows(cls, row):
        try:
            roomStatus = cls(room_id=row[0], is_enable=row[1])
        except Exception:
            raise
        return roomStatus

class OrderRow:
    "An instance for storing order row"

    def __init__(self, **kwargs):
        self.room_id = kwargs['room_id']
        self.user_name = kwargs['user_name']
        self.item_name = kwargs['item_name']
        self.amount = kwargs['amount']

    @classmethod
    def from_db_rows(cls, rows):
        orders = []
        for row in rows:
            try:
                orders.append(cls(room_id=row[0], user_name=row[1], item_name=row[2], amount=row[3]))
            except Exception:
                raise
        return orders

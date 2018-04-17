# @Description : Structures for keeping room property from users.

class RoomPropQuery:
    "SQL Queries for RoomProp class"
    INIT_SCHEMA = """
            CREATE TABLE IF NOT EXISTS room_props (
            room_id  CHAR(128) NOT NULL,
			order_name CHAR(128) NOT NULL,
			enable INT NOT NULL NOT NULL,
			CONSTRAINT PK_RoomProp PRIMARY KEY (room_id);
            """
    # TODO(M): Fix CRUD query
    SET_ORDER = """
        INSERT OR REPLACE INTO orders (room_id, user_name, item_name, amount)
        VALUES (?,?,?,?)"""

    DEL_ORDER_BY_USER = "DELETE FROM orders WHERE room_id = ? and user_name = ? and item_name = ?"
    DEL_ORDER_BY_ROOM = "DELETE FROM orders WHERE room_id = ?"

    SELECT_ALL_ORDER = "SELECT room_id, user_name, item_name, amount FROM orders"
    SELECT_ORDER_BY_ROOM = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ?"
    SELECT_ORDER_BY_USER = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ? and user_name = ?"
    SELECT_ORDER_BY_ITEM = "SELECT room_id, user_name, item_name, amount FROM orders WHERE room_id = ? and item_name = ?"


class RoomPropRow:
    "An instance for storing room property row"

    def __init__(self, **kwargs):
        self.room_id = kwargs['room_id']
        self.order_name = kwargs['order_name']
        self.enable = kwargs['enable']

    @classmethod
    def from_db_rows(cls, rows):
        room_props = []
        for row in rows:
            try:
                room_props.append(cls(room_id=row[0], order_name=row[1], enable=row[2]))
            except Exception:
                raise
        return room_props

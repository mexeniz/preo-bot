# @Description : Structures for keeping orders from users.

import sqlite3
from order import RoomStatus, OrderRow, OrderQuery
from roomprop import RoomPropRow, RoomPropQuery

class PreoDB:
    "DB Wrapper for preo-bot"
    DEFAULT_DB_PATH = "/tmp/preo-bot.db"

    def __create_schema(self):
        "Init table orders in sqlite database"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.INIT_ROOM_SCHEMA)
        cursor.execute(OrderQuery.INIT_ITEM_SCHEMA)
        # TODO(M): Init RoomProp schema
        self.db.commit()

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db = sqlite3.connect(db_path)
        self.__create_schema()

    def set_order(self, room_id, user_name, item_name, amount):
        """
        Insert an order into the table for user in chat room.
        Update the order instead if one exists.
        """
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SET_ORDER, [room_id, user_name, item_name, amount])
        self.db.commit()

    def del_order(self, room_id, user_name, item_name):
        "Delete an order from the table by user_name and item_name"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.DEL_ORDER_BY_USER, [room_id, user_name, item_name])
        self.db.commit()

    def new_room_order(self, room_id):
        "Create new room order being enable as default"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.NEW_ROOM_STATUS, [room_id])
        self.db.commit()

    def enable_room_order(self, room_id):
        "Enable room order"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SET_ROOM_ENABLE, [room_id])
        self.db.commit()

    def disable_room_order(self, room_id):
        "Disable room order"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SET_ROOM_DISABLE, [room_id])
        self.db.commit()

    def is_room_order_exist(self, room_id):
        "Check room order existence"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ROOM_STATUS, [room_id])
        row = cursor.fetchone()
        return (row != None)

    def is_room_order_enable(self, room_id):
        '''
        Check room order status
        return True if room is enabled
        return False if either room is disabled or not created
        '''
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ROOM_STATUS, [room_id])
        row = cursor.fetchone()
        if row == None:
            return False
        roomStatus = RoomStatus.from_db_rows(row)
        return (roomStatus.is_enable == 1)

    def del_room_order(self, room_id):
        "Delete room order from the table by room_id"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.DEL_ORDER_BY_ROOM, [room_id])
        cursor.execute(OrderQuery.DEL_ROOM_STATUS, [room_id])
        self.db.commit()

    def list_all(self):
        "List all orders from the table"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ALL_ORDER)
        rows = cursor.fetchall()
        return rows

    def get_room_order(self, room_id):
        "List orders by room_id"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ORDER_BY_ROOM, [room_id])
        rows = cursor.fetchall()
        return OrderRow.from_db_rows(rows)

    def get_user_order(self, room_id, user_name):
        "List orders by room_id and user_name"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ORDER_BY_USER, [room_id, user_name])
        rows = cursor.fetchall()
        return OrderRow.from_db_rows(rows)

    def get_item_order(self, room_id, item_name):
        "List orders by room_id and item_name"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ORDER_BY_ITEM, [room_id, item_name])
        rows = cursor.fetchall()
        return OrderRow.from_db_rows(rows)

    def get_user_item_order(self, room_id, user_name, item_name):
        "List orders by room_id , user_name and item_name"
        cursor = self.db.cursor()
        cursor.execute(OrderQuery.SELECT_ORDER_BY_USER_AND_ITEM, [room_id, user_name, item_name])
        rows = cursor.fetchall()
        return OrderRow.from_db_rows(rows)

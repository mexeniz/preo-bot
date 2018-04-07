from response import Response
from orderdb import OrderDB

class RoomOrder:
    def __init__(self, db_path=OrderDB.DEFAULT_DB_PATH):
        self.rooms_enable = {}
        self.order_db = OrderDB(db_path)

    def new_order(self, room_id, order_name):
        if room_id not in self.rooms_enable:
            self.rooms_enable[room_id] = True
            return Response.text(Response.REP_NEW_ORDERLIST_CREATED, order_name)
        else:
            return Response.text(Response.REP_DUP_ORDERLIST)

    def list_all(self):
        pass

    def list_order(self, room_id):
        text = ""
        order_list = self.order_db.get_room_order(room_id)
        for order in order_list:
            text += __order_print_user_item_amount(order) + "\n"
        text = text[:-1]
        return Response.text(Response.REP_SUMMARY_ORDERLIST, text)

    def close_order(self, room_id):
        try:
            self.rooms_enable[room_id] = False
            return Response.text(Response.REP_ORDERLIST_CLOSED)
        except KeyError:
            return None

    def end_order(self, room_id):
        self.order_db.del_room_order(room_id)
        return Response.text(Response.REP_END_ORDERLIST)

    @staticmethod
    def __order_print_user_item_amount(order):
        return "%s: %s %s" % (order.user_name, order.item_name, order.amount)

""" deprecated code use for reference
class Order:
    def __init__(self, name):
        self.name = name
        self.enable = True
        self.order_by_menu = {}
        self.order_by_user = {}

    def add_order(self, user, menu, amount=1):
        if self.enable:
            return Response.text(Response.REP_NOT_IMPLEMENT)
        else:
            return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

    def del_order(self, user, menu, amount=-1):
        if self.enable:
            return Response.text(Response.REP_NOT_IMPLEMENT)
        else:
            return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

    def set_enable(self, flag):
        self.enable = flag

    def order_by_menu_string(self):
        text = ""
        for menu, amount in self.order_by_menu:
            text += "%s %d" % (menu, amount) + "\n"
        return text[:-1]

    def order_by_user_string(self):
        text = ""
        for user, order in self.order_by_user:
            text += user + "\n"
            for menu, amount in order:
                text += menu + " " + amount + "\n"
        return text[:-1]

    def list_order_by_menu(self):
        return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_menu_string)

    def list_order_by_user(self):
        return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_user_string)

    def __str__(self):
        return self.order_by_user_string()
"""
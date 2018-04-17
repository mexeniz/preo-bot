from response import Response
from preodb import PreoDB

class RoomOrder:
    def __init__(self, db_path=PreoDB.DEFAULT_DB_PATH):
        self.rooms_enable = {}
        self.preo_db = PreoDB(db_path)

    def new_order(self, room_id, order_name):
        res = None
        if room_id not in self.rooms_enable:
            self.rooms_enable[room_id] = True
            res = Response.text(Response.REP_NEW_ORDERLIST_CREATED, order_name)
        else:
            # room order is already created yet.
            res = Response.text(Response.REP_DUP_ORDERLIST)
        return res

    def list_all(self):
        pass

    def list_order(self, room_id):
        res = None
        if room_id in self.rooms_enable:
            # room order exists.
            text = ""
            order_list = self.preo_db.get_room_order(room_id)
            for order in order_list:
                text += self.__order_print_user_item_amount(order) + "\n"
            text = text[:-1]
            res = Response.text(Response.REP_SUMMARY_ORDERLIST, text)
        else:
            # room order is not created yet.
            print("Error: room order %s does not exist" % (room_id))
        return res

    def close_order(self, room_id):
        res = None
        if room_id in self.rooms_enable:
            # room order exists.
            if self.rooms_enable[room_id]:
                # room order is opened.
                self.rooms_enable[room_id] = False
                res = Response.text(Response.REP_ORDERLIST_CLOSED)
            else:
                # room order has been already closed.
                res = Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)
        else:
            # room order is not created yet.
            print("Error: room order %s does not exist" % (room_id))
        return res

    def is_order_opened(self, room_id):
        try:
            return self.rooms_enable[room_id]
        except KeyError:
            return False

    def end_order(self, room_id):
        res = None
        try:
            del self.rooms_enable[room_id]
            self.preo_db.del_room_order(room_id)
            res = Response.text(Response.REP_END_ORDERLIST)
        except KeyError:
            print("Error: room order %s does not exist" % (room_id))
        except Exception as e:
            print(e)
        return res

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

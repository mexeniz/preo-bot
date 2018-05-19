class Response:
    LANG_EN = 0
    LANG_TH = 1

    REP_NOT_IMPLEMENT = -1
    REP_NEW_ORDERLIST_CREATED = 0
    REP_DUP_ORDERLIST = 1
    REP_SUMMARY_ORDERLIST = 2
    REP_CLOSE_ORDERLIST = 3
    REP_END_ORDERLIST = 4
    REP_ORDERLIST_CLOSED = 5
    REP_ORDER_PRINT = 6
    REP_ORDERLIST_ALREADY_CLOSED = 7
    REP_SET_ITEM = 8
    REP_DEL_ITEM = 9
    REP_DEL_NOT_EXIST_ITEM = 10
    REP_OPEN_ORDERLIST = 11
    REP_ORDERLIST_ALREADY_OPENED = 12

    LANGUAGE = LANG_EN

    @classmethod
    def set_language(cls, code):
        "Set the language of response text"
        cls.LANGUAGE = code

    @classmethod
    def text(cls, code, *args):
        if cls.LANGUAGE == cls.LANG_EN:
            if code == cls.REP_NOT_IMPLEMENT: return "Sorry, this feature is under construction"
            # list_name
            if code == cls.REP_NEW_ORDERLIST_CREATED: return "New Order '%s' created" % args
            # -
            if code == cls.REP_DUP_ORDERLIST: return "This room already has an order\nPlease end the previous order first"
            # list_name, summarized order_list
            if code == cls.REP_SUMMARY_ORDERLIST: return "===== %s Order Summary =====\n%s" % (args[0], args[1])
            # -
            if code == cls.REP_CLOSE_ORDERLIST: return "Order closed"
            # list_name, summarized order_list
            if code == cls.REP_END_ORDERLIST: return "%s order ended\n%s" % (args[0], args[1])
            # -
            if code == cls.REP_ORDERLIST_CLOSED: return "Order is closed"
            # -
            if code == cls.REP_ORDERLIST_ALREADY_CLOSED: return "Order has been already closed"
            # list_name, order_text
            if code == cls.REP_ORDER_PRINT: return "====== Order '%s' ======\n%s" % args
            # user_name, order_text
            if code == cls.REP_SET_ITEM: return "Update: %s has ordered %d %s" % (args[0], args[2], args[1])
            # user_name, order_text
            if code == cls.REP_DEL_ITEM: return "Update: %s has deleted %s order" % (args[0], args[1])
            # user_name, item_name
            if code == cls.REP_DEL_NOT_EXIST_ITEM: return "%s for %s does not exist in order list" % (args[1], args[0])
            # -
            if code == cls.REP_OPEN_ORDERLIST: return "Order is opened"
            # -
            if code == cls.REP_ORDERLIST_ALREADY_OPENED: return "Order has been already opened"

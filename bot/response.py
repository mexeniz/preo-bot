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
    REP_ADD_ITEM = 8
    REP_DEL_ITEM = 9
    REP_DEL_NOT_EXIST_ITEM = 10
    REP_ORDERLIST_OPENED = 11
    REP_ORDERLIST_ALREADY_OPENED = 12

    LANGUAGE = LANG_EN

    @staticmethod
    def set_language(code):
        LANGUAGE = code

    @staticmethod
    def text(code, *args):
        if Response.LANGUAGE == Response.LANG_EN:
            if code == Response.REP_NOT_IMPLEMENT: return "Sorry, this feature is under construction"
            # list_name
            if code == Response.REP_NEW_ORDERLIST_CREATED: return "New Order '%s' created" % args
            # -
            if code == Response.REP_DUP_ORDERLIST: return "This room already has order\nPlease end the previous order first"
            # order_list
            if code == Response.REP_SUMMARY_ORDERLIST: return "===== Order Summary =====\n%s" % args
            # -
            if code == Response.REP_CLOSE_ORDERLIST: return "Order closed"
            # -
            if code == Response.REP_END_ORDERLIST: return "Order ended"
            # -
            if code == Response.REP_ORDERLIST_CLOSED: return "Order is closed"
            # -
            if code == Response.REP_ORDERLIST_ALREADY_CLOSED: return "Order has been already closed"
            # list_name, order_text
            if code == Response.REP_ORDER_PRINT: return "====== Order '%s' ======\n%s" % args
            # user_name, order_text
            if code == Response.REP_ADD_ITEM: return "Update: %s has ordered %d %s" % (args[0], args[2], args[1])
            # user_name, order_text
            if code == Response.REP_DEL_ITEM: return "Update: %s has deleted %s order" % (args[0], args[1])
            # list_name, user_name , order_text
            if code == Response.REP_DEL_NOT_EXIST_ITEM: return "%s for %s is not exist in %s" % (args[2], args[1], args[0])
            # -
            if code == REP_OPEN_ORDERLIST: return "Order is opened"
            # -
            if code == REP_ORDERLIST_ALREADY_OPENED: return "Order has been already opened"

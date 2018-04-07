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

    LANGUAGE = LANG_EN

    @staticmethod
    def set_language(code):
        LANGUAGE = code

    @staticmethod
    def text(code, *args):
        if Response.LANGUAGE == Response.LANG_EN:
            if code == Response.REP_NOT_IMPLEMENT: return "Sorry, this feature is under construction"
            # order_name
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
            if code == Response.REP_ORDERLIST_CLOSED: return "Order is already closed"
            # order_name, order_text
            if code == Response.REP_ORDER_PRINT: return "====== Order '%s' ======\n%s" % args

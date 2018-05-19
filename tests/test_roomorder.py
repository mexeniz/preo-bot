import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from roomorder import (
    RoomOrder
)
from preodb import (
    PreoDB
)
from response import (
    Response
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"
TEST_ROOM_1 = "room1"
TEST_ORDER_1 = "order1"
TEST_ORDER_2 = "order2"
TEST_USER_NAME_1 = "user1"
TEST_USER_NAME_2 = "user2"
TEST_ITEM_1 = "food1"
TEST_ITEM_2 = "food2"
TEST_AMOUNT_1 = 1
TEST_AMOUNT_2 = 2

###########################
# RoomOrder test cases
###########################

def _mock_print_user_item_amount(user_name, item_name, amount):
    return "%s: %s %s" % (user_name, item_name, amount)

def create_mock_roomorder():
    if os.path.exists(TEST_DB_PATH):
        # clean old test database before init new RoomOrder
        os.remove(TEST_DB_PATH)
    room_order = RoomOrder(TEST_DB_PATH)
    assert isinstance(room_order, RoomOrder)
    return room_order

def test_roomorder_init():
    room_order = RoomOrder(TEST_DB_PATH)
    assert isinstance(room_order, RoomOrder)
    assert isinstance(room_order.preo_db, PreoDB)

def test_roomorder_new_order():
    room_order = create_mock_roomorder()
    reply = room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    assert reply == Response.text(Response.REP_NEW_ORDERLIST_CREATED, TEST_ORDER_1)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_set_item():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    assert reply == Response.text(Response.REP_SET_ITEM, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_2, TEST_AMOUNT_2)
    assert reply == Response.text(Response.REP_SET_ITEM, TEST_USER_NAME_2, TEST_ITEM_2, TEST_AMOUNT_2)

def test_roomorder_multiple_new_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.new_order(TEST_ROOM_1, TEST_ORDER_2)
    assert reply == Response.text(Response.REP_DUP_ORDERLIST)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_list_order_empty():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.list_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_SUMMARY_ORDERLIST, TEST_ORDER_1, "")

def test_roomorder_list_order_filled():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    # Set orders
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_1, TEST_AMOUNT_2)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_2, TEST_AMOUNT_1)
    # Expected summary list
    item1_amount = TEST_AMOUNT_1 + TEST_AMOUNT_2
    item2_amount = TEST_AMOUNT_1
    exp_sum = [
        "%s %d: %s %s(%d)" % (TEST_ITEM_1, item1_amount, TEST_USER_NAME_1, TEST_USER_NAME_2, TEST_AMOUNT_2),
        "%s %d: %s" % (TEST_ITEM_2, item2_amount, TEST_USER_NAME_1)
    ]
    reply = room_order.list_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_SUMMARY_ORDERLIST, TEST_ORDER_1, "\n".join(exp_sum))

def test_roomorder_set_item_after_closing_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    assert reply == Response.text(Response.REP_SET_ITEM, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    # Close order
    assert Response.text(Response.REP_ORDERLIST_CLOSED) == room_order.close_order(TEST_ROOM_1)
    assert False == room_order.is_order_opened(TEST_ROOM_1)
    # Try to add new item
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_2, TEST_AMOUNT_2)
    assert reply == Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)

def test_roomorder_update_item():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    # Add item for first time
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    assert reply == Response.text(Response.REP_SET_ITEM, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    reply = room_order.list_order(TEST_ROOM_1)
    text = _mock_print_user_item_amount(TEST_USER_NAME_1, TEST_ITEM_1, str(TEST_AMOUNT_1))
    assert reply == Response.text(Response.REP_SUMMARY_ORDERLIST, text)
    # Update existing item
    reply = room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_2)
    assert reply == Response.text(Response.REP_SET_ITEM, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_2)
    reply = room_order.list_order(TEST_ROOM_1)
    text = _mock_print_user_item_amount(TEST_USER_NAME_1, TEST_ITEM_1, str(TEST_AMOUNT_2))
    assert reply == Response.text(Response.REP_SUMMARY_ORDERLIST, text)

def test_roomorder_close_order_success():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    assert Response.text(Response.REP_ORDERLIST_CLOSED) == room_order.close_order(TEST_ROOM_1)
    assert False == room_order.is_order_opened(TEST_ROOM_1)
    # try to close again
    assert Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED) == room_order.close_order(TEST_ROOM_1)

def test_roomorder_close_order_fail():
    room_order = create_mock_roomorder()
    assert None == room_order.close_order(TEST_ROOM_1)

def test_roomorder_end_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    # Set orders
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_1, TEST_AMOUNT_2)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_2, TEST_AMOUNT_1)
    # Expected summary list
    item1_amount = TEST_AMOUNT_1 + TEST_AMOUNT_2
    item2_amount = TEST_AMOUNT_1
    exp_sum = [
        "%s %d: %s %s(%d)" % (TEST_ITEM_1, item1_amount, TEST_USER_NAME_1, TEST_USER_NAME_2, TEST_AMOUNT_2),
        "%s %d: %s" % (TEST_ITEM_2, item2_amount, TEST_USER_NAME_1)
    ]
    reply = room_order.end_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_END_ORDERLIST, TEST_ORDER_1, "\n".join(exp_sum))
    assert False == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_del_item():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_2, TEST_AMOUNT_2)
    reply = room_order.delete_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1)
    assert reply == Response.text(Response.REP_DEL_ITEM, TEST_USER_NAME_1, TEST_ITEM_1)
    reply = room_order.delete_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_2)
    assert reply == Response.text(Response.REP_DEL_ITEM, TEST_USER_NAME_2, TEST_ITEM_2)

def test_roomorder_del_not_exist_item():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_2, TEST_AMOUNT_2)
    reply = room_order.delete_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_2)
    assert reply == Response.text(Response.REP_DEL_NOT_EXIST_ITEM, TEST_USER_NAME_1, TEST_ITEM_2)
    reply = room_order.delete_item(TEST_ROOM_1, TEST_USER_NAME_2, TEST_ITEM_1)
    assert reply == Response.text(Response.REP_DEL_NOT_EXIST_ITEM, TEST_USER_NAME_2, TEST_ITEM_1)

def test_roomorder_del_item_after_closing_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.close_order(TEST_ROOM_1)
    reply = room_order.delete_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_2)
    assert reply == Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)

def test_roomorder_open_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.close_order(TEST_ROOM_1)
    reply = room_order.open_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_OPEN_ORDERLIST)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_open_opened_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.open_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_ORDERLIST_ALREADY_OPENED)
    assert True == room_order.is_order_opened(TEST_ROOM_1)
    room_order.set_item(TEST_ROOM_1, TEST_USER_NAME_1, TEST_ITEM_1, TEST_AMOUNT_1)
    room_order.close_order(TEST_ROOM_1)
    room_order.open_order(TEST_ROOM_1)
    #open order agian
    reply = room_order.open_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_ORDERLIST_ALREADY_OPENED)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

import pytest
import sqlite3
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from order import (
    Order
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# Order test cases
###########################


MOCK_ORDERS = [
    # first room
    ['10001', '20001', 'milk', 1],
    ['10001', '20001', 'steak', 1],
    ['10001', '20002', 'milk', 2],
    ['10001', '20003', 'milk', 1],
    ['10001', '20004', 'bread', 2],
    ['10001', '20004', 'milk', 1],
    # second room
    ['10002', '20001', 'milk', 1],
    ['10002', '20001', 'steak', 3],
    ['10002', '20002', 'milk', 1],
    ['10002', '20003', 'milk', 3],
    ['10002', '20004', 'bread', 1],
    ['10002', '20004', 'milk', 2],
    ['10002', '20005', 'tea', 1]
]
INVALID_MOCK_ORDERS = [
    ['10002', '20004', 'bread', -5],
    ['10002', '20004', 'milk', 0],
    ['10002', '20005', 'tea', -1]
]

def clean_db():
    if os.path.exists(TEST_DB_PATH):
        print("Remove DB at %s" % (TEST_DB_PATH))
        os.remove(TEST_DB_PATH)


def insert_mock_data(order):
    for data in MOCK_ORDERS:
        order.set_order(data[0], data[1], data[2], data[3])

def count_item_amount(rows, item_name):
    amount = 0
    for row in rows:
        if row[2] == item_name:
            amount = amount + row[3]
    return amount


def test_order_init():
    clean_db()
    order = Order(TEST_DB_PATH)
    assert order != None
    assert isinstance(order, Order)


def test_order_set_order_success():
    clean_db()
    order = Order(TEST_DB_PATH)
    for data in MOCK_ORDERS:
        order.set_order(data[0], data[1], data[2], data[3])
    rows = order.list_all()
    assert len(rows) == len(MOCK_ORDERS)

def test_order_set_order_fail():
    # Test orders table constraint
    clean_db()
    order = Order(TEST_DB_PATH)
    for data in INVALID_MOCK_ORDERS:
        with pytest.raises(sqlite3.IntegrityError):
            order.set_order(data[0], data[1], data[2], data[3])
    rows = order.list_all()
    assert len(rows) == 0


def test_order_del_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    insert_mock_data(order)
    for data in MOCK_ORDERS:
        order.del_order(data[0], data[1], data[2])
    rows = order.list_all()
    assert len(rows) == 0

def test_order_get_room_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_room_order('10000')
    assert len(rows) == 0
    rows = order.get_room_order('10001')
    assert len(rows) == 6

def test_order_get_user_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_user_order('10001', '20000')
    assert len(rows) == 0
    rows = order.get_user_order('10001', '20001')
    assert len(rows) == 2
    rows = order.get_user_order('10001', '20004')
    assert len(rows) == 2

def test_order_get_item_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_item_order('10001', 'rice')
    assert count_item_amount(rows, 'rice') == 0
    rows = order.get_item_order('10001', 'milk')
    assert count_item_amount(rows, 'milk') == 5
    rows = order.get_item_order('10001', 'bread')
    assert count_item_amount(rows, 'bread') == 2

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
from orderdb import (
    OrderDB
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# Order test cases
###########################


MOCK_ORDERS = [
    # first room
    ['10001', 'finn', 'milk', 1],
    ['10001', 'finn', 'steak', 1],
    ['10001', 'poe', 'milk', 2],
    ['10001', 'luke', 'milk', 1],
    ['10001', 'rey', 'bread', 2],
    ['10001', 'rey', 'milk', 1],
    # second room
    ['10002', 'hux', 'milk', 1],
    ['10002', 'hux', 'steak', 3],
    ['10002', 'snoke', 'milk', 1],
    ['10002', 'ren', 'milk', 3],
    ['10002', 'phasma', 'bread', 1],
    ['10002', 'phasma', 'milk', 2],
    ['10002', 'krennic', 'tea', 1]
]
INVALID_MOCK_ORDERS = [
    ['10002', 'hux', 'bread', -5],
    ['10002', 'hux', 'milk', 0],
    ['10002', 'krennic', 'tea', -1]
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


def test_orderdb_init():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    assert order != None
    assert isinstance(order, OrderDB)


def test_orderdb_set_order_success():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    for data in MOCK_ORDERS:
        order.set_order(data[0], data[1], data[2], data[3])
    rows = order.list_all()
    assert len(rows) == len(MOCK_ORDERS)

def test_orderdb_set_order_fail():
    # Test orders table constraint
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    for data in INVALID_MOCK_ORDERS:
        with pytest.raises(sqlite3.IntegrityError):
            order.set_order(data[0], data[1], data[2], data[3])
    rows = order.list_all()
    assert len(rows) == 0


def test_orderdb_del_order():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    insert_mock_data(order)
    for data in MOCK_ORDERS:
        order.del_order(data[0], data[1], data[2])
    rows = order.list_all()
    assert len(rows) == 0

def test_orderdb_del_room_order():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    insert_mock_data(order)
    order.del_room_order('10001')
    rows = order.get_room_order('10001')
    assert len(rows) == 0
    order.del_room_order('10002')
    rows = order.get_room_order('10002')
    assert len(rows) == 0

def test_orderdb_get_room_order():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_room_order('10000')
    assert len(rows) == 0
    rows = order.get_room_order('10001')
    assert len(rows) == 6

def test_orderdb_get_user_order():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_user_order('10001', 'noone')
    assert len(rows) == 0
    rows = order.get_user_order('10001', 'finn')
    assert len(rows) == 2
    rows = order.get_user_order('10001', 'rey')
    assert len(rows) == 2

def test_orderdb_get_item_order():
    clean_db()
    order = OrderDB(TEST_DB_PATH)
    insert_mock_data(order)
    rows = order.get_item_order('10001', 'rice')
    assert count_item_amount(rows, 'rice') == 0
    rows = order.get_item_order('10001', 'milk')
    assert count_item_amount(rows, 'milk') == 5
    rows = order.get_item_order('10001', 'bread')
    assert count_item_amount(rows, 'bread') == 2

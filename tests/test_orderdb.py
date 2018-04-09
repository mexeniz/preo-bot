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
    OrderDB, OrderRow
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# OrderRow test cases
###########################

MOCK_ROWS = [
    ['10001', 'finn', 'milk', 1],
    ['10001', 'finn', 'steak', 1]
]


def test_orderrow_init():
    room_id = "10001"
    user_name = "yoda"
    item_name = "fishburger"
    amount = 1
    order_row = OrderRow(room_id=room_id, user_name=user_name,
                         item_name=item_name, amount=amount)
    assert order_row.room_id == room_id
    assert order_row.user_name == user_name
    assert order_row.item_name == item_name
    assert order_row.amount == amount


def test_orderrow_from_db_rows():
    order_rows = OrderRow.from_db_rows(MOCK_ROWS)
    assert len(order_rows) == len(MOCK_ROWS)
    for idx, order_row in enumerate(order_rows):
        assert order_row.room_id == MOCK_ROWS[idx][0]
        assert order_row.user_name == MOCK_ROWS[idx][1]
        assert order_row.item_name == MOCK_ROWS[idx][2]
        assert order_row.amount == MOCK_ROWS[idx][3]

###########################
# OrderDB test cases
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
        # clean old test database before init new OrderDB
        os.remove(TEST_DB_PATH)


def insert_mock_data(order_db):
    for data in MOCK_ORDERS:
        order_db.set_order(data[0], data[1], data[2], data[3])


def count_item_amount(orders, item_name):
    amount = 0
    for order in orders:
        if order.item_name == item_name:
            amount = amount + order.amount
    return amount


def test_orderdb_init():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    assert order_db != None
    assert isinstance(order_db, OrderDB)


def test_orderdb_set_order_success():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    for data in MOCK_ORDERS:
        order_db.set_order(data[0], data[1], data[2], data[3])
    orders = order_db.list_all()
    assert len(orders) == len(MOCK_ORDERS)


def test_orderdb_set_order_fail():
    # Test orders table constraint
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    for data in INVALID_MOCK_ORDERS:
        with pytest.raises(sqlite3.IntegrityError):
            order_db.set_order(data[0], data[1], data[2], data[3])
    orders = order_db.list_all()
    assert len(orders) == 0


def test_orderdb_del_order():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    insert_mock_data(order_db)
    for data in MOCK_ORDERS:
        order_db.del_order(data[0], data[1], data[2])
    orders = order_db.list_all()
    assert len(orders) == 0


def test_orderdb_del_room_order():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    insert_mock_data(order_db)
    order_db.del_room_order('10001')
    orders = order_db.get_room_order('10001')
    assert len(orders) == 0
    order_db.del_room_order('10002')
    orders = order_db.get_room_order('10002')
    assert len(orders) == 0


def test_orderdb_get_room_order():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    insert_mock_data(order_db)
    orders = order_db.get_room_order('10000')
    assert len(orders) == 0
    orders = order_db.get_room_order('10001')
    assert len(orders) == 6


def test_orderdb_get_user_order():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    insert_mock_data(order_db)
    orders = order_db.get_user_order('10001', 'noone')
    assert len(orders) == 0
    orders = order_db.get_user_order('10001', 'finn')
    assert len(orders) == 2
    orders = order_db.get_user_order('10001', 'rey')
    assert len(orders) == 2


def test_orderdb_get_item_order():
    clean_db()
    order_db = OrderDB(TEST_DB_PATH)
    insert_mock_data(order_db)
    orders = order_db.get_item_order('10001', 'rice')
    assert count_item_amount(orders, 'rice') == 0
    orders = order_db.get_item_order('10001', 'milk')
    assert count_item_amount(orders, 'milk') == 5
    orders = order_db.get_item_order('10001', 'bread')
    assert count_item_amount(orders, 'bread') == 2

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
from preodb import (
    PreoDB, OrderRow
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# PreoDB test cases
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
        # clean old test database before init new PreoDB
        os.remove(TEST_DB_PATH)


def insert_mock_data(preo_db):
    for data in MOCK_ORDERS:
        preo_db.set_order(data[0], data[1], data[2], data[3])


def count_item_amount(orders, item_name):
    amount = 0
    for order in orders:
        if order.item_name == item_name:
            amount = amount + order.amount
    return amount


def test_preodb_init():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    assert preo_db != None
    assert isinstance(preo_db, PreoDB)


def test_preodb_set_order_success():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    for data in MOCK_ORDERS:
        preo_db.set_order(data[0], data[1], data[2], data[3])
    orders = preo_db.list_all()
    assert len(orders) == len(MOCK_ORDERS)


def test_preodb_set_order_fail():
    # Test orders table constraint
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    for data in INVALID_MOCK_ORDERS:
        with pytest.raises(sqlite3.IntegrityError):
            preo_db.set_order(data[0], data[1], data[2], data[3])
    orders = preo_db.list_all()
    assert len(orders) == 0


def test_preodb_del_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    for data in MOCK_ORDERS:
        preo_db.del_order(data[0], data[1], data[2])
    orders = preo_db.list_all()
    assert len(orders) == 0


def test_preodb_del_room_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    preo_db.del_room_order('10001')
    orders = preo_db.get_room_order('10001')
    assert len(orders) == 0
    preo_db.del_room_order('10002')
    orders = preo_db.get_room_order('10002')
    assert len(orders) == 0


def test_preodb_get_room_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_room_order('10000')
    assert len(orders) == 0
    orders = preo_db.get_room_order('10001')
    assert len(orders) == 6


def test_preodb_get_user_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_user_order('10001', 'noone')
    assert len(orders) == 0
    orders = preo_db.get_user_order('10001', 'finn')
    assert len(orders) == 2
    orders = preo_db.get_user_order('10001', 'rey')
    assert len(orders) == 2


def test_preodb_get_item_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_item_order('10001', 'rice')
    assert count_item_amount(orders, 'rice') == 0
    orders = preo_db.get_item_order('10001', 'milk')
    assert count_item_amount(orders, 'milk') == 5
    orders = preo_db.get_item_order('10001', 'bread')
    assert count_item_amount(orders, 'bread') == 2

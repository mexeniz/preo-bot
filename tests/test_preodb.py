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

MOCK_ROOMPROPS = [
    ['10001', 'list1'],
    ['10002', 'list2']
]

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

INVALID_MOCK_ROOMPROPS = [
    ['10001', None, -1],
    [None, 'list2', 1]
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
    for data in MOCK_ROOMPROPS:
        preo_db.new_room_order(data[0], data[1])


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

############ Test Order table ############


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
    assert preo_db.is_room_order_exist('10001')
    preo_db.del_room_order('10001')
    assert not preo_db.is_room_order_exist('10001')
    orders = preo_db.get_order_by_room('10001')
    assert len(orders) == 0

    assert preo_db.is_room_order_exist('10002')
    preo_db.del_room_order('10002')
    assert not preo_db.is_room_order_exist('10002')
    orders = preo_db.get_order_by_room('10002')
    assert len(orders) == 0


def test_preodb_get_order_by_room():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_order_by_room('10000')
    assert len(orders) == 0
    orders = preo_db.get_order_by_room('10001')
    assert len(orders) == 6


def test_preodb_get_order_by_user():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_order_by_user('10001', 'noone')
    assert len(orders) == 0
    orders = preo_db.get_order_by_user('10001', 'finn')
    assert len(orders) == 2
    orders = preo_db.get_order_by_user('10001', 'rey')
    assert len(orders) == 2


def test_preodb_get_order_by_item():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    orders = preo_db.get_order_by_item('10001', 'rice')
    assert count_item_amount(orders, 'rice') == 0
    orders = preo_db.get_order_by_item('10001', 'milk')
    assert count_item_amount(orders, 'milk') == 5
    orders = preo_db.get_order_by_item('10001', 'bread')
    assert count_item_amount(orders, 'bread') == 2

############ Test RoomProp table ############


def test_preodb_new_room_order_success():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    for data in MOCK_ROOMPROPS:
        preo_db.new_room_order(data[0], data[1])
    for data in MOCK_ROOMPROPS:
        is_exist = preo_db.is_room_order_exist(data[0])
        assert is_exist


def test_preodb_new_room_order_fail():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    for data in INVALID_MOCK_ROOMPROPS:
        with pytest.raises(sqlite3.IntegrityError):
            preo_db.new_room_order(data[0], data[1])


def test_preodb_get_room_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    assert preo_db.get_room_order('10001') != None
    assert preo_db.get_room_order('10002') != None
    assert preo_db.get_room_order('10003') == None

def test_preodb_enable_room_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    preo_db.disable_room_order('10001')
    preo_db.enable_room_order('10001')
    assert preo_db.is_room_order_enable('10001')


def test_preodb_disable_room_order():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    preo_db.disable_room_order('10001')
    assert not preo_db.is_room_order_enable('10001')


def test_preodb_is_room_order_exist():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    assert preo_db.is_room_order_exist('10001')
    # Should return false, if room id does not exist.
    assert not preo_db.is_room_order_exist('11111')


def test_preodb_is_room_order_enable():
    clean_db()
    preo_db = PreoDB(TEST_DB_PATH)
    insert_mock_data(preo_db)
    # New room prop is enabled by default.
    assert preo_db.is_room_order_enable('10001')
    # Should return false, if room id does not exist.
    assert not preo_db.is_room_order_enable('11111')

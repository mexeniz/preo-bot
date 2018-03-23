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
    ['10001', '20001', 'milk', 1],
    ['10001', '20001', 'steak', 1],
    ['10001', '20002', 'milk', 1],
    ['10001', '20003', 'milk', 1],
    ['10001', '20004', 'bread', 2],
    ['10001', '20004', 'milk', 1]
]


def clean_db():
    print("Remove DB at %s" % (TEST_DB_PATH))
    os.remove(TEST_DB_PATH)


def insert_mock_data(order):
    for data in MOCK_ORDERS:
        order.set_order(data[0], data[1], data[2], data[3])


def test_order_init():
    clean_db()
    order = Order(TEST_DB_PATH)
    assert order != None
    assert isinstance(order, Order)


def test_order_set_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    for data in MOCK_ORDERS:
        order.set_order(data[0], data[1], data[2], data[3])
    rows = order.list_all()
    assert len(rows) == len(MOCK_ORDERS)


def test_order_del_order():
    clean_db()
    order = Order(TEST_DB_PATH)
    insert_mock_data(order)
    for data in MOCK_ORDERS:
        order.del_order(data[0], data[1], data[2])
    rows = order.list_all()
    assert len(rows) == 0

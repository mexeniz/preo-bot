import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from order import (
    RoomOrder
)
from orderdb import (
    OrderDB
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# RoomOrder test cases
###########################

def create_mock_roomorder():
    if os.path.exists(TEST_DB_PATH):
        # clean old test database before init new RoomOrder
        os.remove(TEST_DB_PATH)
    return RoomOrder(TEST_DB_PATH)

def test_roomorder_init():
    room_order = RoomOrder(TEST_DB_PATH)
    assert isinstance(room_order, RoomOrder)
    assert isinstance(room_order.rooms, dict)
    assert isinstance(room_order.order_db, OrderDB)

def test_roomorder_new_order():
    room_order = create_mock_roomorder()
    # Wait for test case
    pytest.fail()

def test_roomorder_list_order():
    room_order = create_mock_roomorder()
    # Wait for test case
    pytest.fail()

def test_roomorder_close_order():
    room_order = create_mock_roomorder()
    # Wait for test case
    pytest.fail()

def test_roomorder_end_order():
    room_order = create_mock_roomorder()
    # Wait for test case
    pytest.fail()

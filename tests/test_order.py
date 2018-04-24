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
    OrderRow,
    RoomStatus
)

###########################
# OrderRow test cases
###########################

MOCK_ROWS = [
    ['10001', 'finn', 'milk', 1],
    ['10001', 'finn', 'steak', 1]
]

MOCK_INVALID_ROWS = [
    ['10001', 'finn', 'milk']
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


def test_orderrow_from_db_rows_success():
    order_rows = OrderRow.from_db_rows(MOCK_ROWS)
    assert len(order_rows) == len(MOCK_ROWS)
    for idx, order_row in enumerate(order_rows):
        assert order_row.room_id == MOCK_ROWS[idx][0]
        assert order_row.user_name == MOCK_ROWS[idx][1]
        assert order_row.item_name == MOCK_ROWS[idx][2]
        assert order_row.amount == MOCK_ROWS[idx][3]

def test_orderrow_from_db_rows_fail():
    with pytest.raises(Exception):
        # some Exception should be raise
        _ = OrderRow.from_db_rows(MOCK_INVALID_ROWS)

MOCK_INVALID_ROOMS = [
    ['room_001', 1, 2]
]

def test_roomStatus_init():
    room_id = "room_001"
    status = 1
    room_status = RoomStatus(room_id=room_id, is_enable=status)
    assert room_status.room_id == room_id
    assert room_status.is_enable == status

def test_roomStatus_from_db_rows_fail():
    with pytest.raises(Exception):
        # some Exception should be raise
        _ = RoomStatus.from_db_rows(MOCK_INVALID_ROOMS)

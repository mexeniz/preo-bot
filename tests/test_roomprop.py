import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from roomprop import (
    RoomPropRow
)

###########################
# OrderRow test cases
###########################

MOCK_ROWS = [
    ['10001', 'room1', 1],
    ['10002', 'room2', 0]
]

MOCK_INVALID_ROWS = [
    ['10001', 'room1']
]

def test_roomproprow_init():
    room_id = "10001"
    list_name = "list1"
    enable = 1
    room_prop_row = RoomPropRow(room_id=room_id, list_name=list_name, enable=enable)
    assert room_prop_row.room_id == room_id
    assert room_prop_row.list_name == list_name
    assert room_prop_row.enable == enable

def test_roomproprow_from_db_rows_success():
    for idx, mock_row in enumerate(MOCK_ROWS):
        room_prop_row = RoomPropRow.from_db_row(mock_row)
        assert room_prop_row.room_id == MOCK_ROWS[idx][0]
        assert room_prop_row.list_name == MOCK_ROWS[idx][1]
        assert room_prop_row.enable == MOCK_ROWS[idx][2]

def test_roomproprow_from_db_rows_fail():
    with pytest.raises(Exception):
        # some Exception should be raise
        _ = RoomPropRow.from_db_row(MOCK_INVALID_ROWS)

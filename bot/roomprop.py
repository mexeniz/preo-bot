# @Description : Structures for keeping room property from users.

class RoomPropQuery:
    "SQL Queries for RoomProp class"
    INIT_SCHEMA = """
            CREATE TABLE IF NOT EXISTS room_props (
            room_id  CHAR(128) NOT NULL PRIMARY KEY,
			list_name CHAR(128) NOT NULL,
			enable INT NOT NULL CHECK(enable == 0 OR enable == 1));
            """

    INSERT_ROOM_PROP = "INSERT OR REPLACE INTO room_props (room_id, list_name, enable) VALUES (?,?,?)"
    SET_ROOM_PROP = "UPDATE room_props SET enable = ? WHERE room_id = ?"

    READ_ROOM_PROP = "SELECT room_id, list_name, enable FROM room_props WHERE room_id = ?"
    DEL_ROOM_PROP = "DELETE FROM room_props WHERE room_id = ?"

class RoomPropRow:
    "An instance for storing room property row"

    def __init__(self, **kwargs):
        self.room_id = kwargs['room_id']
        self.list_name = kwargs['list_name']
        self.enable = kwargs['enable']

    @classmethod
    def from_db_row(cls, row):
        try:
            return cls.__init__(room_id=row[0], list_name=row[1], enable=int(row[2]))
        except Exception:
            raise

# @Description : Structures for keeping room property from users.

class RoomPropQuery:
    "SQL Queries for RoomProp class"
    INIT_SCHEMA = """
            CREATE TABLE IF NOT EXISTS room_props (
            room_id  CHAR(128) NOT NULL PRIMARY KEY,
			list_name CHAR(128) NOT NULL,
			enable INT NOT NULL);
            """

    INSERT_ROOM_PROP = """
        INSERT INTO room_props (room_id, list_name, enable) VALUES (?,?,?)"""

    READ_ROOM_PROP = "SELECT room_id, list_name, order FROM room_props WHERE room_id = ?"
    READ_ROOM_PROP = "DELETE FROM room_props WHERE room_id = ?"

class RoomPropRow:
    "An instance for storing room property row"

    def __init__(self, **kwargs):
        self.room_id = kwargs['room_id']
        self.list_name = kwargs['list_name']
        self.enable = kwargs['enable']

    @classmethod
    def from_db_rows(cls, rows):
        room_props = []
        for row in rows:
            try:
                room_props.append(cls(room_id=row[0], list_name=row[1], enable=row[2]))
            except Exception:
                raise
        return room_props

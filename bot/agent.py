from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from roomorder import (
    RoomOrder
)
import re


class BotCMD():
    "Enum class for bot command"
    UNKNOWN_CMD = 0
    NEW_ORDER = 1
    SET_ORDER = 2
    DEL_ORDER = 3
    LIST_ORDER = 4
    CLOSE_ORDER = 5
    OPEN_ORDER = 6
    END_ORDER = 7
    HELP = 8

    CMD_DICT = {
        "new": NEW_ORDER,
        "set": SET_ORDER,
        "del": DEL_ORDER,
        "list": LIST_ORDER,
        "close": CLOSE_ORDER,
        "open": OPEN_ORDER,
        "end": END_ORDER,
        "help": HELP
    }

    @classmethod
    def parse_command(cls, text):
        command = cls.UNKNOWN_CMD
        if text:
            text = text.strip().lower()
            if text in cls.CMD_DICT:
                command = cls.CMD_DICT[text]
        return command


class GroupParser():
    """
    Class for parsing text into several parts
    Support several regexes
    """

    # TODO(M) : Fix reqex to support Thai item and user_name.
    order_regexes = [r"^!(\w+)$",
                     r"^!(\w+) ([\u0E00-\u0E7F\w]+)$",
                     r"^!(\w+) ([\u0E00-\u0E7F\w]+) ([\u0E00-\u0E7F\w]+)$",
                     r"^!(\w+) ([\u0E00-\u0E7F\w]+) ([\u0E00-\u0E7F\w]+) (\d{1,})$"]
    text_groups = [["cmd"],
                   ["cmd", "name"],
                   ["cmd", "user_name", "item"],
                   ["cmd", "user_name", "item", "num"]]

    @classmethod
    def parse_text_group(cls, text):
        text = text.strip()
        result = {}
        i = -1
        for order_regex in GroupParser.order_regexes:
            i += 1
            m = re.match(order_regex, text)
            if m == None:
                continue
            try:
                j = 0
                for match in GroupParser.text_groups[i]:
                    j += 1
                    result[match] = m.group(j)
                return result
            except:
                continue
        return None


class Agent():
    """Chatbot agent for handling incoming message event"""
    HELP_MESSAGE = "\n".join(["Available PreoBot commands", "!new <list_name>", "!set <user_name> <item> <amount>",
                              "!del <user_name> <item>", "!end", "!open", "!close", "!list", "!help"])

    def __init__(self, **kwargs):
        if 'db_path' in kwargs:
            self.room_orders = RoomOrder(kwargs['db_path'])
        else:
            # use default config
            self.room_orders = RoomOrder()

    def __handle_new_order(self, **kwargs):
        """
        Create new order list.
        Store order list properties such as name in room_dict using room_id as a key.
        """
        return self.room_orders.new_order(kwargs['room_id'], kwargs['name'])

    def __handle_set_order(self, **kwargs):
        """
        Add an order from user into database with room_id, user_name, item and amount.
        """
        return self.room_orders.set_item(kwargs['room_id'], kwargs['user_name'], kwargs['item'], kwargs['amount'])


    def __handle_del_order(self, **kwargs):
        """
        Delete an order from database by room_id, user_name and item.
        """
        return self.room_orders.delete_item(kwargs['room_id'], kwargs['user_name'], kwargs['item'])

    def __handle_list_order(self, **kwargs):
        """
        Show the list of orders by room_id.
        Error message will be return if an order list is not created yet.
        """
        return self.room_orders.list_order(kwargs['room_id'])

    def __handle_close_order(self, **kwargs):
        """
        Close the list of orders by room_id. After that, user can only list the order.
        Error message will be return if an order list is not created yet.
        """
        return self.room_orders.close_order(kwargs['room_id'])

    def __handle_open_order(self, **kwargs):
        """
        Open the closed list of orders by room_id. After that, user can edit the order.
        Error message will be return if an order list is not created yet.
        """
        return self.room_orders.open_order(kwargs['room_id'])

    def __handle_end_order(self, **kwargs):
        """
        Remove the list of orders by room_id and remove room_id key from room_dict.
        Any orders from this room will be deleted from database.
        Error message will be return if an order list is not created yet.
        """
        return self.room_orders.end_order(kwargs['room_id'])

    def __handle_help(self, **kwargs):
        """
        Show a list of bot commands.
        """
        return self.HELP_MESSAGE

    def handle_text_message(self, event):
        "Handle text message event."
        group_text = GroupParser.parse_text_group(event.message.text)
        if group_text == None:
            # TODO(M) : Should throw textParserError
            # Text is not in valid format.
            return None
        cmd = BotCMD.parse_command(group_text['cmd'])
        if cmd == BotCMD.UNKNOWN_CMD:
            # TODO(M) : Should throw botCommandError
            # Invalid command.
            return None
        # Get room_id/group_id/user_id as room_id
        room_id = None
        if hasattr(event.source, 'group_id'):
            room_id = event.source.group_id
        elif hasattr(event.source, 'room_id'):
            room_id = event.source.room_id
        else:
            room_id = event.source.user_id
        print("Handle message from room_id: %s groupt_text=%s" %
              (room_id, group_text))
        # Handle group_text
        try:
            if cmd == BotCMD.NEW_ORDER:
                response = self.__handle_new_order(
                    room_id=room_id, name=group_text['name'])
            elif cmd == BotCMD.SET_ORDER:
                response = self.__handle_set_order(room_id=room_id, user_name=group_text['user_name'],
                                                   item=group_text['item'], amount=int(group_text['num']))
            elif cmd == BotCMD.DEL_ORDER:
                response = self.__handle_del_order(room_id=room_id,
                                                   user_name=group_text['user_name'], item=group_text['item'])
            elif cmd == BotCMD.LIST_ORDER:
                response = self.__handle_list_order(room_id=room_id)
            elif cmd == BotCMD.CLOSE_ORDER:
                response = self.__handle_close_order(room_id=room_id)
            elif cmd == BotCMD.OPEN_ORDER:
                response = self.__handle_open_order(room_id=room_id)
            elif cmd == BotCMD.END_ORDER:
                response = self.__handle_end_order(room_id=room_id)

            elif cmd == BotCMD.HELP:
                response = self.__handle_help()
            return response
        except Exception as e:
            return None

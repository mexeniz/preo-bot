from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from orderdb import (
    OrderDB
)
from order import (
    RoomOrder, Order
)
import re


class BotCMD():
    "Enum class for bot command"
    UNKNOWN_CMD = 0
    NEW_ORDER = 1
    ADD_ORDER = 2
    DEL_ORDER = 3
    END_ORDER = 4
    LIST_ORDER = 5
    HELP = 6

    CMD_DICT = {
        "new": NEW_ORDER,
        "add": ADD_ORDER,
        "del": DEL_ORDER,
        "end": END_ORDER,
        "list": LIST_ORDER,
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
    HELP_MESSAGE = "\n".join(["Help message", "!new <order_name>", "!add <user_name> <item> <amount>",
                              "!del <user_name> <item> <amount>", "!end", "!list", "!help"])

    def __init__(self):
        # Map room_id with order property
        self.roomOrders = RoomOrder()

    def __handle_new_order(self, **kwargs):
        """
        Create new order list.
        Store order list properties such as name in room_dict using room_id as a key.
        """
        # return "new order list\nroom_id=%s name=%s" % (kwargs['room_id'], kwargs['name'])
        return self.roomOrders.new_order(room=kwargs['room_id'], order_name=kwargs['name'])

    def __handle_add_order(self, **kwargs):
        """
        Add an order from user into database with room_id, user_name, item and amount.
        """
        return "add order\nroom_id=%s user=%s order=%s amount=%d" % (kwargs['room_id'],
                                                                     kwargs['user_name'], kwargs['item'], kwargs['amount'])

    def __handle_del_order(self, **kwargs):
        """
        Delete an order from database by room_id, user_name and item.
        """
        return "del order\nroom_id=%s user=%s order=%s" % (kwargs['room_id'],
                                                           kwargs['user_name'], kwargs['item'])

    def __handle_end_order(self, **kwargs):
        """
        Close the list of orders by room_id and remove room_id key from room_dict.
        Any orders from this room will be deleted from database.
        Error message will be return if an order list is not created yet.
        """
        # return "end order list\nroom_id=%s" % (kwargs['room_id'])
        return self.roomOrders.end_order(room=kwargs['room_id'])

    def __handle_list_order(self, **kwargs):
        """
        Show the list of orders by room_id.
        Error message will be return if an order list is not created yet.
        """
        # return "show order list\nroom_id=%s" % (kwargs['room_id'])
        return self.roomOrders.list_order(room=kwargs['room_id'])

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
            elif cmd == BotCMD.ADD_ORDER:
                response = self.__handle_add_order(room_id=room_id, user_name=group_text['user_name'],
                                                   item=group_text['item'], amount=int(group_text['num']))
            elif cmd == BotCMD.DEL_ORDER:
                response = self.__handle_del_order(room_id=room_id,
                                                   user_name=group_text['user_name'], item=group_text['item'])
            elif cmd == BotCMD.END_ORDER:
                response = self.__handle_end_order(room_id=room_id)
            elif cmd == BotCMD.LIST_ORDER:
                response = self.__handle_list_order(room_id=room_id)
            elif cmd == BotCMD.HELP:
                response = self.__handle_help()
            return response
        except Exception as e:
            return None

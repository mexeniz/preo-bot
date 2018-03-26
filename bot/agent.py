from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
       MessageEvent, TextMessage, TextSendMessage,
)
import re

class BotCMD():
    "Enum class for bot command"
    UNKNOWN_CMD = 0
    NEW_ORDER = 1
    ADD_ORDER = 2
    CMD_DICT = {
        "new" : NEW_ORDER,
        "add" : ADD_ORDER
    }
    @classmethod
    def parse_command(cls, text):
        command = cls.UNKNOWN_CMD
        if text and text in cls.CMD_DICT:
            command = cls.CMD_DICT[text]
        return command

class GroupParser():
    """Class for parsing text into several part"""
    order_regex = "^(\w+) (.*) (\d{1,})$"
    text_group = ["cmd", "order", "num"]

    @classmethod
    def parse_text_group(cls, text):
        m = re.match(GroupParser.order_regex, text)
        if not m:
            return None 

        result = {}
        try:
            i = 0
            for match in GroupParser.text_group:
                i += 1
                result[match] = m.group(i);
        except:
            return None 
        return result

class Agent():

    """Chatbot agent"""
    def __init__ (self):
        self.group_dict = {}

    def handle_text_message(self, event):
        "Handle text message event."
        return event.message.text

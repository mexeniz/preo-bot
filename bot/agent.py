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
    """
    Class for parsing text into several parts
    Support several regexes
    """
    order_regexes = ["^!(\w+)$", "^!(\w+) (.*) (\d{1,})$"]
    text_groups = [ ["cmd"], ["cmd", "order", "num"] ]

    @classmethod
    def parse_text_group(cls, text):
        result = {} 
        i = -1
        for order_regex in GroupParser.order_regexes:
            i += 1
            m = re.match(order_regex, text)
            print text, m
            if m == None:
                continue 
            try:
                j = 0
                for match in GroupParser.text_groups[i]:
                    j += 1
                    result[match] = m.group(j);
                return result
            except:
                continue
        return None 

class Agent():

    """Chatbot agent"""
    def __init__ (self):
        self.group_dict = {}

    def handle_text_message(self, event):
        "Handle text message event."
        return event.message.text

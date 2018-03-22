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

class Agent():

    """Chatbot agent"""
    def __init__ (self):
        self.group_dict = {}

    def handle_text_message(self, event):
        "Handle text message event."
        return event.message.text

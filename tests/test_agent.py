import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))

from agent import (
    Agent, BotCMD
)
from linebot.models import (
    MessageEvent, TextMessage
)
###########################
# BotCMD test cases
###########################

def test_bot_cmd_parse_command():
    assert BotCMD.parse_command("new") == BotCMD.NEW_ORDER
    assert BotCMD.parse_command("add") == BotCMD.ADD_ORDER
    assert BotCMD.parse_command("") == BotCMD.UNKNOWN_CMD
    assert BotCMD.parse_command(None) == BotCMD.UNKNOWN_CMD

###########################
# Agent test cases
###########################

# Init agent and mock object
agent = Agent()
text_message = TextMessage(text="mock message")
mock_event = MessageEvent(timestamp=123, source='123',
                          reply_token='123', message=text_message)


def test_agent_handle_text_message():
    assert agent.handle_text_message(mock_event) == mock_event.message.text

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))

from agent import (
    Agent, BotCMD, GroupParser
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
# GroupParser test cases
###########################

def test_bot_text_group_parser():
    # return None because last group must be number
    assert GroupParser.parse_text_group("a b c") == None
    # Return correctly 
    assert GroupParser.parse_text_group("a b 5") == {"cmd":"a", "order":"b", "num": "5"} 
    # Return correctly 
    assert GroupParser.parse_text_group("a b c 5") == {"cmd":"a", "order":"b c", "num": "5"} 
    # Not match regex, return None 
    assert GroupParser.parse_text_group("a b") == None
    # Not match regex, return None 
    assert GroupParser.parse_text_group("a 5") == None
    # Not match regex, return None 
    assert GroupParser.parse_text_group("HelloWorld") == None
    # "order" should handle special char correclty
    assert GroupParser.parse_text_group("add Hamburger,Steak 5") == {"cmd":"add", "order":"Hamburger,Steak", "num":"5"}
    # "num" only count last number; other number will be in "order"
    assert GroupParser.parse_text_group("add Hamburger,Steak 5 19") == {"cmd":"add", "order":"Hamburger,Steak 5", "num":"19"}

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

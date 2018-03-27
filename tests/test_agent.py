import pytest
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
from linebot.models import (
    SourceGroup, SourceRoom, SourceUser
)

###########################
# BotCMD test cases
###########################

def test_bot_cmd_parse_command():
    assert BotCMD.parse_command("new") == BotCMD.NEW_ORDER
    assert BotCMD.parse_command("add") == BotCMD.ADD_ORDER
    assert BotCMD.parse_command("del") == BotCMD.DEL_ORDER
    assert BotCMD.parse_command("end") == BotCMD.END_ORDER
    assert BotCMD.parse_command("list") == BotCMD.LIST_ORDER
    assert BotCMD.parse_command("help") == BotCMD.HELP
    assert BotCMD.parse_command("") == BotCMD.UNKNOWN_CMD
    assert BotCMD.parse_command(None) == BotCMD.UNKNOWN_CMD

###########################
# GroupParser test cases
###########################

def test_bot_group_parser():
    # Return correctly
    assert GroupParser.parse_text_group("!a b c 5") == {"cmd":"a", "user_name":"b", "item":"c", "num": "5"}
    assert GroupParser.parse_text_group("!a b") == {"cmd":"a", "name":"b"}
    assert GroupParser.parse_text_group("!a 5") == {"cmd":"a", "name":"5"}
    # Not match regex, return None
    assert GroupParser.parse_text_group("!a b c -1") == None
    assert GroupParser.parse_text_group("!a 5 b") == None
    assert GroupParser.parse_text_group("a b 5") == None
    assert GroupParser.parse_text_group("!add user1 Steak 5 19") == None
    # "item" should handle special char correclty
    assert GroupParser.parse_text_group("!add user1 Hamburger 5") == {"cmd":"add", "user_name":"user1", "item":"Hamburger", "num":"5"}
    # Single Command
    assert GroupParser.parse_text_group("!Help") == {"cmd":"Help"}
    assert GroupParser.parse_text_group("Help") == None
    assert GroupParser.parse_text_group("Help5") == None
    assert GroupParser.parse_text_group("Help help") == None
    # From Real Command
    assert GroupParser.parse_text_group("!new ploen") == {"cmd":"new", "name": "ploen"}
    assert GroupParser.parse_text_group("!add food food 3") == {"cmd":"add", "user_name":"food", "item":"food", "num":"3"}
    assert GroupParser.parse_text_group("!del food food 3") == {"cmd":"del", "user_name":"food", "item":"food", "num":"3"}
    assert GroupParser.parse_text_group("!end") == {"cmd":"end"}
    assert GroupParser.parse_text_group("!list") == {"cmd":"list"}
    assert GroupParser.parse_text_group("!help") == {"cmd":"help"}

###########################
# Agent test cases
###########################

# Init agent and mock object
agent = Agent()

def test_agent_new():
    assert agent.room_dict != None
    assert len(agent.room_dict) == 0
    assert agent.order_db != None

def test_agent_handle_text_message_fail():
    # Parser error
    text_message = TextMessage(text="mock message")
    mock_event = MessageEvent(timestamp=123, source='123',
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) == None
    # Command error
    text_message = TextMessage(text="!yatta order")
    mock_event = MessageEvent(timestamp=123, source='123',
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) == None


def test_agent_handle_text_message_group_source():
    group_source = SourceGroup(group_id="G20001", user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=group_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None

def test_agent_handle_text_message_room_source():
    room_source = SourceRoom(room_id="R20001", user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=room_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None

def test_agent_handle_text_message_user_source():
    user_source = SourceUser(user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=user_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None

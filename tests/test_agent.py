#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from order import (
    RoomOrder
)
from linebot.models import (
    MessageEvent, TextMessage
)
from linebot.models import (
    SourceGroup, SourceRoom, SourceUser
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"

###########################
# BotCMD test cases
###########################


def test_bot_cmd_parse_command():
    assert BotCMD.parse_command("new") == BotCMD.NEW_ORDER
    assert BotCMD.parse_command("add") == BotCMD.ADD_ORDER
    assert BotCMD.parse_command("del") == BotCMD.DEL_ORDER
    assert BotCMD.parse_command("list") == BotCMD.LIST_ORDER
    assert BotCMD.parse_command("close") == BotCMD.CLOSE_ORDER
    assert BotCMD.parse_command("end") == BotCMD.END_ORDER
    assert BotCMD.parse_command("help") == BotCMD.HELP
    assert BotCMD.parse_command("") == BotCMD.UNKNOWN_CMD
    assert BotCMD.parse_command(None) == BotCMD.UNKNOWN_CMD
    # Mixed case
    assert BotCMD.parse_command("NeW") == BotCMD.NEW_ORDER
    assert BotCMD.parse_command("lISt") == BotCMD.LIST_ORDER
    # Upper case
    assert BotCMD.parse_command("ADD") == BotCMD.ADD_ORDER
    assert BotCMD.parse_command("HELP") == BotCMD.HELP

###########################
# GroupParser test cases
###########################


def test_bot_group_parser():
    # Return correctly
    assert GroupParser.parse_text_group(
        "!a b c 5") == {"cmd": "a", "user_name": "b", "item": "c", "num": "5"}
    assert GroupParser.parse_text_group(
        "!a b c") == {"cmd": "a", "user_name": "b", "item": "c"}
    assert GroupParser.parse_text_group("!a b") == {"cmd": "a", "name": "b"}
    assert GroupParser.parse_text_group("!a 5") == {"cmd": "a", "name": "5"}
    # Space at beginning or ending shoud not affect
    assert GroupParser.parse_text_group(" !a ") == {"cmd": "a"}
    assert GroupParser.parse_text_group("!a b ") == {"cmd": "a", "name": "b"}
    assert GroupParser.parse_text_group(" !a b") == {"cmd": "a", "name": "b"}
    # Not match regex, return None
    assert GroupParser.parse_text_group("!a b c -1") == None
    assert GroupParser.parse_text_group("a b 5") == None
    assert GroupParser.parse_text_group("!add user1 Steak 5 19") == None
    # Single Command
    assert GroupParser.parse_text_group("!Help") == {"cmd": "Help"}
    assert GroupParser.parse_text_group("Help") == None
    assert GroupParser.parse_text_group("Help5") == None
    assert GroupParser.parse_text_group("Help help") == None
    # From Real Command
    assert GroupParser.parse_text_group("!new ploen") == {
        "cmd": "new", "name": "ploen"}
    assert GroupParser.parse_text_group("!add food food 3") == {
        "cmd": "add", "user_name": "food", "item": "food", "num": "3"}
    assert GroupParser.parse_text_group("!add user1 Hamburger 5") == {
        "cmd": "add", "user_name": "user1", "item": "Hamburger", "num": "5"}
    assert GroupParser.parse_text_group("!del food food") == {
        "cmd": "del", "user_name": "food", "item": "food"}
    assert GroupParser.parse_text_group("!del food food 3") == {
        "cmd": "del", "user_name": "food", "item": "food", "num": "3"}
    assert GroupParser.parse_text_group("!list") == {"cmd": "list"}
    assert GroupParser.parse_text_group("!close") == {"cmd": "close"}
    assert GroupParser.parse_text_group("!end") == {"cmd": "end"}
    assert GroupParser.parse_text_group("!help") == {"cmd": "help"}
    # From Real Command (mixed and upper case)
    assert GroupParser.parse_text_group("!DeL food food 3") == {
        "cmd": "DeL", "user_name": "food", "item": "food", "num": "3"}
    assert GroupParser.parse_text_group("!END") == {"cmd": "END"}
    assert GroupParser.parse_text_group("!ClOse") == {"cmd": "ClOse"}

    # Testing Thai Language
    assert GroupParser.parse_text_group("!new เพลิน") == {
        "cmd": "new", "name": "เพลิน"}
    assert GroupParser.parse_text_group("!add แบ้ง อาหาร 3") == {
        "cmd": "add", "user_name": "แบ้ง", "item": "อาหาร", "num": "3"}
    assert GroupParser.parse_text_group("!add เอ็ม ผัดกะเพราหมูสับไม่ใส่กะเพรา 5") == {
        "cmd": "add", "user_name": "เอ็ม", "item": "ผัดกะเพราหมูสับไม่ใส่กะเพรา", "num": "5"}
    assert GroupParser.parse_text_group("!del กิ๊กกัน โลกทั้งใบ") == {
        "cmd": "del", "user_name": "กิ๊กกัน", "item": "โลกทั้งใบ"}
    assert GroupParser.parse_text_group("!del คน มนุษย์ 3") == {
        "cmd": "del", "user_name": "คน", "item": "มนุษย์", "num": "3"}

###########################
# Agent test cases
###########################


TEST_ROOM_1 = "room1"
TEST_ORDER_1 = "order1"
TEST_USER_NAME_1 = "user_name1"
TEST_ITEM_1 = "item1"


def create_mock_agent():
    if os.path.exists(TEST_DB_PATH):
        # clean old test database before init new Agent
        os.remove(TEST_DB_PATH)
    mock_agent = Agent(db_path=TEST_DB_PATH)
    assert isinstance(mock_agent, Agent)
    return mock_agent


def test_agent_new():
    agent = create_mock_agent()
    assert isinstance(agent, Agent)
    assert isinstance(agent.room_orders, RoomOrder)


def test_agent_handle_text_message_fail():
    agent = create_mock_agent()
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
    agent = create_mock_agent()
    group_source = SourceGroup(group_id="G20001", user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=group_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None


def test_agent_handle_text_message_room_source():
    agent = create_mock_agent()
    room_source = SourceRoom(room_id="R20001", user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=room_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None


def test_agent_handle_text_message_user_source():
    agent = create_mock_agent()
    user_source = SourceUser(user_id="U10001")
    text_message = TextMessage(text="!new myOrder")
    mock_event = MessageEvent(timestamp=123, source=user_source,
                              reply_token='123', message=text_message)
    assert agent.handle_text_message(mock_event) != None


def test_agent_handle_new_order():
    agent = create_mock_agent()
    assert agent._Agent__handle_new_order(
        room_id=TEST_ROOM_1, name=TEST_ORDER_1) != None


def test_agent_handle_add_order():
    agent = create_mock_agent()
    assert agent._Agent__handle_add_order(
        room_id=TEST_ROOM_1, user_name=TEST_USER_NAME_1, item=TEST_ITEM_1, amount=1) != None


def test_agent_handle_del_order():
    agent = create_mock_agent()
    assert agent._Agent__handle_del_order(
        room_id=TEST_ROOM_1, user_name=TEST_USER_NAME_1, item=TEST_ITEM_1) != None


def test_agent_handle_list_order():
    agent = create_mock_agent()
    agent._Agent__handle_new_order(room_id=TEST_ROOM_1, name=TEST_ORDER_1)
    assert agent._Agent__handle_list_order(room_id=TEST_ROOM_1) != None


def test_agent_handle_close_order():
    agent = create_mock_agent()
    agent._Agent__handle_new_order(room_id=TEST_ROOM_1, name=TEST_ORDER_1)
    assert agent._Agent__handle_close_order(room_id=TEST_ROOM_1) != None


def test_agent_handle_end_order():
    agent = create_mock_agent()
    agent._Agent__handle_new_order(room_id=TEST_ROOM_1, name=TEST_ORDER_1)
    assert agent._Agent__handle_end_order(room_id=TEST_ROOM_1) != None


def test_agent_handle_help():
    agent = create_mock_agent()
    assert agent._Agent__handle_help() == Agent.HELP_MESSAGE

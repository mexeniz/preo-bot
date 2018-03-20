import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/bot')
from agent import Agent

agent = Agent()

def test_say_hi():
    assert agent.say_hi() == "Hi"

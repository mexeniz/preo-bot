import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from order import (
    OrderPool, OrderList, Order
)

###########################
# OrderPool test cases
###########################


def test_order_pool_init():
    order_pool = OrderPool()
    assert order_pool != None
    assert isinstance(order_pool, OrderPool)

###########################
# OrderList test cases
###########################


def test_order_list_init():
    order_list = OrderList()
    assert order_list != None
    assert isinstance(order_list, OrderList)

###########################
# Order test cases
###########################


def test_order_init():
    order = Order()
    assert order != None
    assert isinstance(order, Order)

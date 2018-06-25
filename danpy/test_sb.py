import pytest
import time
from unittest.mock import patch, call
from .sb import *

def test_double_input():
  output = double_input(2)
  assert output == 4, "Error with double_input."

@patch('builtins.print')
def test_print_input(mocked_print):
  print_input('This is a test.')
  assert mocked_print.mock_calls == [call('This is a test.')], "Error with print statement generated from " + print_input.__name__()

def test_dsb__init__():
    statusbar = dsb()
    current_time = time.time()
    assert hasattr(statusbar,'counter'), "self.counter not initialized for dsb()"
    assert hasattr(statusbar,'time_array'), "self.time_array not initialized for dsb()"
    assert hasattr(statusbar,'start_time'), "self.start_time not initialized for dsb()"
    assert hasattr(statusbar,'time_left'), "self.time_left not initialized for dsb()"
    
    assert statusbar.counter == 0, \
        "Error initializing self.counter for dsb(). Should be 0, instead of " + str(statusbar.counter)
    assert statusbar.time_array == [], \
        "Error initializing self.time_array. Should be [], instead of " + str(statusbar.time_array)
    assert abs(statusbar.start_time - current_time)<1e-4, \
        "Error initializing self.start_time. Should be " + str(current_time) + ", instead of " + str(statusbar.start_time)
    assert statusbar.time_left == "--", \
        "Error initializing self.time_array. Should be '--', instead of " + str(statusbar.time_left)

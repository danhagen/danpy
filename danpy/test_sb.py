import pytest
import time
from unittest.mock import patch, call
import os
import subprocess
from .sb import *

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
    del(statusbar,current_time)

def test_get_terminal_width():
    assert get_terminal_width() == 80, "Error with get_terminal_width(). Should be 80 (default pytest terminal size), instead of " + str(get_terminal_width())
    assert int(subprocess.check_output(["tput","cols"])) == 80, "Error with get_terminal_width() ImportError mode. The value of int(subprocess.check_output(['tput','cols'])) should be 80 (default pytest terminal size), instead of " + str(int(subprocess.check_output(["tput","cols"])))

def test_dsb_reset():
    statusbar = dsb()
    for i in range(10):
        time.sleep(0.1)
        statusbar.update(i,10)
    statusbar.reset()
    current_time = time.time()

    assert not hasattr(statusbar,"bar_indices"), "Error resetting dsb(). bar_indices should not exist."

    assert hasattr(statusbar,'counter'), "self.counter not initialized for dsb()"
    assert hasattr(statusbar,'time_array'), "self.time_array not initialized for dsb()"
    assert hasattr(statusbar,'start_time'), "self.start_time not initialized for dsb()"
    assert hasattr(statusbar,'time_left'), "self.time_left not initialized for dsb()"

    assert statusbar.counter == 0, \
        "Error initializing self.counter for dsb(). Should be 0, instead of " + str(statusbar.counter)
    assert statusbar.time_array == [], \
        "Error initializing self.time_array. Should be [], instead of " + str(statusbar.time_array)
    assert abs(statusbar.start_time - current_time)<1e-3, \
        "Error initializing self.start_time. Should be " + str(current_time) + ", instead of " + str(statusbar.start_time)
    assert statusbar.time_left == "--", \
        "Error initializing self.time_array. Should be '--', instead of " + str(statusbar.time_left)

    del(statusbar,current_time)

def test_dsb_automatic_reset():
    statusbar = dsb()
    for i in range(10):
        time.sleep(0.1)
        statusbar.update(i,10)
    statusbar.update(0,10)
    current_time = time.time()
    test_bar_indices = [0,1,2,3,4,5,6,7,8,9,10]

    assert hasattr(statusbar,'bar_indices'), "self.bar_indices not initialized for statusbar.update(...) when statusbar.counter == 0."
    assert hasattr(statusbar,'counter'), "self.counter not initialized for dsb()"
    assert hasattr(statusbar,'time_array'), "self.time_array not initialized for dsb()"
    assert hasattr(statusbar,'start_time'), "self.start_time not initialized for dsb()"
    assert hasattr(statusbar,'time_left'), "self.time_left not initialized for dsb()"

    assert statusbar.bar_indices == test_bar_indices, "Error resetting dsb(). bar_indices should be [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], not " + str(statusbar.bar_indices)
    assert statusbar.counter == 1, \
        "Error initializing self.counter for dsb(). Should be 1, instead of " + str(statusbar.counter) + " as the statusbar.update(...) added one to the count."
    assert statusbar.time_array == [], \
        "Error initializing self.time_array. Should be [], instead of " + str(statusbar.time_array)
    assert abs(statusbar.start_time - current_time)<1e-3, \
        "Error initializing self.start_time. Should be " + str(current_time) + ", instead of " + str(statusbar.start_time)
    assert statusbar.time_left == "--", \
        "Error initializing self.time_array. Should be '--', instead of " + str(statusbar.time_left)

    del(statusbar,current_time,test_bar_indices)

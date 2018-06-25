import pytest
from .sb import *

def test_double_input():
  output = double_input(2)
  assert output == 4, "Error with double_input."

  from unittest.mock import patch, call

@patch('builtins.print')
def test_print_input(mocked_print):
  test_input('This is a test.')
  assert mocked_print.mock_calls == [call('This is a test.')]

import pytest
import dsb

def test_double_input():
  output = dsb.double_input(2)
  assert output == 4, "Error with double_input."
  
  

# Collection of useful python functions/features.
Prepared by: Daniel A Hagen  
[![Build Status](https://travis-ci.com/danhagen/danpy.svg?branch=master)](https://travis-ci.com/danhagen/danpy)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Coverage Status](https://coveralls.io/repos/github/danhagen/danpy/badge.svg?branch=master)](https://coveralls.io/github/danhagen/danpy?branch=master)

## Installation
```py
pip install danpy
```

## Installation from GitHub
```bash
git clone https://github.com/danhagen/danpy.git && cd danpy
pip install -r requirements.txt
pip install .
```


## Statusbar for Python `for/while` loops with `danpy.sb`
This helpful statusbar can be used with `for/while` loops to keep track of how much time has elapsed as well as how much time remains. Simply place inside the loop (after initializing the statusbar -- `dsb`) and `update` with the current timestep (i). A `title` can be added to the statusbar to keep track of individual function/loops and it is recommended that any function that runs a loop uses `arbitrary_function_name.__name__` to automatically assign an appropriate title. 

### Initialize statusbar before running a for/while loop.
```py
from danpy.sb import *
from time import sleep

statusbar = dsb()
number_of_loops = 10
for i in range(number_of_loops):
  sleep(0.5)
  statusbar.update(i,number_of_loops,title="Test Loop")
```
It is useful to either `reset` the statusbar instance. However, loops run in succession will automatically reset if the loops are of the same size.

```py
from danpy.sb import *
from time import sleep

statusbar = dsb()
number_of_inside_loops = 10
number_of_outside_loops = 3
for j in range(number_of_outside_loops):
  for i in range(number_of_inside_loops):
    sleep(0.5)
    statusbar.update(i,number_of_inside_loops,title="Testing Loop-D-Loops")

number_of_additional_loops = 10
for i in range(number_of_additional_loops):
  sleep(0.5)
  statusbar.update(i,number_of_additional_loops,title="Test Another Loop")
```

### Resetting Statusbar
```py
from danpy.sb import *
from time import sleep

statusbar = dsb()
number_of_loops = 10
for i in range(number_of_loops):
  sleep(0.5)
  statusbar.update(i,number_of_loops,title="Testing One Loop")

statusbar.reset()
a_different_number_of_loops = 20
for i in range(a_different_number_of_loops):
  sleep(0.5)
  statusbar.update(i,a_different_number_of_loops,title="Test A Different Loop")
```

### Using `while` Loops
If using a `while` loop, the statusbar will still update, but depending on the nature of the code in the loop, the extrapolation to determine time remaining may be off.

```py
from danpy.sb import *
from time import sleep

statusbar = dsb()
count = 0
number_of_loops = 10
while count<=number_of_loops:
  sleep(0.5)
  statusbar.update(count,number_of_loops,Title="Testing One Loop")
  count+=1
```

Only compatible with while loops that utilize a `count` metric where the loop continues while `count<number_of_loops`. The "<" ensures that the statusbar terminates at 100%. If you use "<=" then the input to the statusbar will be `statusbar.update(i,number_of_loops+1,**kwargs)`.

# Collection of useful python functions/features.
Prepared by: Daniel A Hagen  
[![Build Status](https://travis-ci.com/danhagen/danpy.svg?branch=master)](https://travis-ci.com/danhagen/danpy)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Coverage Status](https://coveralls.io/repos/github/danhagen/danpy/badge.svg?branch=master&service=github)](https://coveralls.io/github/danhagen/danpy?branch=master&service=github)

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
This helpful statusbar can be used with `for/while` loops to keep track of how much time has elapsed as well as how much time remains. Simply place inside the loop (after initializing the statusbar -- `dsb` -- with `final_value`) and `update` with the current timestep (i). A `title` can be added to the statusbar to keep track of individual function/loops and it is recommended that any function that runs a loop uses `arbitrary_function_name.__name__` to automatically assign an appropriate title. The `initial_value` can also be initialized or left at default (0).

### Initialize statusbar before running a for/while loop.
```py
from danpy.sb import *
from time import sleep

initial_value = 0
final_value = 10
statusbar = dsb(initial_value,final_value,title='a Loop')
for i in range(final_value):
  sleep(0.5)
  statusbar.update(i)
```

It is useful to either `reset` the statusbar instance. However, loops run in succession will automatically reset if the loops are of the same size.

```py
from danpy.sb import *
from time import sleep

initial_value = 0
final_value = 10
number_of_outside_loops = 3
statusbar = dsb(initial_value,final_value,title="Loop-D-Loops")
for j in range(number_of_outside_loops):
  for i in range(final_value):
    sleep(0.5)
    statusbar.update(i)
```
It is also possible to rename loops when they are run in succession by using the updating `title`.

```py
from danpy.sb import *
from time import sleep

initial_value = 0
final_value = 10
statusbar = dsb(initial_value,final_value,title="a Loop")
for i in range(final_value):
  sleep(0.5)
  statusbar.update(i)

for i in range(final_value):
  sleep(0.5)
  statusbar.update(i,title="a Different Loop")
```

However, these automatic reset features will only work if the length of each loop is the same *and* they have the same starting value. If you wish to run consecutive loops with *different* starting values or loop lengths, then you can `reset` the statusbar. It should be noted that the automatic reset, although convenient, will initialize the `start_time` after the first iteration of the loop. Therefore it is not the most accurate representation of runtime. We recommend a hard reset between trials or a redefinition of the statusbar before each loop.

### Resetting Statusbar

A statusbar can be reset by calling the builtin function `reset` one of two way; `reset()` will return a statusbar with the previously used `initial_value`, `final_value`, and `title`, or `reset(**kwargs)` can manually reset any of those values (while the others are kept as previously define).

```py
from danpy.sb import *
from time import sleep

initial_value = 0
final_value = 10
statusbar = dsb(initial_value,final_value,title='One Loop')
for i in range(final_value):
  sleep(0.5)
  statusbar.update(i)

a_different_final_value = 1010
a_different_initial_value = 1000
statusbar.reset(
  initial_value=a_different_initial_value,
  final_value=a_different_final_value,
  title="Another Loop")
for i in range(a_different_initial_value,a_different_final_value):
  sleep(0.5)
  statusbar.update(i)
```

### Using `while` Loops
If using a `while` loop, the statusbar will still update, but depending on the nature of the code in the loop, the extrapolation to determine time remaining may be off.

```py
from danpy.sb import *
from time import sleep

count = 0
final_count = 10
statusbar = dsb(count,final_count,title="a while Loop")
while count<final_count:
  sleep(0.5)
  statusbar.update(count)
  count+=1
```

Only compatible with while loops that utilize a `count` metric where the loop continues while `count<final_value`. The "<" ensures that the statusbar terminates at 100%. If you use "<=" then the input to the statusbar will be `statusbar.update(i,final_value+1,**kwargs)`.

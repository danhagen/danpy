# Statusbar for Python `for/while` loops
Prepared by: Daniel A Hagen  
[![Build Status](https://travis-ci.com/danhagen/dsb.svg?branch=master)](https://travis-ci.com/danhagen/dsb)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Coverage Status](https://coveralls.io/repos/github/danhagen/dsb/badge.svg?branch=master)](https://coveralls.io/github/danhagen/dsb?branch=master)
# Installation
```py
pip install dsb
```

# Installation from GitHub
```bash
git clone https://github.com/danhagen/dsb.git && cd dsb
pip install -r requirements.txt
pip install .
```

# Example usage:

### Initialize statusbar before running a for/while loop.
```py
from danpy_sb import *
from time import sleep

SB = dsb()
N_loops = 10
for i in range(N_loops):
  sleep(0.5)
  SB.statusbar(i,N_loops,Title="Test Loop")
```
It is useful to either reset the statusbar instance. However, loops run in succession will automatically reset if the loops are of the same size.

```py
from danpy_sb import *
from time import sleep

SB = dsb()
N_loops = 10
for j in range(3):
  for i in range(N_loops):
    sleep(0.5)
    SB.statusbar(i,N_loops,Title="Testing Loop-D-Loops")

for i in range(N_loops):
  sleep(0.5)
  SB.statusbar(i,N_loops,Title="Test Another Loop")
```

### Resetting Statusbar
```py
from danpy_sb import *
from time import sleep

SB = dsb()
N_loops = 10
for i in range(N_loops):
  sleep(0.5)
  SB.statusbar(i,N_loops,Title="Testing One Loop")

SB.reset_dsb()
N_loops = 20
for i in range(N_loops):
  sleep(0.5)
  SB.statusbar(i,N_loops,Title="Test A Different Loop")
```

### Using `while` Loops

If using a `while` loop, the statusbar will still update, but depending on the nature of the code in the loop, the extrapolation to determine time remaining may be off.

```py
from danpy_sb import *
from time import sleep

SB = dsb()
count = 0
N_loops = 10
while count<=N_loops:
  sleep(0.5)
  SB.statusbar(count,N_loops,Title="Testing One Loop")
  count+=1
```

Only compatible with while loops that utilize a `count` metric where the loop continues while `count<N_loops`. The "<" ensures that the statusbar terminates at 100%. If you use "<=" then the input to the statusbar will be `SB.statusbar(i,N_loops+1,**kwargs)`.

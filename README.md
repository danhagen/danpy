<h1 align="center">DanPy</h1>
<h2 align="center">A Collection of Useful Python Functions/Features</h2>
<h3 align="center">Written by: Daniel A Hagen</h3>
<p align="center">
  <img src="https://travis-ci.com/danhagen/danpy.svg?branch=master" alt="Build Status">
  <img src="https://img.shields.io/badge/code%20style-pep8-green.svg" alt="PEP8">
  <img src="https://coveralls.io/repos/github/danhagen/danpy/badge.svg?branch=master&service=github" alt="Coverage Status">
</p>

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
This helpful statusbar can be used with `for/while` loops to keep track of how much time has elapsed as well as how much time remains. Simply place inside the loop (after initializing the statusbar -- `dsb` -- with `finalValue`) and `update` with the current timestep (i). A `title` can be added to the statusbar to keep track of individual function/loops and it is recommended that any function that runs a loop uses `arbitrary_function_name.__name__` to automatically assign an appropriate title. The `initialValue` can also be initialized or left at default (0).

### Initialize statusbar before running a for/while loop.
```py
from danpy.sb import *
from time import sleep

initialValue = 0
finalValue = 10
statusbar = dsb(initialValue,finalValue,title='a Loop')
for i in range(finalValue):
  sleep(0.5)
  statusbar.update(i)
```

It is useful to either `reset` the statusbar instance. However, loops run in succession will automatically reset if the loops are of the same size.

```py
from danpy.sb import *
from time import sleep

initialValue = 0
finalValue = 10
numberOfOutsideLoops = 3
statusbar = dsb(initialValue,finalValue,title="Loop-D-Loops")
for j in range(numberOfOutsideLoops):
  for i in range(finalValue):
    sleep(0.5)
    statusbar.update(i)
```
It is also possible to rename loops when they are run in succession by using the updating `title`.

```py
from danpy.sb import *
from time import sleep

initialValue = 0
finalValue = 10
statusbar = dsb(initialValue,finalValue,title="a Loop")
for i in range(finalValue):
  sleep(0.5)
  statusbar.update(i)

for i in range(finalValue):
  sleep(0.5)
  statusbar.update(i,title="a Different Loop")
```

However, these automatic reset features will only work if the length of each loop is the same *and* they have the same starting value. If you wish to run consecutive loops with *different* starting values or loop lengths, then you can `reset` the statusbar. It should be noted that the automatic reset, although convenient, will initialize the `start_time` after the first iteration of the loop. Therefore it is not the most accurate representation of runtime. We recommend a hard reset between trials or a redefinition of the statusbar before each loop.

### Resetting Statusbar

A statusbar can be reset by calling the builtin function `reset` one of two way; `reset()` will return a statusbar with the previously used `initialValue`, `finalValue`, and `title`, or `reset(**kwargs)` can manually reset any of those values (while the others are kept as previously define).

```py
from danpy.sb import *
from time import sleep

initialValue = 0
finalValue = 10
statusbar = dsb(initialValue,finalValue,title='One Loop')
for i in range(finalValue):
  sleep(0.5)
  statusbar.update(i)

aDifferentFinalValue = 1010
aDifferentInitialValue = 1000
statusbar.reset(
  initialValue=aDifferentInitialValue,
  finalValue=aDifferentFinalValue,
  title="Another Loop")
for i in range(aDifferentInitialValue,aDifferentFinalValue):
  sleep(0.5)
  statusbar.update(i)
```

### Using `while` Loops
If using a `while` loop, the statusbar will still update, but depending on the nature of the code in the loop, the extrapolation to determine time remaining may be off.

```py
from danpy.sb import *
from time import sleep

count = 0
finalCount = 10
statusbar = dsb(count,finalCount,title="a while Loop")
while count<finalCount:
  sleep(0.5)
  statusbar.update(count)
  count+=1
```

Only compatible with while loops that utilize a `count` metric where the loop continues while `count<finalValue`. The "<" ensures that the statusbar terminates at 100%. If you use "<=" then the input to the statusbar will be `statusbar.update(i,finalValue+1,**kwargs)`.

## Useful Functions for Python with `danpy.useful_functions`
Included in this package are the functions `is_number` and `save_figures`.

### Simple function to save all current figures.
The function `save_figures` is designed to save all currently open figures (or a prescribed subset of them) to a convenient location for easy storing, viewing, and comparison.
I find that this works best if you create a "figures/" destination folder first so that your figures automatically get organized in a location other than location of your project's source code.

In order to save your figures, you must specify the `destination` of the figures (`str`, in this case, "figures/"), the `baseFileName` (`str`, which can be used to further describe the figures), and a dictionary of the parameters (`params`:`dict`) used to create these plots.
This last argument is a little different and can left blank (i.e., `{}`) if desired, but I find this to be incredibly useful when you need to compare parameters across trials.
This will also be used to create a `notes.txt` (or `README.md`; see below) file that allows for quick reference of the used parameters. As an example, try:

```py
from danpy.useful_functions import save_figures
import matplotlib.pyplot as plt
import numpy as np

dt = 0.01
signalAmplitude = 1
signalFrequency = 0.5 # Hz
durationOfSignal = 10 # seconds

params = {
  "Time Step" : dt,
  "Signal Amplitude" : signalAmplitude,
  "Signal Frequency" : signalFrequency,
  "Duration Of Signal" : durationOfSignal
}

time = np.arange(0,durationOfSignal+dt,dt)
signal1 = signalAmplitude*np.sin(2*np.pi*signalFrequency*time)
signal2 = signalAmplitude*np.cos(2*np.pi*signalFrequency*time)

fig1 = plt.figure()
ax1 = plt.gca()
ax1.plot(time,signal1)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Signal 1")

fig2 = plt.figure()
ax2 = plt.gca()
ax2.plot(time,signal2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Signal 2")

save_figures(
  "figures/",
  "Signal_figures",
  params
)

plt.show()
```

This code will create a subfolder in "figures/" that is time stamped that contains three files (`Signal_figures_01-01.png`,`Signal_figures_01-02.png`, and `notes.txt`). The first two files have the base file name `Signal_figures` followed by the number 01 (which corresponds to the trial number) and then the figure number. This can be useful when you wish to add figures to the _same_ subfolder, when the parameters don't change (but more on that later).

The notes will appear as such,

```
[Created 2020/01/03 at 09:28.42]

##############################
########### Notes ############
##############################

		NONE

##############################
######### Parameters #########
##############################

		Time Step: 0.01
		Signal Amplitude: 1
		Signal Frequency: 0.5
		Duration Of Signal: 10

##############################
```

Note that all of the parameters have been listed conveniently as well as the date and time that the file was generated. You can also add your own notes to further categorize your results with the `addNotes` kwarg.

Additionally, you can set the kwarg `saveAsMD` as `True` (default is `False`) to create a Github-flavored markdown version of this `notes.txt` files, which will be saved as a `README.md` file to allow for seamless viewing.
If these figures are to be pushed to your project repository, simply navigate to the `figures/` folder and the corresponding subfolder and your results will be automatically presented on the Github subfolder page thanks to the magic of Github-flavored markdown.
I prefer this option as it will also automatically add HTML figure blocks with all of the figures in the corresponding subfolder. As an example, see the screen grab of the `README.md` file created for the above code when `saveAsMD=True`.

<p align="center">
	<img width="500" src="https://user-images.githubusercontent.com/16945786/91619078-f4a73900-e940-11ea-87f4-c61f30ee2c6d.png">
</p>

These README files can be edited directly as well to include things like figure captions.

For either option, if you wish to run an additional trial and have those results saved in the same folder you can specify the `subFolderName` to the previously generated subfolder and (1) the figures will be saved there with the number identifier changed (generally, plus 1) to denote a new trial and (2) the `notes.txt` or `README.md` file will be _appended_ to include the new information.

To do this, you will also want to recover the path to the previous subfolder. To do this, use the kwarg `returnPath=True` in the first `save_figures` instance which will return the `Path` (from `pathlib` package) of the folder, which we will designate as `figPath`.
Then use the kwarg `subFolderName=figPath.stem`.

```py
from danpy.useful_functions import save_figures
import matplotlib.pyplot as plt
import numpy as np

dt = 0.01
signalAmplitude = 1
signalFrequency = 0.5 # Hz
durationOfSignal = 10 # seconds

params = {
  "Time Step" : dt,
  "Signal Amplitude" : signalAmplitude,
  "Signal Frequency" : signalFrequency,
  "Duration Of Signal" : durationOfSignal
}

time = np.arange(0,durationOfSignal+dt,dt)
signal1 = signalAmplitude*np.sin(2*np.pi*signalFrequency*time)
signal2 = signalAmplitude*np.cos(2*np.pi*signalFrequency*time)

fig1 = plt.figure()
ax1 = plt.gca()
ax1.plot(time,signal1)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Signal 1")

fig2 = plt.figure()
ax2 = plt.gca()
ax2.plot(time,signal2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Signal 2")

# save first set of figures
figPath = save_figures(
  "figures/",
  "Signal_figures",
  params,
  returnPath=True
)

plt.close('all')

fig3 = plt.figure()
ax1 = plt.gca()
ax1.plot(time,signal1+signal2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Signal 1 + Signal 2")

fig4 = plt.figure()
ax2 = plt.gca()
ax2.plot(time,signal1-signal2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Signal 1 - Signal 2")

# save next set of figures
save_figures(
  "figures/",
  "Signal_figures",
  params,
  subFolderName=figPath.stem
)

plt.show()
```

### `kwargs` for `save_figures`
There are multiple ways to adjust the behavior of this function with `kwargs`. Specifically,

  * `fileType` (default is "png") - You can change the file extension to any of the following: "eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz". Note that saving them as "pdf" will save each figure individually, where the `kwargs` `saveAsPDF` will combine them into a single file.
  * `subFolderName` (default is the time stamped folder name) - Sometimes it is more convenient to name the subfolder yourself **or** to send files to a previously defined location. In this case, just specify the `subFolderName` and it will send the figures there. Note that this should only be done for trials where the parameters *do not change* as the `notes.txt` files is only generated when the subfolder is created.
  * `addNotes` (default `None`) - This will allow for notes to be added to the `notes.txt` or `README.md` files directly from the function call. Must be a `str`.
  * `saveAsMD` (default `False`) - If true, the notes will be saved in Github-flavored markdown which includes figure displays in addition to notes and parameters. This can be viewed directly from the figure folder once uploaded to your projects repository or locally with a markdown previewer (like Atom).
  * `saveAsPDF` (default `False`) - If true, in addition to saving the figures as the specified filetype, a single PDF will be constructed to include all figures generated.
  * `returnPath` (default `False`) - If you intend on saving additional figures to the folder location, this option allows you to return the path of the subfolder. Use this for the first trial and the `subFolderName` argument for any additional trials to send new figures to the same location. Note that this returns a `Path` item from the `pathlib` package, which means that the subfolder name can be recovered by the command `<figure subfolder path>.stem`
  * `figs` (default will save every figure open) - You can alternatively specify the specific figures that you wish to save. This should be a list of figures.

### Simple `timer` class that allows you to keep track of function run/loop times.

This class creates a timer that allows you to keep track of how long loops take to run. This can be particularly helpful if you are running many large loops with irregular run times and you want to keep track of how long your code has been running.

To use this class, simply instantiate it with `myTimer = timer()` and then print updates after each loop with a variety of commands depending on what you are doing.

As an example consider the code snippet below

```py
from danpy.useful_functions import timer
import time

myTimer = timer()

myTimer.start()
for i in range(5):
    print("Trial " + str(i+1) + "\n")
    time.sleep(5)
    myTimer.loop()
```

Which prints the following output.

```console
Trial 1

Total Run Time: 00:00:05 (00:00:05)

Trial 2

Total Run Time: 00:00:10 (00:00:05)

Trial 3

Total Run Time: 00:00:15 (00:00:05)

Trial 4

Total Run Time: 00:00:20 (00:00:05)

Trial 5

Total Run Time: 00:00:25 (00:00:05)
```

Alternatively, you can choose to only print the total run time of your code by starting the timer at the beginning and then ending it at the bottom of your code with the command `myTimer.end()`, which will print the total run time as well. If this is the case, you can select the arg `--single_trial` when the timer is initialized and the displays will adjust to only display the total run time (i.e., `myTimer = timer('--single_trial')`). Note, however, that you cannot use the `loop` function in single trial mode.

If instead you wish to display or save the run time, the output of these functions can be suppressed by the kwarg `verbose=0`. The value of the `totalRunTime` can then be recovered as an attribute of the timer (i.e., `myTimer.totalRunTime`). Similarly, the trial run time can always be recovered by the attribute `trialRunTime`. And lastly, the formated `str` version of these values can be recovered by the attributes `totalRunTimeStr` and `trailRunTimeStr`, respectively.

You can always reset your timer with the function `reset` as well, in case you ever needed to run back to back timers (but be sure to use `--single_trial` again if you want to continue using that option).

```py
from danpy.useful_functions import timer
import time

myTimer = timer()

print("First Timer\n")
myTimer.start()
for i in range(5):
    print("Trial " + str(i+1) + "\n")
    time.sleep(5)
    myTimer.loop()

print("Second Timer\n")
myTimer.reset()
for i in range(5):
    print("Trial " + str(i+1) + "\n")
    time.sleep(5)
    myTimer.loop()
```

### Simple test function for asserting a variable is, in fact, a number.
In order to quickly test if a variable is a number (and not a `str` or `bool`), simply type `is_number(variable,variableName)` as such:

```py
from danpy.useful_function import is_number

myVariable = 3.1415926536
is_number(myVariable,"myVariable")
```

This will not raise an AssertionError as `myVariable` is a number. To make the debugging easier to locate, the additional arguments `default` and `notes` have been added.

```py
from danpy.useful_functions import is_number

myVariable = "Not a number"
defaultValue = 3.1415926536
notes = "This is where I would put notes pertaining to the variable like relative magnitude, units, etc."

is_number(myVariable,"myVariable",
default=defaultValue,
notes=notes
)
```

which will raise the `AssertionError`:

```console
AssertionError: myVariable must be an int, float, float32, float64, or numpy.float not <class 'str'>. Default is 3.1415926536. This is where I would put notes pertaining to the variable like relative magnitude, units, etc.
```

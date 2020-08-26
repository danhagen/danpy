import pytest
import time
from datetime import datetime
from unittest.mock import patch, call
import os
import subprocess
from .sb import *
from .useful_functions import *

def test_dsb__init__default():
    initialValue = 0
    finalValue = 10
    usedSpace = len(
        'XXXX.X' + '% Complete, ' + 'XXXXX.X '
        + ' sec, (est. ' + "XXXXX.X" + ' sec left)')
    statusbar = dsb(initialValue,finalValue)
    currentTime = time.time()

    assert hasattr(statusbar,'timeArray'), "self.timeArray not initialized for dsb()"
    assert hasattr(statusbar,'startTime'), "self.startTime not initialized for dsb()"
    assert hasattr(statusbar,'timeRemaining'), "self.timeRemaining not initialized for dsb()"
    assert hasattr(statusbar,'terminalWidth'), "self.terminalWidth not initialized for dsb()"
    assert hasattr(statusbar,'statusbarWidth'), "self.statusbarWidth not initialized for dsb()"
    assert hasattr(statusbar,'title'), "self.title not initialized for dsb()"
    assert hasattr(statusbar,'initialValue'), "self.initialValue not initialized for dsb()"
    assert hasattr(statusbar,'finalValue'), "self.finalValue not initialized for dsb()"

    assert statusbar.timeArray == [], \
        "Error initializing self.timeArray. Should be [], instead of " + str(statusbar.timeArray)
    assert abs(statusbar.startTime - currentTime)<1e-4, \
        "Error initializing self.startTime. Should be " + str(currentTime) + ", instead of " + str(statusbar.startTime)
    assert statusbar.timeRemaining == "--", \
        "Error initializing self.timeArray. Should be '--', instead of " + str(statusbar.timeRemaining)
    assert statusbar.terminalWidth == 80, \
        ("Error initializing self.terminalWidth. Should be 80, instead of "
        + str(statusbar.terminalWidth))
    assert statusbar.statusbarWidth == 80-usedSpace-2, \
        ("Error initializing self.statusbarWidth. Should be "
        + str(80-usedSpace-2)
        + ", instead of "
        + str(statusbar.statusbarWidth))
    assert statusbar.title == "a Loop", \
        "Error initializing self.title. Should be 'a Loop', instead of " + str(statusbar.title)
    assert statusbar.initialValue == 0, \
        ("Error initializing self.initialValue. Should be 0, instead of "
        + str(statusbar.initialValue))
    assert statusbar.finalValue == finalValue, \
        ("Error initializing self.finalValue. Should be "
        + str(finalValue)
        + ", instead of "
        + str(statusbar.finalValue))

    del(statusbar,
        currentTime,
        initialValue,
        finalValue,
        usedSpace)

def test_dsb__init__kwargs():
    initialValue = 0
    finalValue = 10
    title = "Test"
    usedSpace = len(
        'XXXX.X' + '% Complete, ' + 'XXXXX.X '
        + ' sec, (est. ' + "XXXXX.X" + ' sec left)')
    statusbar = dsb(initialValue,finalValue,title=title)
    currentTime = time.time()

    assert hasattr(statusbar,'timeArray'), "self.timeArray not initialized for dsb()"
    assert hasattr(statusbar,'startTime'), "self.startTime not initialized for dsb()"
    assert hasattr(statusbar,'timeRemaining'), "self.timeRemaining not initialized for dsb()"
    assert hasattr(statusbar,'terminalWidth'), "self.terminalWidth not initialized for dsb()"
    assert hasattr(statusbar,'statusbarWidth'), "self.statusbarWidth not initialized for dsb()"
    assert hasattr(statusbar,'title'), "self.title not initialized for dsb()"
    assert hasattr(statusbar,'initialValue'), "self.initialValue not initialized for dsb()"
    assert hasattr(statusbar,'finalValue'), "self.finalValue not initialized for dsb()"

    assert statusbar.timeArray == [], \
        "Error initializing self.timeArray. Should be [], instead of " + str(statusbar.timeArray)
    assert abs(statusbar.startTime - currentTime)<1e-4, \
        "Error initializing self.startTime. Should be " + str(currentTime) + ", instead of " + str(statusbar.startTime)
    assert statusbar.timeRemaining == "--", \
        "Error initializing self.timeArray. Should be '--', instead of " + str(statusbar.timeRemaining)
    assert statusbar.terminalWidth == 80, \
        ("Error initializing self.terminalWidth. Should be 80, instead of "
        + str(statusbar.terminalWidth))
    assert statusbar.statusbarWidth == 80-usedSpace-2, \
        ("Error initializing self.statusbarWidth. Should be "
        + str(80-usedSpace-2)
        + ", instead of "
        + str(statusbar.statusbarWidth))
    assert statusbar.title == title, \
        ("Error initializing self.title. Should be "
        + title
        + ", instead of "
        + str(statusbar.title))
    assert statusbar.initialValue == initialValue, \
        ("Error initializing self.initialValue. Should be "
        + str(initialValue)
        + ", instead of "
        + str(statusbar.initialValue))
    assert statusbar.finalValue == finalValue, \
        ("Error initializing self.finalValue. Should be "
        + str(finalValue)
        + ", instead of "
        + str(statusbar.finalValue))

    del(statusbar,
        currentTime,
        finalValue,
        usedSpace,
        initialValue,
        title)

def test_get_terminal_width():
    assert get_terminal_width() == 80, "Error with get_terminal_width(). Should be 80 (default pytest terminal size), instead of " + str(get_terminal_width())
    assert int(subprocess.check_output(["tput","cols"])) == 80, "Error with get_terminal_width() ImportError mode. The value of int(subprocess.check_output(['tput','cols'])) should be 80 (default pytest terminal size), instead of " + str(int(subprocess.check_output(["tput","cols"])))

def test_dsb_reset_default():
    initialValue = 0
    finalValue = 10
    statusbar = dsb(initialValue,finalValue)
    for i in range(finalValue):
        time.sleep(0.1)
        statusbar.update(i)
    statusbar.reset()
    currentTime = time.time()

    assert not hasattr(statusbar,"barIndices"), "Error resetting dsb(). barIndices should not exist."

    assert hasattr(statusbar,'timeArray'), "self.timeArray not initialized for dsb()"
    assert hasattr(statusbar,'startTime'), "self.startTime not initialized for dsb()"
    assert hasattr(statusbar,'timeRemaining'), "self.timeRemaining not initialized for dsb()"
    assert hasattr(statusbar,'terminalWidth'), "self.terminalWidth not initialized for dsb()"
    assert hasattr(statusbar,'statusbarWidth'), "self.statusbarWidth not initialized for dsb()"
    assert hasattr(statusbar,'title'), "self.title not initialized for dsb()"
    assert hasattr(statusbar,'initialValue'), "self.initialValue not initialized for dsb()"
    assert hasattr(statusbar,'finalValue'), "self.finalValue not initialized for dsb()"

    assert statusbar.timeArray == [], \
        "Error initializing self.timeArray. Should be [], instead of " + str(statusbar.timeArray)
    assert abs(statusbar.startTime - currentTime)<1e-4, \
        "Error initializing self.startTime. Should be " + str(currentTime) + ", instead of " + str(statusbar.startTime)
    assert statusbar.timeRemaining == "--", \
        "Error initializing self.timeArray. Should be '--', instead of " + str(statusbar.timeRemaining)
    assert statusbar.title == "a Loop", \
        "Error initializing self.title. Default should be 'a Loop', instead of " + str(statusbar.title)
    assert statusbar.initialValue == 0, \
        ("Error initializing self.initialValue. Should be 0, instead of "
        + str(statusbar.initialValue))
    assert statusbar.finalValue == finalValue, \
        ("Error initializing self.finalValue. Should be "
        + str(finalValue)
        + ", instead of "
        + str(statusbar.finalValue))

    del(statusbar,currentTime,initialValue,finalValue)

def test_dsb_reset_kwargs():
    initialValue = 0
    finalValue = 10
    aDifferentInitialValue = 5
    aDifferentFinalValue = 20
    aDifferentTitle = "Test"

    statusbar = dsb(initialValue,finalValue)
    for i in range(finalValue):
        time.sleep(0.1)
        statusbar.update(i)
    statusbar.reset(
        initialValue=aDifferentInitialValue,
        finalValue=aDifferentFinalValue,
        title=aDifferentTitle)
    currentTime = time.time()

    assert not hasattr(statusbar,"barIndices"), "Error resetting dsb(). barIndices should not exist."

    assert hasattr(statusbar,'timeArray'), "self.timeArray not initialized for dsb()"
    assert hasattr(statusbar,'startTime'), "self.startTime not initialized for dsb()"
    assert hasattr(statusbar,'timeRemaining'), "self.timeRemaining not initialized for dsb()"
    assert hasattr(statusbar,'terminalWidth'), "self.terminalWidth not initialized for dsb()"
    assert hasattr(statusbar,'statusbarWidth'), "self.statusbarWidth not initialized for dsb()"
    assert hasattr(statusbar,'title'), "self.title not initialized for dsb()"
    assert hasattr(statusbar,'initialValue'), "self.initialValue not initialized for dsb()"
    assert hasattr(statusbar,'finalValue'), "self.finalValue not initialized for dsb()"

    assert statusbar.timeArray == [], \
        "Error initializing self.timeArray. Should be [], instead of " + str(statusbar.timeArray)
    assert abs(statusbar.startTime - currentTime)<1e-4, \
        "Error initializing self.startTime. Should be " + str(currentTime) + ", instead of " + str(statusbar.startTime)
    assert statusbar.timeRemaining == "--", \
        "Error initializing self.timeArray. Should be '--', instead of " + str(statusbar.timeRemaining)
    assert statusbar.title == aDifferentTitle, \
        ("Error initializing self.title. Default should be "
        + aDifferentTitle
        +", instead of "
        + str(statusbar.title))
    assert statusbar.initialValue == aDifferentInitialValue, \
        ("Error initializing self.initialValue. Should be "
        + str(aDifferentInitialValue)
        + ", instead of "
        + str(statusbar.initialValue))
    assert statusbar.finalValue == aDifferentFinalValue, \
        ("Error initializing self.finalValue. Should be "
        + str(aDifferentFinalValue)
        + ", instead of "
        + str(statusbar.finalValue))

    del(statusbar,
        currentTime,
        initialValue,
        finalValue,
        aDifferentTitle,
        aDifferentInitialValue,
        aDifferentFinalValue)

def test_dsb_automatic_reset():
    initialValue = 0
    finalValue = 10
    statusbar = dsb(initialValue,finalValue)
    for i in range(finalValue):
        time.sleep(0.1)
        statusbar.update(i)
    statusbar.update(0)
    currentTime = time.time()
    testBarIndices = [0,1,2,3,4,5,6,7,8,9,10]

    assert hasattr(statusbar,'barIndices'), "self.barIndices not initialized for i == statusbar.initialValue."
    assert hasattr(statusbar,'timeArray'), "self.timeArray not initialized for dsb()"
    assert hasattr(statusbar,'startTime'), "self.startTime not initialized for dsb()"
    assert hasattr(statusbar,'timeRemaining'), "self.timeRemaining not initialized for dsb()"
    assert hasattr(statusbar,'terminalWidth'), "self.terminalWidth not initialized for dsb()"
    assert hasattr(statusbar,'statusbarWidth'), "self.statusbarWidth not initialized for dsb()"
    assert hasattr(statusbar,'title'), "self.title not initialized for dsb()"
    assert hasattr(statusbar,'initialValue'), "self.initialValue not initialized for dsb()"
    assert hasattr(statusbar,'finalValue'), "self.finalValue not initialized for dsb()"

    assert statusbar.barIndices == testBarIndices, "Error resetting dsb(). barIndices should be [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], not " + str(statusbar.barIndices)
    assert statusbar.timeArray == [], \
        "Error initializing self.timeArray. Should be [], instead of " + str(statusbar.timeArray)
    assert abs(statusbar.startTime - currentTime)<1e-2, \
        "Error initializing self.startTime. Should be " + str(currentTime) + ", instead of " + str(statusbar.startTime)
    assert statusbar.timeRemaining == "--", \
        "Error initializing self.timeArray. Should be '--', instead of " + str(statusbar.timeRemaining)
    assert statusbar.title == "a Loop", \
        "Error initializing self.title. Default should be 'a Loop', instead of " + str(statusbar.title)
    assert statusbar.initialValue == 0, \
        ("Error initializing self.initialValue. Should be 0, instead of "
        + str(statusbar.initialValue))
    assert statusbar.finalValue == finalValue, \
        ("Error initializing self.finalValue. Should be "
        + str(finalValue)
        + ", instead of "
        + str(statusbar.finalValue))
    del(statusbar,
        currentTime,
        initialValue,
        finalValue,
        testBarIndices)

def test_is_number():
    goodVariableValue = 1111
    poorVariableValue = "Not a number"
    goodVariableName = "variableName"
    poorVariableName = 1111
    goodDefault = 1

    poorDefault = "Not a number"
    poorNotes = 1111

    ### test is_number with Good inputs and no **kwargs ###
    try:
        is_number(goodVariableValue,goodVariableName)
        success = True
    except AssertionError:
        success = False

    assert success==True, is_number.__name__ + " failed with good inputs and default kwargs."

    ### test if x is a number ###
    try:
        is_number(poorVariableValue,goodVariableName)
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, is_number.__name__ + " failed when testing if x was a number."

    ### test if x is a number when default is not None###
    try:
        is_number(poorVariableValue,goodVariableName,default=goodDefault)
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, is_number.__name__ + " failed when testing if x was a number."

    ### test if VarName is a str ###
    try:
        is_number(goodVariableValue,poorVariableName)
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, is_number.__name__ + " failed when testing if VarName is a str."

    ### test if default is a number ###
    try:
        is_number(goodVariableValue,goodVariableName,default=poorDefault)
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, is_number.__name__ + " failed when testing if default (kwargs) is a number."

    ### test if notes is a str ###
    try:
        is_number(goodVariableValue,goodVariableName,notes=poorNotes)
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, is_number.__name__ + " failed when testing if notes (kwargs) is a str."

def test_save_figures():
    goodFileType = "png"
    poorFileType1 = "jpg"
    poorFileType2 = 1111

    goodDestination = "goodDestination"
    os.mkdir(goodDestination)
    poorDestination1 = 1111
    poorDestination2 = "not a Directory"

    goodSubFolderName = "goodSubFolderName"
    poorSubFolderName = 1111

    goodBaseFileName = "goodBaseFileName"
    poorBaseFileName = 1111

    goodParams = {"Good Params" : True}
    poorParams = 1111

    goodSaveAsPDF = True
    poorSaveAsPDF = "Not a good SaveAsPDF"

    ### test if destination is a str ###
    try:
        save_figures(
            poorDestination1,
            goodBaseFileName,
            goodParams
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if destination is a str."

    ### test if destination is a directory ###
    try:
        save_figures(
            poorDestination2,
            goodBaseFileName,
            goodParams
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if destination is a str."

    ### test if subFolderName is a str ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            subFolderName = poorSubFolderName
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if subFolderName is a str."

    ### test if params is a dict ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            poorParams,
        )
        errorCaught = False
    except AttributeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if params is a dict."

    ### test if fileType is a proper file type ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            fileType=poorFileType1
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if fileType is one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz"

    ### test if fileType is a str ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            fileType=poorFileType2
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if fileType is a str."

    ### test if subFolderName is a str ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            subFolderName=poorSubFolderName
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if subFolderName is a str."

    ### test if saveAsPDF is a bool ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            saveAsPDF = poorSaveAsPDF
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if saveAsPDF is a bool."

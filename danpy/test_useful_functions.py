import pytest
from datetime import datetime
from unittest.mock import patch, call
import os
import subprocess
from .useful_functions import *
#TODO: tests for markdown saving
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
    poorDestination = 1111

    goodSubFolderName = "goodSubFolderName"
    poorSubFolderName = 1111

    goodBaseFileName = "goodBaseFileName"
    poorBaseFileName = 1111

    goodParams = {"Good Params" : True}
    poorParams = 1111

    goodSaveAsPDF = True
    poorSaveAsPDF = "Not a good SaveAsPDF"

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

    ### test if destination is a str ###
    try:
        save_figures(
            poorDestination,
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

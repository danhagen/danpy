import pytest
import time
from unittest.mock import patch, call
import os
import subprocess
from .useful_functions import *

def test_is_number():
    goodVariableValue = 1111
    poorVariableValue = "Not a number"
    goodVariableName = "variableName"
    poorVariableName = 1111

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
    goodDestination = "goodDestination/"
    poorDestination_1 = 1111
    poorDestination_2 = "Not a good destination"

    goodSubFolderName = "goodSubFolderName/"
    poorSubFolderName_1 = 1111
    poorSubFolderName_2 = "Not a good subFolderName"

    goodBaseFileName = "goodBaseFileName"
    poorBaseFileName = 1111

    goodParams = {"Good Params" : True}
    poorParams = 1111

    goodSaveAsPDF = True
    poorSaveAsPDF = "Not a good SaveAsPDF"

    ### test if destination is a str ###
    try:
        save_figures(
            poorDestination_1,
            goodBaseFileName,
            goodParams
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if destination is a str."

    ### test if destination ends in '/' ###
    try:
        save_figures(
            poorDestination_2,
            goodBaseFileName,
            goodParams
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if destination ends in '/'."

    ### test if subFolderName is a str ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            subFolderName = poorSubFolderName_1
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True
    except TypeError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if subFolderName is a str."

    ### test if subFolderName ends in '/' ###
    try:
        save_figures(
            goodDestination,
            goodBaseFileName,
            goodParams,
            subFolderName = poorSubFolderName_2
        )
        errorCaught = False
    except AssertionError:
        errorCaught = True

    assert errorCaught==True, save_figures.__name__ + " failed when testing if subFolderName ends in '/'."

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

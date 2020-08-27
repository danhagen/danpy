import pytest
from datetime import datetime
import unittest
import os
import subprocess
import shutil
from useful_functions import *

class Test_is_number(unittest.TestCase):
    def test_good_is_number(self):
        try:
            is_number(1,"a")
            is_number(1,"a",default=1)
            is_number(1,"a",notes="a")
        except AssertionError:
            self.fail("is_number() raised AssertionError unexpectedly!")
        except TypeError:
            self.fail("is_number() raised TypeError unexpectedly!")

    def test_bad_is_number(self):
        self.assertRaises(AssertionError,is_number,1,1) # poor variable name
        self.assertRaises(AssertionError,is_number,"a",1) # poor variable value
        self.assertRaises(AssertionError,is_number,"a",1,default=1) # poor variable value with nonNone default
        self.assertRaises(AssertionError,is_number,"a",1,default="a") # poor variable default
        self.assertRaises(AssertionError,is_number,"a",1,notes=1) # poor notes

    def test_good_save_figures(self):
        try:
            os.mkdir("test_dir_good")
            save_figures("test_dir_good","a",{"a":1})
            save_figures("test_dir_good","a",{"a":1},fileType="png") # good fileType
            _ = save_figures("test_dir_good","a",{"a":1},returnPath=True) # good saveAsMD
            save_figures("test_dir_good","a",{"a":1},subFolderName="a") # good subFolderName
            save_figures("test_dir_good","a",{"a":1},saveAsMD=True) # good saveAsMD
            save_figures("test_dir_good","a",{"a":1},addNotes="notes") # good addNotes
            save_figures("test_dir_good","a",{"a":1},saveAsPDF=True) # good saveAsMD
        except AssertionError:
            self.fail("save_figures() raised AssertionError unexpectedly!")
        except TypeError:
            self.fail("save_figures() raised TypeError unexpectedly!")

        figurePath = save_figures(
            "test_dir_good",'a',{"1":1},
            subFolderName='a',
            returnPath=True
        )
        assert figurePath==Path("test_dir_good/a"), "Error with returnPath."
        shutil.rmtree("test_dir_good")

    def test_bad_save_figures(self):
        self.assertRaises(TypeError,save_figures,
            1,"a",{"a":1}
        ) # poor destination (expected str)
        self.assertRaises(AssertionError,save_figures,
            "not a dir","a",{"a":1}
        ) # poor destination (not a dir)
        os.mkdir("test_dir_bad")
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad",1,{"a":1}
        ) # poor baseFileName (expected a str)
        self.assertRaises(AttributeError,save_figures,
            "test_dir_bad","a","not a dict"
        ) # poor params (expected a dict)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            fileType=1
        ) # poor fileType (expected a str)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            fileType="not an accepted type"
        ) # poor fileType (expected to be one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            subFolderName=1
        ) # poor subFolderName (expected a str)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            saveAsMD='not a bool'
        ) # poor saveAsMD (expected bool)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            addNotes=1
        ) # poor subFolderName (expected a str)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            saveAsPDF='not a bool'
        ) # poor saveAsPDF (expected bool)
        self.assertRaises(AssertionError,save_figures,
            "test_dir_bad","a",{"a":1},
            returnPath='not a bool'
        ) # poor returnPath (expected bool)
        shutil.rmtree("test_dir_bad")
#
# def test_is_number():
#     goodVariableValue = 1111
#     poorVariableValue = "Not a number"
#     goodVariableName = "variableName"
#     poorVariableName = 1111
#     goodDefault = 1
#
#     poorDefault = "Not a number"
#     poorNotes = 1111
#
#     ### test is_number with Good inputs and no **kwargs ###
#     try:
#         is_number(goodVariableValue,goodVariableName)
#         success = True
#     except AssertionError:
#         success = False
#
#     assert success==True, is_number.__name__ + " failed with good inputs and default kwargs."
#
#     ### test if x is a number ###
#     try:
#         is_number(poorVariableValue,goodVariableName)
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, is_number.__name__ + " failed when testing if x was a number."
#
#     ### test if x is a number when default is not None###
#     try:
#         is_number(poorVariableValue,goodVariableName,default=goodDefault)
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, is_number.__name__ + " failed when testing if x was a number."
#
#     ### test if VarName is a str ###
#     try:
#         is_number(goodVariableValue,poorVariableName)
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, is_number.__name__ + " failed when testing if VarName is a str."
#
#     ### test if default is a number ###
#     try:
#         is_number(goodVariableValue,goodVariableName,default=poorDefault)
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, is_number.__name__ + " failed when testing if default (kwargs) is a number."
#
#     ### test if notes is a str ###
#     try:
#         is_number(goodVariableValue,goodVariableName,notes=poorNotes)
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, is_number.__name__ + " failed when testing if notes (kwargs) is a str."

# def test_save_figures():
#     goodFileType = "png"
#     poorFileType1 = "jpg"
#     poorFileType2 = 1111
#
#     goodDestination = "goodDestination"
#     os.mkdir(goodDestination)
#     poorDestination1 = 1111
#     poorDestination2 = "not a Directory"
#
#     goodSubFolderName = "goodSubFolderName"
#     poorSubFolderName = 1111
#
#     goodBaseFileName = "goodBaseFileName"
#     poorBaseFileName = 1111
#
#     goodParams = {"Good Params" : True}
#     poorParams = 1111
#
#     goodSaveAsPDF = True
#     poorSaveAsPDF = "Not a good SaveAsPDF"
#
#     ### test successful defaults ###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==False, save_figures.__name__ + " failed when testing default good inputs."
#
#     ### test if destination is a str ###
#     try:
#         save_figures(
#             poorDestination1,
#             goodBaseFileName,
#             goodParams
#         )
#         errorCaught = False
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if destination is a str."
#
#     ### test if destination is a directory ###
#     try:
#         save_figures(
#             poorDestination2,
#             goodBaseFileName,
#             goodParams
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if destination is a dir and it exists."
#
#     ### test if baseFileName is a str ###
#     try:
#         save_figures(
#             goodDestination,
#             poorBaseFileName,
#             goodParams
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if baseFileName is a str."
#
#     ### test if params is a dict ###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             poorParams,
#         )
#         errorCaught = False
#     except AttributeError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if params is a dict."
#
#     ### test if subFolderName is a str (GOOD) ###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             subFolderName = goodSubFolderName
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==False, save_figures.__name__ + " failed when testing if subFolderName is a str."
#
#     ### test if subFolderName is a str (POOR)###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             subFolderName = poorSubFolderName
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if subFolderName is a str."
#
#     ### test if fileType is a proper file type (GOOD)###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             fileType=goodFileType
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==False, save_figures.__name__ + " failed when testing if fileType is one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz (GOOD)"
#
#     ### test if fileType is a proper file type (POOR)###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             fileType=poorFileType1
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if fileType is one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz (POOR)"
#
#     ### test if fileType is a str ###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             fileType=poorFileType2
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#     except TypeError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if fileType is a str. (POOR)"
#
#     ################################
#
#     ### test if saveAsPDF is a bool ###
#     try:
#         save_figures(
#             goodDestination,
#             goodBaseFileName,
#             goodParams,
#             saveAsPDF = poorSaveAsPDF
#         )
#         errorCaught = False
#     except AssertionError:
#         errorCaught = True
#
#     assert errorCaught==True, save_figures.__name__ + " failed when testing if saveAsPDF is a bool."

if __name__ == '__main__':
    unittest.main()

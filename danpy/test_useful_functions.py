import pytest
from datetime import datetime
import unittest
import os
import subprocess
import shutil
import matplotlib.pyplot as plt

from useful_functions import *

class Test_is_number(unittest.TestCase):
    def test_is_number_good(self):
        try:
            is_number(1,"a")
        except:
            self.fail("is_number() raised Error unexpectedly!")

    def test_is_number_good_w_default(self):
        try:
            is_number(1,"a",default=1)
        except:
            self.fail("is_number(default=...) raised Error unexpectedly!")

    def test_is_number_good_w_notes(self):
        try:
            is_number(1,"a",notes="a")
        except:
            self.fail("is_number(notes=...) raised Error unexpectedly!")

    def test_is_number_bad_variableName(self):
        self.assertRaises(AssertionError,is_number,1,1)

    def test_is_number_bad_variableValue(self):
        self.assertRaises(AssertionError,is_number,"a",1)

    def test_is_number_bad_variableValue_w_default(self):
        self.assertRaises(AssertionError,is_number,"a",1,default=1)

    def test_is_number_bad_default(self):
        self.assertRaises(AssertionError,is_number,"a",1,default="a")

    def test_is_number_bad_notes(self):
        self.assertRaises(AssertionError,is_number,"a",1,notes=1)

def create_temp_dir():
    if "TEMP_DIR" in os.listdir():
        shutil.rmtree("TEMP_DIR")
    os.mkdir("TEMP_DIR")

def plot_empty_figure():
    fig = plt.figure()
    plt.plot([0,1,2,3,4],[1,0,-1,0,1],'r')
    plt.title("TEST FIGURE")

class Test_save_figures(unittest.TestCase):
    def test_save_figures_good(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1})
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(
                datetime.today().strftime("%Y_%m_%d")
                in os.listdir("TEMP_DIR")[0]
            )
            figPath = Path("TEMP_DIR") / os.listdir("TEMP_DIR")[0]
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures() raised Error unexpectedly!")

    def test_save_figures_good_w_fileType(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1},fileType="png")
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(
                datetime.today().strftime("%Y_%m_%d")
                in os.listdir("TEMP_DIR")[0]
            )
            figPath = Path("TEMP_DIR") / os.listdir("TEMP_DIR")[0]
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures(fileType=...) raised Error unexpectedly!")

    def test_save_figures_good_w_returnPath(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            figPath = save_figures(
                "TEMP_DIR","a",{"a":1},
                returnPath=True
            )
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(figPath.stem==os.listdir("TEMP_DIR")[0])
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures(returnPath=...) raised Error unexpectedly!")

    def test_save_figures_good_w_subFolderName(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1},subFolderName="a")
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue("a"==os.listdir("TEMP_DIR")[0])
            figPath = Path("TEMP_DIR") / "a"
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures(subFolderName=...) raised Error unexpectedly!")

    def test_save_figures_good_w_saveAsMD(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1},saveAsMD=True)
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(
                datetime.today().strftime("%Y_%m_%d")
                in os.listdir("TEMP_DIR")[0]
            )
            figPath = Path("TEMP_DIR") / os.listdir("TEMP_DIR")[0]
            self.assertTrue(figPath/"README.md" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures(saveAsMD=...) raised Error unexpectedly!")

    def test_save_figures_good_w_addNotes(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1},addNotes="CUSTOM_NOTE")
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(
                datetime.today().strftime("%Y_%m_%d")
                in os.listdir("TEMP_DIR")[0]
            )
            figPath = Path("TEMP_DIR") / os.listdir("TEMP_DIR")[0]
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(
                "CUSTOM_NOTE"
                in (figPath/"notes.txt").read_text()
            )
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
        except:
            self.fail("save_figures(addNotes=...) raised Error unexpectedly!")

    def test_save_figures_good_w_saveAsPDF(self):
        try:
            create_temp_dir()
            plot_empty_figure()
            save_figures("TEMP_DIR","a",{"a":1},saveAsPDF=True)
            plt.close('all')

            self.assertTrue("TEMP_DIR" in os.listdir())
            self.assertTrue(len(os.listdir("TEMP_DIR"))==1)
            self.assertTrue(
                datetime.today().strftime("%Y_%m_%d")
                in os.listdir("TEMP_DIR")[0]
            )
            figPath = Path("TEMP_DIR") / os.listdir("TEMP_DIR")[0]
            self.assertTrue(figPath/"notes.txt" in figPath.iterdir())
            self.assertTrue(figPath/"a_01-01.png" in figPath.iterdir())
            self.assertTrue(figPath/"a_01.pdf" in figPath.iterdir())
        except:
            self.fail("save_figures(saveAsPDF=...) raised Error unexpectedly!")

    def test_save_figures_bad_destination_1(self):
        self.assertRaises(TypeError,save_figures,
            1,"a",{"a":1}
        ) # poor destination (not a str)

    def test_save_figures_bad_destination_2(self):
        self.assertRaises(AssertionError,save_figures,
            "not a dir","a",{"a":1}
        ) # poor destination (not a dir)

    def test_save_figures_bad_baseFileName(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR",1,{"a":1}
        )

    def test_save_figures_bad_params(self):
        create_temp_dir()
        self.assertRaises(AttributeError,save_figures,
            "TEMP_DIR","a","not a dict"
        )

    def test_save_figures_bad_fileType_1(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            fileType=1
        )

    def test_save_figures_bad_fileType_2(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            fileType="not an accepted type"
        )

    def test_save_figures_bad_subFolderName(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            subFolderName=1
        )

    def test_save_figures_bad_saveAsMD(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            saveAsMD='not a bool'
        )

    def test_save_figures_bad_addNotes(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            addNotes=1
        )

    def test_save_figures_bad_saveAsPDF(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            saveAsPDF='not a bool'
        )

    def test_save_figures_bad_returnPath(self):
        create_temp_dir()
        self.assertRaises(AssertionError,save_figures,
            "TEMP_DIR","a",{"a":1},
            returnPath='not a bool'
        )
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

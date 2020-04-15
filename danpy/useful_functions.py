import numpy as np
import os.path
import matplotlib._pylab_helpers
from matplotlib.backends.backend_pdf import PdfPages
import time
import ntpath

def is_number(variableValue,variableName,**kwargs):
    assert type(variableName)==str, "variableName must be a string."
    default = kwargs.get('default',None)
    notes = kwargs.get("notes","")
    assert type(notes)==str, "notes must be a string."
    if (default is None):
        assert str(type(variableValue)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            variableName + " must be an int, float, float32, float64, or numpy.float not "+str(type(variableValue))+". " + notes
    else:
        assert str(type(default)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            "default must be an int, float, float32, float64, or numpy.float not "+str(type(default))+"."
        assert str(type(variableValue)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            variableName + " must be an int, float, float32, float64, or numpy.float not "+str(type(variableValue))+". Default is " + str(default) + ". " + notes

def save_figures(destination,baseFileName,params,returnPath=False,**kwargs):
    fileType = kwargs.get("fileType","png")
    assert fileType in ["eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz"],\
        "fileType must be one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz"

    defaultSubFolderName = time.strftime("%Y_%m_%d_%H%M%S")+"/"
    subFolderName = kwargs.get("subFolderName",defaultSubFolderName)

    filePath = destination + subFolderName
    assert type(destination) == str and destination[-1] == "/", \
    	"destination must be a string ending is '/'. Currently destination = " + str(destination)
    assert type(subFolderName) == str and subFolderName[-1] == "/", \
    	"subFolderName must be a string ending is '/'. Currently subFolderName = " + str(subFolderName)
    assert type(baseFileName) == str, \
    	"baseFileName must be a string. Currently baseFileName = " + str(baseFileName) + " of type " + str(type(baseFileName))

    saveAsMD = kwargs.get("saveAsMD",False)
    assert type(saveAsMD)==bool, "saveAsMD must be either true or false (default)."

    addNotes = kwargs.get("addNotes",None)
    if addNotes is not None:
        assert type(addNotes)==str, "addNotes must be either None (default) or a string. If using markdown notes, please format accordingly."
    else:
        addNotes = "(Add Notes Here.)"

    # Create folder if necessary

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    # Save figures as PNGs

    figs = kwargs.get("figs",
    	[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    	)

    i = 1
    fileName = baseFileName + "_" + "{:0>2d}".format(i) + "-01" + "." + fileType
    if os.path.exists(filePath + fileName) == True:
    	while os.path.exists(filePath + fileName) == True:
    		i += 1
    		fileName = baseFileName + "_" + "{:0>2d}".format(i) + "-01" + "." + fileType

    newFilePaths = []
    for i in range(len(figs)):
        newFilePath = (
            filePath + fileName[:-6] + "{:0>2d}".format(i+1) + "." + fileType
        )
        newFilePaths.append(newFilePath)
    	figs[i].savefig(newFilePath)

    # Save notes file

    if saveAsMD==False:
        notesDocument = open(filePath+'/notes.txt','a+')
        notesDocument.write('[Created ' + defaultSubFolderName[:10].replace("_","/") + " at " + defaultSubFolderName[11:13] + ":" + defaultSubFolderName[13:15] + "." + defaultSubFolderName[15:17] + "]\n\n")

        paramString = "#"*30 +"\n" + "#"*11 + " Notes " + "#"*12 + "\n" + "#"*30 + "\n\n" + "\t\t" + addNotes + "\n\n"
        paramString += "#"*30 +"\n" + "#"*9 + " Parameters " + "#"*9 + "\n" + "#"*30 + "\n\n"
        for key in params.keys():
            paramString += "\t\t" + key + ": " + str(params[key]) + "\n"
        paramString += "\n" + "#"*30 + "\n\n"
        notesDocument.write(paramString)

    else: # saveAsMD==True
        if os.path.exists(filePath+"/README.md"):
            notesDocument = open(filePath+"/README.md","a+")
            notesDocument.write('# Appended on ' + defaultSubFolderName[:10].replace("_","/") + " at " + defaultSubFolderName[11:13] + ":" + defaultSubFolderName[13:15] + "." + defaultSubFolderName[15:17] + "\n\n")
        else: # new folder, no README available
            notesDocument = open(filePath+'/README.md','w')
            notesDocument.write('# README.md for Figures Created ' + defaultSubFolderName[:10].replace("_","/") + " at " + defaultSubFolderName[11:13] + ":" + defaultSubFolderName[13:15] + "." + defaultSubFolderName[15:17] + "\n\n")

        paramString = "## Notes\n\n" + addNotes + "\n\n"
        paramString += "## Parameters \n\n ```py\n params = {\n"
        for key in params.keys():
            if type(params[key])==str:
                paramString += "\t'" + key + "' : '" + params[key] + "',\n"
            else:
                paramString += "\t'" + key + "' : " + str(params[key]) + ",\n"
        paramString = paramString[:-2]
        paramString += "\n}\n```\n\n"
        notesDocument.write(paramString)
        notesDocument.write("## Figures\n\n")
        for newFilePath in newFilePaths:
            notesDocument.write("#### " + ntpath.basename(newFilePath) + "\n\n")
            notesDocument.write(
                '<p align="center">\n'
                + '\t<img width="500" src="'+newFilePath[len(filePath):]+'">\n'
                + '</p>\n\n'
            )

    notesDocument.close()

    saveAsPDF = kwargs.get("saveAsPDF",False)
    assert type(saveAsPDF)==bool, "saveAsPDF must be either True or False."

    if saveAsPDF == True:
    	PDFFileName = fileName[:-7] + ".pdf"
    	assert not os.path.exists(filePath + PDFFileName), \
    			("Error with naming file. "
    			+ PDFFileName
    			+ " should not already exist as "
    			+ fileName
    			+ " does not exist. Try renaming or deleting "
    			+ PDFFileName
    			)

    	PDFFile = PdfPages(filePath + PDFFileName)
    	if len(figs)==1:
    		PDFFile.savefig(figs[0])
    	else:
    		[PDFFile.savefig(fig) for fig in figs]
    	PDFFile.close()

    if returnPath==True:
        return(filePath)

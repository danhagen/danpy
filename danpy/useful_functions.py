import numpy as np
import os.path
import matplotlib._pylab_helpers
from matplotlib.backends.backend_pdf import PdfPages
import time

def is_number(x,variableName,**kwargs):
    assert type(variableName)==str, "variableName must be a string."
    default = kwargs.get('default',None)
    notes = kwargs.get("notes","")
    assert type(notes)==str, "notes must be a string."
    if (default is None):
        assert str(type(x)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            variableName + " must be an int, float, float32, float64, or numpy.float not "+str(type(x))+". " + notes
    else:
        assert str(type(default)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            "default must be an int, float, float32, float64, or numpy.float not "+str(type(default))+"."
        assert str(type(x)) in [
                "<class 'int'>",
                "<class 'float'>",
                "<class 'float32'>",
                "<class 'float64'>",
                "<class 'numpy.float'>",
                "<class 'numpy.float64'>"], \
            variableName + " must be an int, float, float32, float64, or numpy.float not "+str(type(x))+". Default is " + str(default) + ". " + notes

def save_figures(destination,baseFileName,params,returnPath=False,**kwargs):
    fileType = kwargs.get("fileType","png")
    assert fileType in ["eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz"],\
        "fileType must be one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz"
    subFolderName = kwargs.get("subFolderName",time.strftime("%Y_%m_%d_%H%M%S")+"/")
    filePath = destination + subFolderName
    assert type(destination) == str and destination[-1] == "/", \
    	"destination must be a string ending is '/'. Currently destination = " + str(destination)
    assert type(subFolderName) == str and subFolderName[-1] == "/", \
    	"subFolderName must be a string ending is '/'. Currently subFolderName = " + str(subFolderName)
    assert type(baseFileName) == str, \
    	"baseFileName must be a string. Currently baseFileName = " + str(baseFileName) + " of type " + str(type(baseFileName))

    if not os.path.exists(filePath):
        os.makedirs(filePath)

        emptyNotesDocument = open(filePath+'/notes.txt','w')
        emptyNotesDocument.write('[Created ' + subFolderName[:10].replace("_","/") + " at " + subFolderName[11:13] + ":" + subFolderName[13:15] + "." + subFolderName[15:17] + "]\n\n")

        paramString = "#"*30 +"\n" + "#"*11 + " Notes " + "#"*12 + "\n" + "#"*30 + "\n\n" + "\t\tNONE\n\n"
        paramString += "#"*30 +"\n" + "#"*9 + " Parameters " + "#"*9 + "\n" + "#"*30 + "\n\n"
        for key in params.keys():
            paramString += "\t\t" + key + ": " + str(params[key]) + "\n"
        paramString += "\n" + "#"*30
        emptyNotesDocument.write(paramString)

        emptyNotesDocument.close()

    figs = kwargs.get("figs",
    	[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    	)

    saveAsPDF = kwargs.get("saveAsPDF",False)
    assert type(saveAsPDF)==bool, "saveAsPDF must be either True or False."

    i = 1
    fileName = baseFileName + "_" + "{:0>2d}".format(i) + "-01" + "." + fileType
    if os.path.exists(filePath + fileName) == True:
    	while os.path.exists(filePath + fileName) == True:
    		i += 1
    		fileName = baseFileName + "_" + "{:0>2d}".format(i) + "-01" + "." + fileType

    for i in range(len(figs)):
    	figs[i].savefig(filePath + fileName[:-6] + "{:0>2d}".format(i+1) + "." + fileType)

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

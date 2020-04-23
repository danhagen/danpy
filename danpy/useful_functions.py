import numpy as np
import os.path
import matplotlib._pylab_helpers
from matplotlib.backends.backend_pdf import PdfPages
import time
from pathlib import Path

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
    assert type(fileType)==str,"fileType must be a string."
    fileType = fileType.lower()
	assert fileType in ["eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz"],\
		"fileType must be one of the supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz"

	defaultSubFolderName = time.strftime("%Y_%m_%d_%H%M%S")
	subFolderName = kwargs.get("subFolderName",defaultSubFolderName)

    destination = Path(destination)
	filePath = destination / subFolderName

    assert destination.exist() and destination.is_dir(), "destination either does not exist or is not a directory."
    assert type(subFolderName) == str, \
		"subFolderName must be a string. Currently subFolderName is '%s' with type %s." % (str(subFolderName),str(type(subFolderName)))
    filePath.mkdir(exist_ok=True) # Create path if it doesn't already exist.

	assert type(baseFileName) == str, \
		"baseFileName must be a string. Currently baseFileName is '%s' with type %s." % (str(baseFileName),str(type(baseFileName)))

	saveAsMD = kwargs.get("saveAsMD",False)
	assert type(saveAsMD)==bool, "saveAsMD must be either true or false (default)."

	addNotes = kwargs.get("addNotes",None)
	if addNotes is not None:
		assert type(addNotes)==str, "addNotes must be either None (default) or a string. If using markdown notes, please format accordingly."
	else:
		addNotes = "(Add Notes Here.)"

	# Save figures as fileType

	figs = kwargs.get("figs",
		[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
		)

	i = 1
	fileName = f"{baseFileName}_{i:0>2d}-01.{fileType}"
	while (filePath/fileName).exists():
		i += 1
		fileName = f"{baseFileName}_{i:0>2d}-01.{fileType}"
    uniqueBase,_ = fileName.rsplit("-",1)

	newFilePaths = []
	for i in range(len(figs)):
		newFilePath = filePath / f"{uniqueBase}-{i+1:0>2d}.{fileType}"
		newFilePaths.append(newFilePath)
		figs[i].savefig(newFilePath)

	# Save notes file
    YYYY,MM,DD,time = defaultSubFolderName.split("_")
    hh,mm,ss = [time[i:i+2] for i in range(0,len(time),2)]

	if saveAsMD==False:
		if (filePath/"notes.txt").exists():
			notesDocument = (filePath/"notes.txt").open('a+')
			notesDocument.write(f'\n [Appended on {YYYY}/{MM}/{DD} at {hh}:{mm}.{ss} PST] \n\n')
		else:
			notesDocument = (filePath/"notes.txt").open('w')
			notesDocument.write(f'[Created on {YYYY}/{MM}/{DD} at {hh}:{mm}.{ss} PST] \n\n')

        paramString = f"{'#'*30}\n{'#'*11} Notes {'#'*12}\n{'#'*30}\n\n"
        paramString += f"\t{addNotes}\n\n"
        paramString += f"{'#'*30}\n{'#'*9} Parameters {'#'*9}\n{'#'*30}\n\n"
        for key in params.keys():
        	paramString += f"\t{key} : {str(params[key])}\n"
        paramString += f"\n{'#'*30}\n\n"
		notesDocument.write(paramString)

	else: # saveAsMD==True
		if (filePath/"README.md").exists():
			notesDocument = (filePath/"README.md").open("a+")
			notesDocument.write(f'\n\n# Appended on {YYYY}/{MM}/{DD} at {hh}:{mm}.{ss} PST. \n\n')
		else: # new folder, no README available
			notesDocument = (filePath/"README.md").open('w')
            notesDocument.write(f'\n\n# README.md for Figures Created on {YYYY}/{MM}/{DD} at {hh}:{mm}.{ss} PST. \n\n')

        paramString = f"## Notes\n\n{addNotes}\n\n"
        paramString += "## Parameters \n\n```py\nparams = {\n"
        for key in params.keys():
        	paramString += f"\t'{key}' : '{str(params[key])}',\n"
        paramString = paramString[:-2] # removing last ',\n'
        paramString += "\n}\n```\n\n"
		notesDocument.write(paramString)

		notesDocument.write("## Figures\n\n")
		for newFilePath in newFilePaths:
			_, newFileName = os.path.split(newFilePath)
			notesDocument.write(f"#### {newFilePath.name}\n\n")
			notesDocument.write(
				'<p align="center">\n'
				+ f'\t<img width="500" src="{newFilePath.name}">\n'
				+ '</p>\n\n'
			)

	notesDocument.close()

	saveAsPDF = kwargs.get("saveAsPDF",False)
	assert type(saveAsPDF)==bool, "saveAsPDF must be either True or False."

	if saveAsPDF == True:
		PDFFileName = uniqueBase + ".pdf"
		assert not (filePath/PDFFileName).exists(), \
			f"Error with naming file. {PDFFileName} should not already exist as {fileName} does not exist. Try renaming or deleting {PDFFileName}."

		PDFFile = PdfPages(filePath/PDFFileName)
		if len(figs)==1:
			PDFFile.savefig(figs[0])
		else:
			[PDFFile.savefig(fig) for fig in figs]
		PDFFile.close()

	if returnPath==True:
		return(filePath)

#!/usr/bin/python2.7
# coding: utf-8

from config import *
from DownloadCurr import DownloadCurr
from DateConvertible import DateConvertible
import fileManager as fm
import fileReader as fr
import convertData as cD

def infoResults(f):
	if f > 0:
		print "\nC'EST TERMINE! les résultats se trouvent dans le repertoire ", fm.getAbsPath(REP_OUTPUT), "\n"
	else:
		print "\nLe programme s'est bien déroulé, malheureusement aucune donnée n'est disponible pour les dates choisies\n" 

if __name__ == "__main__":

	# download the data on histdata
	dl = DownloadCurr()
	dl.dl()
	
	# dezippage + concatenation de fichier
	fm.listAllFromRootFolder(REP_DL, fm.unzipData)
	fm.listAllFromRootFolder(REP_DL, fm.deleteNonCsvFile)
	fm.concatMultipleFolders(REP_DL, REP_PTF)
	
"""
	# lire et transformer les data
	fichiersEcrits = 0
	dataAttr = ['date', 'min', 'open', 'high', 'low', 'close']
	print "\nTransformation des données... (cela peut prendre quelques minutes)\n"
	for dev in dl.devises:
		inputPath = fm.buildpath(REP_PTF, dev+CONCAT_SUFFIX+'.csv')
		resFile = fm.buildfile('csv', dev, 'JOUR', dl.start_d, dl.end_d)
		resPath = fm.buildpath(REP_OUTPUT, resFile)
		
		dataForex = fr.readFileIntoDict(inputPath, dataAttr)
		dataDay = cD.convertDataMinToDay(dataForex, TZ_OUT)

		fichiersEcrits += cD.writeListToFile(dataDay, resPath)

	fm.emptyFolder(REP_PTF)
	infoResults(fichiersEcrits)
"""



	





	
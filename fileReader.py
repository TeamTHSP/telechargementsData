#!/usr/bin/python2.7
# coding: utf-8

from config import *

def readFileIntoDict(file, champs, delim=','):
	""" lit un fichier csv et met son contenu dans un tableau de dict """
	if type(champs) is not list:
		raise TypeError('Le 2eme argument doit etre une liste')

	globList = []

	with open(file, 'r') as fd:

		for datamin in fd.read().split():
			tmpDict = {}
			tmpList = datamin.split(delim)

			try:
				for i, champ in enumerate(champs):
					#print "tmpList[%d] = %s" % (i, tmpList[i],)
					tmpDict[champ] = tmpList[i]

				globList.append(tmpDict)
			except:
				pass
	return globList

def readFileIntoDictOld(file, champs, delim=','):
	""" lit un fichier csv et met son contenu dans un tableau de dict """
	if type(champs) is not list:
		raise TypeError('Le 2eme argument doit etre une liste')

	globList = []

	with open(file, 'r') as fd:
		#print fd.readlines()
		data = "".join(fd.readlines())
		data_cln = data.split("\n")
	

		for datamin in data_cln :
			tmpDict = {}
			tmpList = datamin.split(delim)
			try:
				for i, champ in enumerate(champs):
					#print "tmpList[%d] = %s" % (i, tmpList[i],)
					tmpDict[champ] = tmpList[i]

				globList.append(tmpDict)
			except:
				pass
	return globList






#!/usr/bin/python2.7
# coding: utf-8

from config import *
from DateConvertible import DateConvertible
from fileManager import buildpath

def buildDate(dico, date='date', time='min'):
	""" construit une datetime a partir d'une date et d'un time """

	try:
		dat = dico[date]
		tim = dico[time]
		return dat + ' ' + tim

	except:
		print dico

def isDataWithinRange(d, min=OPENING_TIME, max=CLOSING_TIME):
	return d >= min*60 and d <= max*60

def compareDataToExtr(curr_cs, max_cs):
	max_cs['high'] = max(max_cs['high'], float(curr_cs['high']))
	max_cs['low'] = min(max_cs['low'], float(curr_cs['low']))
	max_cs['close'] = float(curr_cs['close'])

def initCs():
	return {'high':0, 'open':0, 'close': 0, 'low':10000}

def isAcceptableOpen(t, max_h=MAX_OPEN_H):
	return t < max_h

def shouldCalcOpen(o, time, should):
	#print o, isAcceptableOpen(o), should
	return o == 0 and isAcceptableOpen(time) and not should

def appendTo(d, l, cond):
	if cond:
		l.append(d)

	return False

def writeListToFile(l, file):
	ret = 0
	if not isinstance(l, list): 
		raise TypeError("1er argument n'est pas conforme : type entre =", type(l), " taille= ")

	if len(l) == 0:
		return ret

	with open(file,'w') as fd:
		for line in l:
			fd.write(dictToStr(line))
		ret = 1

	return ret

def dictToStr(dico, delim=';'):
	return dico['date'] +delim+ str(dico['open']) +delim+ str(dico['high']) +delim+ str(dico['low']) +delim+ str(dico['close']) + '\n'



def convertDataMinToDay(l, ref_tz='utc'):
	if not isinstance(l, list): 
		raise TypeError("L'arg 1 doit être une liste... type fourni:", type(l))

	if len(l) == 0:
		print "\nAVERTISSEMENT : Aucune donnée pour la période choisie n'est actuellement téléchargeable, réessayez un peu plus tard"
		return []

	globList = []
	maxCs = initCs()
	lastDate = dateC = DateConvertible(buildDate(l[0]))
	validDay = False

	for dat in l:
		dateC = DateConvertible(buildDate(dat), TZ_DAT)
		dateC.changeTimeZone(ref_tz)

		timeMin = dateC.timeInMin()

		# controler l'heure
		if not isDataWithinRange(timeMin):
			continue

		if not dateC.isSameDayAs(lastDate):
			lastDate = dateC
			
			# print maxCs
			# print '---------------'

			appendTo(maxCs, globList, validDay)
			maxCs = initCs()
			validDay = False

		if shouldCalcOpen(maxCs['open'], timeMin/60, validDay):
			maxCs['open'] = dat['open']
			maxCs['date'] = dateC.toString()
			validDay = True
		
		compareDataToExtr(dat, maxCs)

			

	appendTo(maxCs, globList, validDay)
	# print maxCs
	# print '---------------'

	return globList



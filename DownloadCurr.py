#!/usr/bin/python2.7
# coding: utf-8
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
from config import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

def toDatetime(d, format):
	""" transforme un tableau de date string au format datetime avec leur format, retorune un tuple """

	tup = ()

	for date in d:
		if not isinstance(date, datetime):
			tup += (datetime.strptime(date, "%m/%Y"), )
		else:
			tup += (date, )

	return tup

def isCurrentYear(y):
	if not isinstance(y, datetime):
		raise TypeError("Merci d'entrer une date au format datetime")

	currYear = datetime.today().year

	return currYear == y.year


class DownloadCurr(object):
	""" Telecharger tous les fichiers mois ou année des devises choisies 
		sur la periode choisie """
	def __init__(self):
		super(DownloadCurr, self).__init__()
		self.createDlRep()
		self.collectInfos()

	
	def createDlRep(self):
		if not os.path.exists(REP_DL):
			os.makedirs(REP_DL)

	def setCurrencies(self):
		liste = ["audusd", "eurusd", "eurgbp", "eurchf", "eurjpy", "usdcad", "nzdusd"]

		
		print "\nListe des devises possible de traiter:" 
		print"---------------"
		print "1: AUDUSD, EURUSD, EURGBP, EURCHF, EURJPY, USDCAD, NZDUSD"
		print "2: AUDUSD"
		print "3: EURUSD"
		print "4: EURGBP"
		print "5: EURCHF"
		print "6: EURJPY"
		print "7: USDCAD"
		print "8: NZDUSD"
		print"---------------\n"

		choice = int(raw_input("\nEntrez le nombre correspondant à votre choix:\n"))

		while choice < 1 or choice > 8:
			print choice
			print "Votre choix n'est pas dans la liste"
			choice = raw_input("\nEntrez à nouveau le nombre correspondant à votre choix:\n")

		if(choice is 1 ):
			self.devises = liste
		else:
			self.devises = [liste[choice-2]]

	def selectDates(self):
		isPosterior = isPast = False

		while not isPast:
			self.start_d = self.getDate("Entrez la date de départ (mm/yyyy):")
			isPast = DownloadCurr.isChronological(self.start_d, 'now')
			if not isPast:
				print 'La date entrée est posterieur à la date du jour... \n\n'

		while not isPosterior:
			self.end_d = self.getDate("Entrez la date de fin (mm/yyyy):")
			isPosterior = DownloadCurr.isChronological(self.start_d, self.end_d)
			if not isPosterior:
				print 'La date entrée est antérieure à la date de départ (%s) \n\n' % self.start_d

		print "\nDEBUT: %s, FIN: %s \n" % (self.start_d, self.end_d,) 

	def selectPeriod(self):
		print "Entrer le numero correspondant à l'une des périodes proposées:"
		print "---------------"
		print "1: MOIS PRECEDENT"
		print "2: MOIS EN COURS"
		print "3: ANNEE EN COURS"
		print "4: CHOIX DE DATES PERSONNALISE"
		print "---------------"

		choice = int(raw_input("\nEntrez le nombre correspondant à votre choix:\n"))

		while choice < 1 or choice > 4:
			print "Votre choix (%d) n'est pas dans la liste" % choice
			choice = raw_input("\nEntrez à nouveau le nombre correspondant à votre choix:\n")

		options = [self.getLastMonth, self.getCurrentMonth, self.getCurrentYear, self.selectDates]

		options[choice-1]()

			
	def collectInfos(self):
		self.setCurrencies()
		print "\ndevises traitées:", self.devises, "\n"

		self.selectPeriod()
		
	def formatDateMonthYear(self, d):
		month = str(d.months) if (d.month > 9 ) else "0"+str(d.month)
		year = str(d.year)
		return month + "/" + year
	
	def getCurrentYear(self):
		d = datetime.today()
		self.end_d = self.formatDateMonthYear(d)
		d += relativedelta(month=1)
		self.start_d = self.formatDateMonthYear(d)

	def getMonth(self, date):
		if not isinstance(date, datetime):
			raise TypeError("Mauvais format de date")

		self.start_d = self.end_d = self.formatDateMonthYear(date)

	def getLastMonth(self):
		d = datetime.today()
		d += relativedelta(months=-1)
		self.getMonth(d)

	def getCurrentMonth(self):
		d = datetime.today()
		self.getMonth(d)

	def getDate(self, mess):
		d = raw_input(mess +"\n")
		while not re.match("^[0-9]{2}/[0-9]{4}$", d):
			print "Veuillez entrer une date de la forme 'mm/yyyy'"
			d = raw_input(mess +"\n")
		return d

	def getParams(self, addr):
		p = {}
		html = urllib.urlopen(addr).read()
		soup = BeautifulSoup(html, "html.parser")

		# get all the inputs in the form
		form = soup.find("form",id="file_down")

		for child in form.children:
			try:
				attr = child['name']
				p[attr] = child['value']
			except:
				pass

		return p;

	def setHeader(self, p, dat):
		contentLength = len(dat)
		#print "contentLength:", contentLength
		referer = "http://www.histdata.com/download-free-forex-historical-data/?/"+ DATA_SOURCE +"/"+ DATA_FREQUENCY +"/"+ p["fxpair"] +"/"+ p["date"]
		if len(p["datemonth"]) == 6:
			month = int(p["datemonth"][-2:])
			referer += "/"+ str(month)

		return {
			"Host": "www.histdata.com",
			"Connection": "keep-alive",
			"Content-Length": contentLength,
			"Cache-Control": "max-age=0",
			"Origin": "http://www.histdata.com",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			"Content-Type": "application/x-www-form-urlencoded",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Referer": referer,
			"Accept-Language": "en-US,en;q=0.8,fr;q=0.6",
			"Cookie": "__cfduid=dc63bc2074225879801413509210cdecf1479486569; complianceCookie=on"
		}

	def dlDataMonth(self, addr):
		ret = False
		values = self.getParams(addr)
		data = urllib.urlencode(values)
		headers = self.setHeader(values, data)
		
		req = urllib2.Request(POST_URL, data, headers)

		try:
			response = urllib2.urlopen(req)
			result = response.read()

			if len(result) > 0:
				devise = values["fxpair"]

				if not os.path.exists(REP_DL + devise):
					os.makedirs(REP_DL + devise)

				path = REP_DL + devise +'/'+ devise +'_'+ values["datemonth"] +'_MT_M1.zip'

				with open(path, 'wb') as file:
					file.write(result)

				ret = True

		except:
			print "l'adresse url %s n'existe pas" % (addr,)

		return ret

	def buildUrlMonth(self, date, dev):
		url = self.buildUrl(date, dev) +'/'+ str(date.month)
		return url

	def buildUrl(self, date, dev):
		if not isinstance(date, datetime):
			raise TypeError("Veuillez entrer un type date")
		return 'http://www.histdata.com/download-free-forex-historical-data/?/'+ DATA_SOURCE +'/'+ DATA_FREQUENCY +'/'+ dev +'/'+ str(date.year)

	def dlDevise(self, dev):
		curr_d = datetime.strptime("01/"+ self.start_d, "%d/%m/%Y")
		end_d = datetime.strptime("01/"+ self.end_d, "%d/%m/%Y")
		keepAlive = True

		while(curr_d <= end_d and keepAlive):
			print dev,  ": telechargement de ", curr_d.strftime('%m-%Y')
			url = self.buildUrlMonth(curr_d, dev)
			keepAlive = self.dlDataMonth(url)

			if keepAlive:
				curr_d += relativedelta(months=1)
			elif not isCurrentYear(curr_d):
				print "Le fichier au MOIS n'existe plus, on essaye le fichier ANNEE"
				print dev,  ": telechargement de ", curr_d.strftime('%Y')
				url = self.buildUrl(curr_d, dev)
				keepAlive = self.dlDataMonth(url)
				nbMonthToAdd = 12 - curr_d.month + 1
				curr_d += relativedelta(months=nbMonthToAdd)

	def dl(self):
		for devise in self.devises:
			self.dlDevise(devise)

	@staticmethod
	def isChronological(d1, d2, format="%m/%y"):
		""" verifie que 2 date son dans l'ordre chronologique """

		if d2 == 'now':
			d2 = datetime.today()

		d1, d2 = toDatetime([d1, d2], format)
		diff = d1 - d2

		return diff.days <= 0

	@staticmethod
	def isChronologicalOld(d1, d2, format="%m/%y"):
		""" vérifie bien que la date 1 est bien antérieure à la date 2, ne gere pas les 'fausses dates' """

		formatList = re.split('[^\w% ]*', format)
		d1List = re.split('[^\d% ]*', d1)
		d2List = re.split('[^\d% ]*', d2)

		d1Dict, d2Dict = {'y':0,'m':0,'d':0}, {'y':0,'m':0,'d':0}

		for i, val in enumerate(formatList):
		 	d1Dict[formatList[i][1]] = int(d1List[i])
		 	d2Dict[formatList[i][1]] = int(d2List[i])

		#print d1Dict, d2Dict

		res = (d1Dict['y'] - d2Dict['y'])*365 + (d1Dict['m'] - d2Dict['m'])*31 + (d1Dict['d'] - d2Dict['d']) 

		return res <= 0
		


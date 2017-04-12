#!/usr/bin/python2.7
# coding: utf-8

import re
from datetime import datetime, timedelta
from pytz import timezone


class DateConvertible(object):
	""" docstring for DateConvertible """
	def __init__(self, date, tz=''):
		super(DateConvertible, self).__init__()
		self.date = self.setDate(date)
		if not tz == '':
			self.setTimeZone(tz)

	def setDate(self, d, format='%Y.%m.%d %H:%M'):
		if not re.match("\d{4}.\d{2}.\d{2} \d{2}:\d{2}", d):
			raise ValueError("Error date format")
		return datetime.strptime(d, format)


	def setTimeZone(self, tz='UTC'):
		#print "setTimeZone : avant ", self.date
		tz = timezone(tz)
		self.date = tz.localize(self.date)

		#print "setTimeZone: apres ", self.date
		
		#print "---------"
		return self.date

	def changeTimeZone(self, to):
		#print "changeTimeZone : avant ", self.date
		tz = timezone(to)
		#print "changeTimeZone ", tz
		self.date = self.date.astimezone(tz)
		#print "changeTimeZone : apres ", self.date

	def isSameDayAs(self, dateConv):
		if not isinstance(dateConv, DateConvertible):
			raise("l'arg 1 n'est pas de type DateConvertible")

		d1 = datetime.strftime(self.date, "%Y-%m-%d")
		d2 = datetime.strftime(dateConv.date, "%Y-%m-%d")

		return d1 == d2

	def timeInMin(self):
		return self.date.minute + self.date.hour * 60

	def toString(self,delim='.'):
		return self.date.strftime("%d"+delim+"%m"+delim+"%Y")

	@staticmethod
	def printing():
		print 'class DateConvertible'



















	


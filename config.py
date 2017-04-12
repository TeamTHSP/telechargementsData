#!/usr/bin/python2.7
# coding: utf-8


# paths and files
REP_DL = 'downloads/'
REP_OUTPUT = 'resultats/'
REP_PTF = 'ptf/'
CONCAT_SUFFIX = '_CAT'

# get the data from histdata
DATA_SOURCE = 'metatrader'
DATA_SOURCE_SHORT = 'MT'
DATA_FREQUENCY = '1-minute-bar-quotes'

POST_URL = 'http://www.histdata.com/get.php'

# conversion to day data
OPENING_TIME = 9 # en heure
CLOSING_TIME = 18 # en heure
MAX_OPEN_H = 12 # en heure
TZ_DAT = "America/New_York"
TZ_OUT = "Europe/Paris"

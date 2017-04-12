#!/usr/bin/python2.7
# coding: utf-8

import zipfile
import os, re, shutil
from config import *

def buildpath(path, file, *dirs):
	""" Construit ou crée n'importe quel path  """

	if not os.path.exists(path): 
		os.makedirs(path)

	new_path = path + '/' + '/'.join(dirs) + '/' + file
	new_path_clean = re.sub('/{2,}', '/', new_path)
	dirname = os.path.split(new_path_clean)[0]

	if len(dirs) > 0 and not os.path.exists(dirname): 
		os.makedirs(dirname)
	
	return new_path_clean

def builddir(path, *dirs):
	""" Construit un chemin, équivalent de buildpath pour construire des dirnames """
	
	verifyPath(path)

	new_path = path + '/' + '/'.join(dirs) + '/'
	new_path_clean = re.sub('/{2,}', '/', new_path)

	if len(dirs) > 0 and not os.path.exists(new_path_clean): 
		os.makedirs(new_path_clean)

	return new_path_clean

def verifyPath(path):
	""" Verifie si un chemin existe et le crée dans le cas contraire """

	dirname = os.path.split(path)[0]
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def getAbsPath(path):
	if not os.path.isabs(path):
		if os.path.isdir(path):
			path = builddir(os.getcwd(), path)
		else:
			path = buildpath(os.getcwd(), path)

	return path

def buildfile(ext, *parts):
	""" concatene les differents éléments d'un nom de fichier """

	fname = '_'.join(parts) + '.' +ext
	fname_clean = re.sub('[^0-9a-zA-Z.]+', '_', fname)

	return fname_clean

def listAllFromRootFolder(folder, file_handler, recursive=True):
	""" liste tous les fichiers à partir d'un fichier dit 'root', permet d'excuter une action sur le fichier trouvé, par defaut parcourt les dossier de manière récursive  """

	wd = folder if os.path.isabs(folder) else buildpath(os.getcwd(), '', folder)

	for file in os.listdir(wd):
		path = buildpath(wd, file)
		if os.path.isdir(path) and recursive:
			nwd = builddir(wd, file) 

			listAllFromRootFolder(nwd, file_handler)

		elif os.path.isfile(path):
			file_handler(path)

def unzipData(path, to=''):
	""" dezipe un fichier et supprime le zip à la fin, par defaut dezipe le fichier dans le rep courant """
	if not zipfile.is_zipfile(path):
		return

	if to is '':
		to = os.path.dirname(path)
 
	zip_ref = zipfile.ZipFile(path, 'r')
	zip_ref.extractall(to)
	zip_ref.close()

	os.remove(path)

def deleteExtFile(file, *ext):
	""" Permet de supprimer un fichier qui possede l'une des extensions passées en parametre """

	fext = os.path.splitext(file)[1]
	fname = os.path.split(file)[1]

	extToDelete = "".join(ext)
	
	if extToDelete.find(fext) >= 0 or fname.startswith('.'):
		#print "keep", fname," | ", ext 
		pass
	else:
		#print "delete", fname," | ", ext 
		os.remove(file)

def deleteNonCsvFile(file):
	""" Cas particulier de deleteNonExtFile """

	deleteExtFile(file, ".csv")

def emptyFolder(folder):
	""" Vide un dossier de son contenu , fichiers et dossiers """

	if not os.path.isabs(folder):
		folder = builddir(os.getcwd(), folder)

	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)
		
def concatFilesInFolder(wd, ext='', name=CONCAT_SUFFIX, to='', deleteSrc=True):
	""" permet de concaténer tous les fichiers d'un certain type en un seul fichier """

	if name == CONCAT_SUFFIX:
		name = wd.split('/')[-2] + CONCAT_SUFFIX + ext

	if to == '':
		to = wd if (os.path.isabs(wd)) else builddir(os.getcwd(), folder)

	dest = buildpath(to, name)

	if os.path.exists(dest):
		os.remove(dest)

	with open(dest, 'a') as fcat:
		for file in os.listdir(wd):
			path = buildpath(wd, file)
			fext = '' if (ext == '') else os.path.splitext(file)[1] 

			if os.path.isfile(path) and ext == fext:
				with open(path, 'r') as f:
					lines = f.readlines()
					fcat.writelines(lines)

	if deleteSrc:
		emptyFolder(wd)

def concatMultipleFolders(rootFolder, to=''):
	""" execute concatFilesInFolder(...) sur plusieurs dossier d'un meme repertoire """

	wd = builddir(os.getcwd(), rootFolder)

	for f in os.listdir(wd):
		try:
			path = builddir(wd, f)
		except:
			path = buildpath(wd, f)

		if os.path.isdir(path):
			concatFilesInFolder(path, '.csv', to=to)











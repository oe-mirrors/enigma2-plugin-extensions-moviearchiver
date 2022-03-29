# -*- coding: UTF-8 -*-
#######################################################################
#
#    MovieArchiver
#    Copyright (C) 2013 by svox
#
#    In case of reuse of this source code please do not remove this copyright.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For more information on the GNU General Public License see:
#    <http://www.gnu.org/licenses/>.
#
#######################################################################

from os import path, listdir, walk, access, W_OK, statvfs, stat


def getOldestFile(mediapath, fileExtensions=None):
	'''
	get oldest file from folder

	fileExtensions as tuple. example: ('.txt', '.png')
	'''
	files = getFilesFromPath(mediapath)

	if not files:
		return None

	files = __filterFileListByFileExtension(files, fileExtensions)

	oldestFile = min(files, key=mediapath.getmtime)

	return oldestFile


def getFiles(mediapath, fileExtensions=None):
	'''
	get file list as an array
	sorted by date.
	The oldest first

	fileExtensions as tuple. example: ('.txt', '.png')
	'''
	files = getFilesFromPath(mediapath)

	if not files:
		return None

	files = __filterFileListByFileExtension(files, fileExtensions)

	files.sort(key=lambda s: path.getmtime(path.join(mediapath, s)))
	return files


def getFilesFromPath(mediapath):
	return [path.join(pathmediapath, fname) for fname in listdir(mediapath)]


def getFilesWithNameKey(mediapath, excludedDirNames=None, excludeDirs=None):
	'''
	get recursive all files from given path
	'''
	rs = {}
	for dirPath, dirNames, fileNames in walk(mediapath):
		for fileName in fileNames:
			# skip, if dirname is found in excludedDirNames
			if excludedDirNames is not None and path.basename(dirPath) in excludedDirNames:
				continue

			fullFilePath = path.join(dirPath, fileName)

			skipFile = False

			if dirPath.endswith("/"):
				pathToCheck = dirPath
			else:
				pathToCheck = dirPath + "/"

			# skip, if path found in excludeDirs
			if excludeDirs is not None:
				for excludeDir in excludeDirs:
					if pathToCheck[:len(excludeDir)] == excludeDir:
						skipFile = True
						break

			if skipFile == True:
				continue

			rs[path.join(dirPath.replace(mediapath, ""), fileName)] = fullFilePath

	return rs


def pathIsWriteable(mediapath):
	if path.isfile(mediapath):
		mediapath = path.dirname(mediapath)
	if path.isdir(mediapath) and ismount(mediapath) and access(mediapath, W_OK):
		return True
	else:
		return False


def ismount(mediapath):
	return path.isdir(mountpoint(mediapath))


def mountpoint(mediapath, first=True):
	if first:
		mediapath = path.realpath(mediapath)
	if path.ismount(mediapath) or len(mediapath) == 0:
		return mediapath
	return mountpoint(path.dirname(mediapath), False)


def removeSymbolicLinks(pathList):
	tmpExcludedDirs = []

	for folder in pathList:
		if path.islink(folder) == False:
			tmpExcludedDirs.append(folder)

	return tmpExcludedDirs

###############################


def getFreeDiskspace(mediapath):
	# Check free space on path
	if path.exists(mediapath):
		stat = statvfs(mediapath)
		free = (stat.f_bavail if stat.f_bavail != 0 else stat.f_bfree) * stat.f_bsize // 1024 // 1024 # MB
		return free
	return 0 #maybe call exception


def getFreeDiskspaceText(mediapath):
	free = getFreeDiskspace(mediapath)
	if free >= 10 * 1024:    #MB
		free = "%d GB" % (free // 1024)
	else:
		free = "%d MB" % (free)
	return free


def reachedLimit(mediapath, limit):
	free = getFreeDiskspace(mediapath)
	if limit > (free // 1024): #GB
		return True
	else:
		return False


def checkReachedLimitIfMoveFile(mediapath, limit, moviesFileSize):
	freeDiskSpace = getFreeDiskspace(mediapath)
	limitInMB = limit * 1024

	if (freeDiskSpace + moviesFileSize) >= limitInMB:
		return True
	else:
		return False


def getFileHash(file, factor=10, sizeToSkip=104857600):
	'''
	factor, if size is higher, it is faster but need more ram
	sizeToSkip 104857600 = 100mb
	'''
	# currently, we check only the fileSize because opening
	# files and creating hash are to slow
	return str(stat(file).st_size)

	'''
	filehash = hashlib.md5()

	# this size will stored in ram. and not the whole file
	blockSizeToRead = filehash.block_size * (2**factor)

	# we only want this 5mb for creating an md5 string
	sizeToRead = 5242880

	f = open(file, 'rb')
	f.seek(sizeToSkip, 0)

	totalSize = 0
	while (True):
		readData = f.read(blockSizeToRead)

		if not readData:
			if totalSize == 0:
				f.seek(0, 0)
				continue
			else:
				break

		totalSize += blockSizeToRead

		if totalSize > sizeToRead:
			break

		filehash.update(readData)

	hashStr = filehash.hexdigest()
	f.close()
	return hashStr
	'''

	'''
	Private Methods
	'''


def __filterFileListByFileExtension(files, fileExtensions):
	'''
	fileExtensions as tuple. example: ('.txt', '.png')
	'''
	if fileExtensions is not None:
		files = filter(lambda s: s.lower().endswith(fileExtensions), files)
		#files = filter(lambda s: s.endswith(fileExtension), files)
	return files

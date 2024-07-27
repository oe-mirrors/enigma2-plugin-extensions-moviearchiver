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

# PYTHON IMPORTS
from gettext import bindtextdomain, dgettext, gettext

# ENIGMA IMPORTS
from Components.config import config, ConfigSubsection, ConfigNumber, ConfigText, ConfigYesNo, ConfigLocations
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_HDD, SCOPE_PLUGINS

PluginLanguageDomain = "MovieArchiver"
PluginLanguagePath = "Extensions/MovieArchiver/locale"


def localeInit():
	bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
	return dgettext(PluginLanguageDomain, txt) if dgettext(PluginLanguageDomain, txt) else gettext(txt)


localeInit()
language.addCallback(localeInit)


def printToConsole(msg):
	print("[MovieArchiver] %s" % msg)


# Define Settings Entries
config.plugins.MovieArchiver = ConfigSubsection()
config.plugins.MovieArchiver.enabled = ConfigYesNo(default=False)
config.plugins.MovieArchiver.backup = ConfigYesNo(default=False)
config.plugins.MovieArchiver.skipDuringRecords = ConfigYesNo(default=True)
config.plugins.MovieArchiver.showLimitReachedNotification = ConfigYesNo(default=True)
defaultDir = resolveFilename(SCOPE_HDD)  # default hdd
if config.movielist.videodirs.getValue() and len(config.movielist.videodirs.getValue()) > 0:
	defaultDir = config.movielist.videodirs.getValue()[0]
config.plugins.MovieArchiver.sourcePath = ConfigText(default=defaultDir, fixed_size=False, visible_width=30)
config.plugins.MovieArchiver.sourcePath.lastValue = config.plugins.MovieArchiver.sourcePath.getValue()
config.plugins.MovieArchiver.sourceLimit = ConfigNumber(default=30)
config.plugins.MovieArchiver.excludeDirs = ConfigLocations(visible_width=30)  # exclude folders
config.plugins.MovieArchiver.targetPath = ConfigText(default=defaultDir, fixed_size=False, visible_width=30)
config.plugins.MovieArchiver.targetPath.lastValue = config.plugins.MovieArchiver.targetPath.getValue()
config.plugins.MovieArchiver.targetLimit = ConfigNumber(default=30)  # interval

# Helper Functions


def getSourcePath():
	return config.plugins.MovieArchiver.sourcePath


def getSourcePathValue():
	return getSourcePath().getValue()


def getTargetPath():
	return config.plugins.MovieArchiver.targetPath


def getTargetPathValue():
	return getTargetPath().getValue()


__all__ = ['_', 'config', 'printToConsole', 'getSourcePath', 'getSourcePathValue', 'getTargetPath', 'getTargetPathValue']

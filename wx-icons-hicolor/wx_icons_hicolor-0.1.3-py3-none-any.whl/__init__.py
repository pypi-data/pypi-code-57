#!/usr/bin/python3
#
#  __init__.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Includes icons from the gnome-icon-theme
#  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/gnome-icon-theme/3.12.0-3/gnome-icon-theme_3.12.0.orig.tar.xz
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# Hicolor
# https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/hicolor-icon-theme/0.17-2/hicolor-icon-theme_0.17.orig.tar.xz

# stdlib
from typing import Any, Tuple, Union

# 3rd party
import wx  # type: ignore

# this package
from wx_icons_hicolor import Hicolor
from wx_icons_hicolor.constants import mime, theme_index_path
from wx_icons_hicolor.directory import Directory
from wx_icons_hicolor.icon import Icon
from wx_icons_hicolor.icon_theme import HicolorIconTheme, IconTheme
from wx_icons_hicolor.test import test_icon_theme, test_random_icons

__author__ = "Dominic Davis-Foster"
__copyright__ = "2014-2020 Dominic Davis-Foster"
__version__: str = "0.1.3"

__license__ = "LGPLv3+"
__email__ = "dominic@davis-foster.co.uk"

__all__ = [
		"version",
		"wxHicolorIconTheme",
		"Hicolor",
		"mime",
		"theme_index_path",
		"Directory",
		"Icon",
		"HicolorIconTheme",
		"test_icon_theme",
		"test_random_icons",
		]


def version() -> str:
	return f"""wx_icons_hicolor
Version {__version__}
Gnome Icon Theme Version 3.12.0
"""


class wxHicolorIconTheme(wx.ArtProvider):
	_hicolor_theme: IconTheme = HicolorIconTheme.create()

	@staticmethod
	def HasNativeProvider() -> bool:
		return False

	@staticmethod
	def icon2bitmap(icon: Icon, size: int) -> wx.Bitmap:
		if icon.scalable:
			return icon.as_bitmap(size)
		else:
			return icon.as_bitmap()

	def CreateBitmap(self, id: Any, client: Any, size: Union[Tuple[int], wx.Size]) -> wx.Bitmap:

		icon = self._hicolor_theme.find_icon(id, size[0], None)

		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size[0])

		else:
			# return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Hicolor theme")
			print(id)
			return super().CreateBitmap(id, client, size)

	# # optionally override this one as well
	# def CreateIconBundle(self, id, client):
	# 	# Your implementation of CreateIconBundle here
	# 	pass


if __name__ == "__main__":
	# theme = HicolorIconTheme.from_configparser(theme_index_path)
	theme = HicolorIconTheme.create()

	# for directory in theme.directories:
	# 	print(directory.icons)

	# test_random_icons(theme)

	test_icon_theme(theme, show_success=False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gui_widgets.py
#
#  Copyright 2023 yucef sourani <yuceff28@fedora>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from gi.repository import Gtk,Gdk

class IconNamePaint(Gtk.Widget):
    def __init__(self,icon_name,w,h,parent):
        Gtk.Widget.__init__(self)
        self.props.hexpand = True
        self.props.vexpand = True

        self.__parent = parent
        self.__w      = w
        self.__h      = h
        self.__icon_name            = icon_name
        self.__icon_theme           = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.__themeicon_paintable  = self.__icon_theme.lookup_icon(self.__icon_name,["applications-accessories"],self.__w,1, self.__parent.get_direction(), Gtk.IconLookupFlags.FORCE_REGULAR)

    def do_snapshot(self,snapshot):
        self.__themeicon_paintable.snapshot(snapshot,self.__w,self.__h)

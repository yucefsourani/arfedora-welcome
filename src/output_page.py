#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  output_page.py
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
import gi
gi.require_version('Vte', '3.91')
from gi.repository import Adw
from gi.repository import Gtk,Vte,Gdk
import sys

class OutPutPage():
    def __init__(self,parent):
        self.parent   = parent
        self.mbox     = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)
        self.mbox.set_hexpand(True)
        self.mbox.set_vexpand(True)
        
        tscrolledwindow = Gtk.ScrolledWindow()
        #tscrolledwindow.set_hexpand(True)
        #tscrolledwindow.set_vexpand(True)
        self.mbox.append(tscrolledwindow)
        tscrolledwindow.set_policy(Gtk.PolicyType.NEVER ,Gtk.PolicyType.AUTOMATIC)
        self.terminal = Vte.Terminal()
        self.terminal.set_hexpand(True)
        self.terminal.set_vexpand(True)
        self.terminal.set_scroll_on_keystroke(True)
        self.terminal.set_scroll_on_output(True)
        self.terminal.set_rewrap_on_resize(True)
        self.terminal.set_input_enabled(False)
        tscrolledwindow.set_child(self.terminal)
            
        #self.terminal.set_color_background(Gdk.RGBA(red=0.180392, green=0.203922, blue=0.211765, alpha=1.000000))
        #self.terminal.set_color_foreground(Gdk.RGBA(red=0.988235, green=0.913725, blue=0.309804, alpha=1.000000))
        vadjustment = self.terminal.get_vadjustment()
        tscrolledwindow.set_vadjustment(vadjustment)
        _pty = Vte.Pty.new_sync(Vte.PtyFlags(0),None)
        if "--debug" not in sys.argv and "-d" not in sys.argv:
            _pty.child_setup()
            self.terminal.set_pty(_pty)

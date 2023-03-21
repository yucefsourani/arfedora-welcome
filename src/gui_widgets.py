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
from gi.repository import Gtk,Gdk,Adw

infooverlay = Adw.ToastOverlay.new()
all_infobar = {}

class IconNamePaint(Gtk.Widget):
    def __init__(self,icon_name,w,h,parent):
        Gtk.Widget.__init__(self)
        #self.props.hexpand = True
        #self.props.vexpand = True

        self.__parent = parent
        self.__w      = w
        self.__h      = h
        self.__icon_name            = icon_name
        self.__icon_theme           = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.__themeicon_paintable  = self.__icon_theme.lookup_icon(self.__icon_name,["applications-accessories"],self.__w,1, self.__parent.get_direction(), Gtk.IconLookupFlags.FORCE_REGULAR)

    def do_snapshot(self,snapshot):
        self.__themeicon_paintable.snapshot(snapshot,self.__w,self.__h)

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE
        
    def do_measure(self, orientation, for_size):
        if orientation == Gtk.Orientation.HORIZONTAL:
            return (self.__w, self.__w, -1, -1)
        else:
            return (self.__h, self.__h, -1, -1)

class ImagePaint(Gtk.Widget):
    def __init__(self,image_location,w,h):
        Gtk.Widget.__init__(self)

        self.__w            = w
        self.__h            = h
        self.image_location = image_location
        self.__texture      = Gdk.Texture.new_from_filename(self.image_location)

    def do_snapshot(self,snapshot):
        self.__texture.snapshot(snapshot,self.__w,self.__h)

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE
        
    def do_measure(self, orientation, for_size):
        if orientation == Gtk.Orientation.HORIZONTAL:
            return (self.__w, self.__w, -1, -1)
        else:
            return (self.__h, self.__h, -1, -1)
            

def create_toast(title="",priority=1,button_label="Ok",timeout=0,custom_title=False,action_name=False,action_target=False,infoover=False):
    toast = Adw.Toast.new(title)
    if custom_title:
        toast.props.custom_title = custom_title
        
    if action_name:
        toast.props.action_name = action_name
        
    if action_name and action_target:
        toast.props.action_target = action_target

    if priority<0 or priority>1:
        priority = 0
        
    toast.props.priority = Adw.ToastPriority(priority)
    toast.props.button_label = button_label
    toast.props.timeout      = timeout
    
    if not infoover:
        infoover = infooverlay
    return infoover.add_toast(toast)


def on_infobar_response(info_bar, response_id,parent,infobar,func,argv,nofunc,noargv):
    if response_id == Gtk.ResponseType.CLOSE :
        on_infobar_close(info_bar,parent,infobar)
    elif response_id == Gtk.ResponseType.NO:
        on_infobar_close(info_bar,parent,infobar)
        if nofunc:
            if noargv:
                nofunc(*noargv)
            else:
                nofunc()
    else:
        on_infobar_close(info_bar,parent,infobar)
        if func:
            if argv:
                func(*argv)
            else:
                func()
    
def on_infobar_close(infobar_,parent,infobar):
    parent.infobar = None
    infobar_.props.revealed = False
    all_infobar[parent].remove(infobar)
    parent.remove_overlay(infobar)
    infobar_.unparent()
    infobar_.run_dispose()
    infobar.unparent()
    infobar.run_dispose()
    if len(all_infobar[parent])>0:
        print("ok")
        new_infobar    = all_infobar[parent][0]
        parent.add_overlay(new_infobar)
        parent.infobar = new_infobar
        new_infobar.infobar_.props.revealed = True
    
def yes_or_no(parent,msg="",func=None,argv=None,nofunc=None,noargv=None,label=False,message_type=2,show_close_button=True,yes="Yes",no="No"):
    if parent not in all_infobar.keys():
        all_infobar.setdefault(parent,list())
    if "infobar" not in parent.__dict__.keys():
        parent.infobar = None
    infobar          = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=0)
    infobar_         = Gtk.InfoBar.new()
    infobar.append(infobar_)
    infobar.infobar_ = infobar_
    if message_type < 0 or message_type >4:
        message_type = 2
    if label:
        infobar_.add_child(label)
    else:
        label = Gtk.Label.new()
        label.props.label = msg
        label.props.wrap  = True
        infobar_.add_child(label)
    infobar_.props.message_type      = Gtk.MessageType(message_type)
    infobar_.props.show_close_button = show_close_button
    
    infobar_.add_button(yes,-8)
    infobar_.add_button(no,-9)
    all_infobar[parent].append(infobar)
    infobar_.connect("close",on_infobar_close,parent,infobar)
    infobar_.connect("response",on_infobar_response,parent,infobar,func,argv,nofunc,noargv)
    if not parent.infobar:
        parent.add_overlay(infobar)
        parent.infobar = infobar
        infobar_.props.revealed = True
    return infobar_

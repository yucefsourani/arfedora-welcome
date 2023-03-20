#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  uplugin.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
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
from gi.repository import Gtk, GLib, GdkPixbuf, Pango,Gdk
import threading
import os
from arfedora_welcome import utils


class ThreadCheck(threading.Thread):
    def __init__(self,func_check,label,
               button_remove_label,button_install_label,
               spinner,button,loadingmsg,daemon):
        threading.Thread.__init__(self,daemon=daemon)
        self.func_check           = func_check
        self.label                = label
        self.button_remove_label  = button_remove_label
        self.button_install_label = button_install_label
        self.spinner              = spinner
        self.button               = button
        self.loadingmsg           = loadingmsg

    def run(self):
        GLib.idle_add(self.label.set_markup,self.loadingmsg)
        GLib.idle_add(self.button.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        if self.func_check():
            GLib.idle_add(self.label.set_markup,self.button_install_label)
            self.button.__to_install = True
        else:
            GLib.idle_add(self.label.set_markup,self.button_remove_label)
            self.button.__to_install = False
        
        GLib.idle_add(self.button.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)


        
class ThreadCheckInstallRemove(threading.Thread):
    def __init__(self,func_check,func_install,func_remove,label,
               button_remove_label,button_install_label,parent,
               spinner,blockparent,waitmsg,runningmsg,
               ifinstallfailmsg,ifremovefailmsg,
               ifinstallsucessmsg,ifremovesucessmsg,
               daemon,modal,button):
                   
        threading.Thread.__init__(self,daemon=daemon)
        self.func_check           = func_check
        self.func_install         = func_install
        self.func_remove          = func_remove
        self.label                = label
        self.button_remove_label  = button_remove_label
        self.button_install_label = button_install_label
        self.parent               = parent
        self.spinner              = spinner
        self.blockparent          = blockparent
        self.waitmsg              = waitmsg
        self.runningmsg           = runningmsg
        self.ifinstallfailmsg     = ifinstallfailmsg
        self.ifremovefailmsg      = ifremovefailmsg
        self.ifinstallsucessmsg   = ifinstallsucessmsg
        self.ifremovesucessmsg    = ifremovesucessmsg
        self.modal                = modal
        self.__button__           = button
        
    def run(self):
        GLib.idle_add(self.__button__.set_sensitive,False)
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.label.set_markup,self.waitmsg)
        

        GLib.idle_add(self.label.set_markup,self.runningmsg)
        check_install = self.func_install()
        if self.__button__.__to_install:
            if check_install:
                GLib.idle_add(self.label.set_markup,self.button_remove_label)
                if self.ifinstallsucessmsg:
                    self.__button__.__to_install = not self.__button__.__to_install
            else:
                GLib.idle_add(self.label.set_markup,self.button_install_label)
                if self.ifinstallfailmsg:
                    #GLib.idle_add(self.info__,self.ifinstallfailmsg)
                    pass
        else:
            GLib.idle_add(self.label.set_markup,self.runningmsg)
            check_remove = self.func_remove()
            if check_remove:
                GLib.idle_add(self.label.set_markup,self.button_install_label)
                if self.ifremovesucessmsg:
                    self.__button__.__to_install = not self.__button__.__to_install
            else:
                GLib.idle_add(self.label.set_markup,self.button_remove_label)
                if self.ifremovefailmsg:
                    #GLib.idle_add(self.info__,self.ifremovefailmsg)
                    pass
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.__button__.set_sensitive,True)

        


class BasePlugin():        
    def __init__(self,parent,spacing=2,margin=10,button_image="",button_install_label="Install",
                button_remove_label="Remove",
                buttontooltip="Test tooltip",
                buttonsizewidth=100,
                buttonsizeheight=100,
                button_relief=2,
                blockparent=True,
                waitmsg="Wait...",
                runningmsg="Running...",
                loadingmsg="Loading...",
                ifinstallfailmsg="",
                ifremovefailmsg="",
                ifinstallsucessmsg="",
                ifremovesucessmsg="",
                beforeinstallyesorno="",
                beforeremoveyesorno="",
                expand=False,
                daemon=True,
                modal=False):
        
        self.___parent               = parent
        self.___spacing              = spacing
        self.___button_image         = button_image
        self.___button_install_label = button_install_label
        self.___button_remove_label  = button_remove_label
        self.___buttontooltip        = buttontooltip
        self.___buttonsizewidth      = buttonsizewidth
        self.___buttonsizeheight     = buttonsizeheight
        self.___button_relief        = button_relief
        self.___blockparent          = blockparent
        self.___waitmsg              = waitmsg
        self.___runningmsg           = runningmsg
        self.___loadingmsg           = loadingmsg
        self.___ifinstallfailmsg     = ifinstallfailmsg
        self.___ifremovefailmsg      = ifremovefailmsg
        self.___ifinstallsucessmsg   = ifinstallsucessmsg
        self.___ifremovesucessmsg    = ifremovesucessmsg
        self.___beforeinstallyesorno = beforeinstallyesorno
        self.___beforeremoveyesorno  = beforeremoveyesorno
        self.__daemon                = daemon
        self.__modal                 = modal

        
        self.__mainbox__   = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=self.___spacing)
        self.__button__    = Gtk.Button.new()
        self.__button__props.hexpand = True
        self.__button__props.vexpand = True
        self.__button__.set_has_frame(self.___button_relief)
        self.__button__.connect("clicked",self.___clicked)
        try:
            ___pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(utils.get_image_location(self.___button_image),self.___buttonsizewidth,self.___buttonsizeheight)
            ___image  = Gtk.Image.new_from_pixbuf(___pixbuf)
        except Exception as e:
            print(e)
            icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
            icon_theme.lookup_icon(plugin.category_icon_theme,["applications-accessories"],32,1, self.___parent.get_direction(), Gtk.IconLookupFlags.FORCE_REGULAR )
            ___image   = Gtk.Image.new_from_paintable(icon_theme)
        
        self.__button__.set_child(___image)
        if self.___buttontooltip:
            self.__button__.set_tooltip_markup(self.___buttontooltip)
    
        self.__spinner__       = Gtk.Spinner()
        self.__spinner__.hexpand = True
        self.__spinner__.vexpand = True
        self.__progressbar__   = Gtk.ProgressBar()
        
        self.__label__         = Gtk.Label.new()
        self.__label__.hexpand = True
        self.__label__.vexpand = True
        self.__label__.props.use_markup=True
        self.__label__.set_wrap(True)
        self.__label__.set_wrap_mode(Pango.WrapMode.WORD_CHAR )
        self.__label__.set_max_width_chars(14)
        self.__label__.set_justify(Gtk.Justification.CENTER)
        
        
    
        self.__mainbox__.append(self.__button__)
        self.__mainbox__.append(self.__label__)
        self.__mainbox__.append(self.__spinner__)

        self._init_()
        ThreadCheck(self.check,self.__label__,
                    self.___button_remove_label,
                    self.___button_install_label,
                    self.__spinner__,
                    self.__button__,
                    self.___loadingmsg,self.__daemon).start()

    def _init_(self):
        pass
        
    def ___clicked(self,button):
        if self.func_check():
            if self.beforeinstallyesorno:
                if True:
                    self.___clicked_t(button)
            else:
                self.___clicked_t(button)
        else:
            if self.beforeremoveyesorno:
                if True:
                    self.___clicked_t(button)
            else:
                self.___clicked_t(button)
            
    def ___clicked_t(self,button):
        ThreadCheckInstallRemove(func_check=self.check,
        func_install=self.install,
        func_remove=self.remove,
        label=self.__label__,
        button_remove_label=self.___button_remove_label,
        button_install_label=self.___button_install_label,
        parent=self.___parent,
        spinner=self.__spinner__,
        blockparent=self.___blockparent,
        waitmsg=self.___waitmsg,
        runningmsg=self.___runningmsg,
        ifinstallfailmsg=self.___ifinstallfailmsg,
        ifremovefailmsg=self.___ifremovefailmsg,
        ifinstallsucessmsg=self.___ifinstallsucessmsg,
        ifremovesucessmsg=self.___ifremovesucessmsg,
        daemon=self.__daemon,
        modal=self.__modal,
        button=button
        ).start()





    

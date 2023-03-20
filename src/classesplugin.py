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
from arfedora_welcome import gui_widgets
import uuid



class ThreadCheck(threading.Thread):
    def __init__(self,func_check,label,
               button_remove_label,button_install_label,
               spinner,button,loadingmsg,daemon):
        threading.Thread.__init__(self,daemon=daemon)
        self.func_check           = func_check
        self.__label__            = label
        self.button_remove_label  = button_remove_label
        self.button_install_label = button_install_label
        self.spinner              = spinner
        self.button               = button
        self.loadingmsg           = loadingmsg

    def run(self):
        GLib.idle_add(self.__label__.set_label,self.loadingmsg)
        GLib.idle_add(self.button.set_sensitive,False)
        GLib.idle_add(self.spinner.show)
        GLib.idle_add(self.spinner.start)

        if self.func_check():
            self.button.to_install = True
            GLib.idle_add(self.__label__.set_label,self.button_install_label)
            GLib.idle_add(self.button.set_css_classes,["suggested-action"])
        else:
            self.button.to_install = False
            GLib.idle_add(self.__label__.set_label,self.button_remove_label)
            GLib.idle_add(self.button.set_css_classes,["destructive-action"])
        GLib.idle_add(self.button.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.spinner.hide)



        
class ThreadCheckInstallRemove(threading.Thread):
    def __init__(self,func_check,func_install,func_remove,label,
               button_remove_label,button_install_label,parent,
               spinner,blockparent,waitmsg,runningmsg,
               ifinstallfailmsg,ifremovefailmsg,
               ifinstallsucessmsg,ifremovesucessmsg,
               daemon,button,threads,uuid_):
                   
        threading.Thread.__init__(self,daemon=daemon)
        self.func_check           = func_check
        self.func_install         = func_install
        self.func_remove          = func_remove
        self.__label__            = label
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
        self.__button__           = button
        self.__threads            = threads
        self.uuid_                = uuid_
        
        GLib.idle_add(self.__label__.set_label,"Waiting...")
        GLib.idle_add(self.__button__.set_css_classes,["wait-action-button"])
        
    def run(self):
        GLib.idle_add(self.__button__.set_sensitive,False)
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,False)
        GLib.idle_add(self.spinner.show)
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.__label__.set_label,self.waitmsg)
        GLib.idle_add(self.__button__.set_css_classes,["running-destructive-action-button"])
        
        GLib.idle_add(self.__label__.set_label,self.runningmsg)
        if self.__button__.to_install:
            check_install = self.func_install()
            if check_install:
                self.__button__.to_install = not self.__button__.to_install
                if self.ifinstallsucessmsg:
                    GLib.idle_add(gui_widgets.create_toast,self.ifinstallsucessmsg)                    
            else:
                if self.ifinstallfailmsg:
                    GLib.idle_add(gui_widgets.create_toast,self.ifinstallfailmsg)
                    
        else:
            check_remove = self.func_remove()
            if check_remove:
                self.__button__.to_install = not self.__button__.to_install
                if self.ifremovesucessmsg:
                    GLib.idle_add(gui_widgets.create_toast,self.ifremovesucessmsg)
                    
            else:
                if self.ifremovefailmsg:
                    GLib.idle_add(gui_widgets.create_toast,self.ifremovefailmsg)
    

        if  self.__button__.to_install:
            GLib.idle_add(self.__label__.set_label,self.button_install_label)
            GLib.idle_add(self.__button__.set_css_classes,["suggested-action"])
        else:
            GLib.idle_add(self.__label__.set_label,self.button_remove_label)
            GLib.idle_add(self.__button__.set_css_classes,["destructive-action"])
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.spinner.hide)
        GLib.idle_add(self.__button__.set_sensitive,True)
        del self.__threads[self.uuid_]
        if self.__threads:
            t = list(self.__threads.values())[0]
            if not t.is_alive():
                t.start()
        
        
class BasePlugin():        
    def __init__(self,parent,
                threads,
                button_image="",
                button_install_label="Install",
                button_remove_label="Remove",
                button_frame=False,
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
                daemon=True,
                parallel_install=False):
        
        self.___parent               = parent
        self.__threads               = threads
        self.___button_image         = button_image
        self.___button_install_label = button_install_label
        self.___button_remove_label  = button_remove_label
        self.___button_frame         = button_frame
        self.___blockparent          = blockparent
        self.___waitmsg              = waitmsg
        self._runningmsg             = runningmsg
        self.___loadingmsg           = loadingmsg
        self.___ifinstallfailmsg     = ifinstallfailmsg
        self.___ifremovefailmsg      = ifremovefailmsg
        self.___ifinstallsucessmsg   = ifinstallsucessmsg
        self.___ifremovesucessmsg    = ifremovesucessmsg
        self.___beforeinstallyesorno = beforeinstallyesorno
        self.___beforeremoveyesorno  = beforeremoveyesorno
        self.__daemon                = daemon
        self.__parallel_install      = parallel_install
        self.uuid_ = uuid.uuid1()
        
        self.__button_box__ = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=2)
        self.__button__     = Gtk.Button.new()
        self.__button__.props.margin_top = 5
        self.__button_box__.append(self.__button__)
        self.__button__.set_has_frame(self.___button_frame)
        self.__button__.connect("clicked",self.___clicked)
        
        self.__label__ = Gtk.Label.new()
        self.__label__.set_ellipsize(Pango.EllipsizeMode.END)
        self.__label__.set_justify(Gtk.Justification.CENTER)
        self.__button__.set_child(self.__label__)
        try:
            ___pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(utils.get_image_location(self.___button_image),100,100)
            self.__image__  = Gtk.Image.new_from_pixbuf(___pixbuf)
        except Exception as e:
            print(e)
            self.__image__   = gui_widgets.IconNamePaint("applications-accessories",100,100,self.___parent)
        self.__image__.props.margin_top    = 5
        self.__image__.props.margin_bottom = 5
        
        self.__spinner__     = Gtk.Spinner()
        self.__spinner__.hide()
        self.__spinner__.set_halign(Gtk.Align.CENTER)
        self.__button_box__.append(self.__spinner__)
        
        
        self.__progressbar__ = Gtk.ProgressBar()
        self.__progressbar__.set_show_text(True)
        self.__progressbar__.set_ellipsize(Pango.EllipsizeMode.END)
        self.__progressbar__.hide()
        self.__button_box__.append(self.__progressbar__)
        #self.__progressbar__.props.hexpand = True
        
        
        
        self._init_()
        self.check_()
        
    def check_(self):
        ThreadCheck(self.check,self.__label__,
                    self.___button_remove_label,
                    self.___button_install_label,
                    self.__spinner__,
                    self.__button__,
                    self.___loadingmsg,self.__daemon).start()

    def _init_(self):
        pass

    def ___clicked(self,button):
        if not self.__parallel_install:
            if self.uuid_ in self.__threads.keys():
                del self.__threads[self.uuid_]
                ThreadCheck(self.check,self.__label__,
                            self.___button_remove_label,
                            self.___button_install_label,
                            self.__spinner__,
                            self.__button__,
                            self.___loadingmsg,self.__daemon).start()
                return
        if self.__button__.to_install:
            if self.___beforeinstallyesorno:
                infobar = gui_widgets.yes_or_no(self.__banner__,self.___beforeinstallyesorno,
                                     func=self.___clicked_t,argv=(button,))
                return
            else:
                self.___clicked_t(button)
        else:
            if self.___beforeremoveyesorno:
                infobar = gui_widgets.yes_or_no(self.__banner__,self.___beforeremoveyesorno,
                                     func=self.___clicked_t,argv=(button,))
                return
            else:
                self.___clicked_t(button)
            
    def ___clicked_t(self,button):
        t = ThreadCheckInstallRemove(func_check=self.check,
        func_install=self.install,
        func_remove=self.remove,
        label=self.__label__,
        button_remove_label=self.___button_remove_label,
        button_install_label=self.___button_install_label,
        parent=self.___parent,
        spinner=self.__spinner__,
        blockparent=self.___blockparent,
        waitmsg=self.___waitmsg,
        runningmsg=self._runningmsg,
        ifinstallfailmsg=self.___ifinstallfailmsg,
        ifremovefailmsg=self.___ifremovefailmsg,
        ifinstallsucessmsg=self.___ifinstallsucessmsg,
        ifremovesucessmsg=self.___ifremovesucessmsg,
        daemon=self.__daemon,
        button=button,
        threads=self.__threads,
        uuid_=self.uuid_)
        self.__threads.setdefault(self.uuid_,t)
        if  self.__parallel_install:
            t.start()
            return
        if not any([i for i in self.__threads.values() if i.is_alive()]):
            t.start()

            





    

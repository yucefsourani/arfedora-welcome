#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
from arfedora_welcome.classesplugin import BasePlugin
from arfedora_welcome.utils import get_uniq_name
import subprocess


if_true_skip         = False
type_                = "Oneshot"
arch                 = ("all",)
distro_name          = ("all",)
distro_version       = ("all",)
category             = "Gnome"
category_icon_theme  = "preferences-desktop-appearance-symbolic"
desktop_env          = ("gnome","gnome-xorg")
display_type         = ("all",)
title                = "FR/ARA Keyboard Layout"
subtitle             = "Set keyboard layout French/arabic"
keywords             = "arabic keyboard layout"
licenses             = ()
website              = ()


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="input-keyboard.png",
                            button_install_label="Run Task",
                            button_remove_label="Run Task",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            beforeinstallyesorno="Set keyboard layout French/arabic ?",
                            beforeremoveyesorno="Set keyboard layout French/arabic ?",
                            parallel_install=True)


    def check(self):
        return True # force return True 

        
    def install(self):
        subprocess.call("""gsettings set org.gnome.desktop.input-sources sources \"[('xkb', 'fr'), ('xkb', 'ara')]\" """,shell=True)
        return False # force return False 
        
    def remove(self):
        subprocess.call("""gsettings set org.gnome.desktop.input-sources sources \"[('xkb', 'fr'), ('xkb', 'ara')]\" """,shell=True)
        return False # force return False 


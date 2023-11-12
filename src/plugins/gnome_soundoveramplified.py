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
type_                = "Enable/Disable"
arch                 = ("all",)
distro_name          = ("all",)
distro_version       = ("all",)
category             = "Gnome"
category_icon_theme  = "preferences-desktop-appearance-symbolic"
desktop_env          = ("gnome",)
display_type         = ("all",)
title                = "Sound Overamplification"
subtitle             = "Allow volume to exceed 100%"
keywords             = "sound over volume"
licenses             = ()
website              = ()


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="audio-volume-high.png",
                            button_install_label="Enable",
                            button_remove_label="Disable",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            parallel_install=True)


    def check(self):
        output = subprocess.check_output("gsettings get org.gnome.desktop.sound allow-volume-above-100-percent",shell=True).decode("utf-8").strip()
        if output == "'true'" or output == "true":
            return False
        return True

        
    def install(self):
        if subprocess.call("gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true",shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("gsettings set org.gnome.desktop.sound allow-volume-above-100-percent false",shell=True)==0:
            return True
        return False


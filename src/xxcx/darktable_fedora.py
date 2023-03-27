#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  darktable.py
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
import os

if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Graphics"
category_icon_theme  = "applications-graphics-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Darktable"
subtitle             = "Organize and develop images from digital cameras"
keywords             = "darktable camera"
licenses             = (("License\nGPL v3.0+","https://www.gnu.org/licenses/gpl-3.0.html"),)
website              = ("WebSite","https://www.darktable.org/")
                

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="darktable.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Darktable Failed",
                            ifremovefailmsg="Remove Darktable Failed",
                            parallel_install=False)


    def check(self):
        return not os.path.isfile("/usr/bin/darktable")
        
    def install(self):
        if subprocess.call("pkexec dnf install darktable -y --best",shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e darktable",shell=True)==0:
            return True
        return False


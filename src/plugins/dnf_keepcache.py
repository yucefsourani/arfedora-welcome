#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dnf_keepcache.py
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
distro_name          = ("fedora",)
distro_version       = ("41","42","43","44","45","46")
category             = "Utils"
category_icon_theme  = "applications-utilities-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Dnf Keepcache"
subtitle             = "Dnf Enable/Disable keepcache"
keywords             = "dnf"
licenses             = ()
website              = ()


true  = ["True", "true", "1"]
false = ["False", "false", "0"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="rpm.svg",
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
        check = subprocess.check_output("dnf --dump-main-config | grep keepcache |cut -f2- -d \"=\"",shell=True).strip().decode("utf-8")
        if check in true:
            return False
        return True

        
    def install(self):
        if subprocess.call("pkexec dnf config-manager setopt keepcache=1",shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec dnf config-manager setopt keepcache=0",shell=True)==0:
            return True
        return False


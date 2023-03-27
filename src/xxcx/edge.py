#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vivaldi.py
#  
#  Copyright 2020 youcef sourani <youssef.m.sourani@gmail.com>
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
from arfedora_welcome.utils import get_uniq_name,write_to_tmp
import subprocess
import os

if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Internet"
category_icon_theme  = "web-browser-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Edge"
subtitle             = "Introducing the new Microsoft Edge web browser"
keywords             = "edge"
licenses             = (("License\nnUNKNOWN","https://www.microsoft.com/en-us/edge?exp=e01&form=MA13FJ"),)
website              = ("WebSite","https://www.microsoft.com/en-us/edge?exp=e01&form=MA13FJ")
                


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="edge.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Microsoft Edge Failed",
                            ifremovefailmsg="Remove Microsoft Edge Failed",
                            parallel_install=False)


    def check(self):
        return not os.path.isfile("/usr/bin/microsoft-edge-stable")
        
    def install(self):
        if os.path.isfile("/etc/yum.repos.d/microsoft-edge-beta.repo"):
            commands = ["dnf install microsoft-edge-stable -y --best"]
        else:
            commands = ["dnf config-manager --add-repo https://packages.microsoft.com/yumrepos/edge",
            "rpm --import https://packages.microsoft.com/keys/microsoft.asc",
            "dnf install microsoft-edge-stable -y --best"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e microsoft-edge-stable",shell=True)==0:
            return True
        return False


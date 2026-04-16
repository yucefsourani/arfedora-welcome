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
arch                 = ("x86_64",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Developer Tools"
category_icon_theme  = "applications-science-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Antigravity"
subtitle             = "Google Antigravity"
keywords             = "google ai ide antigravity"
licenses             = (("License\nUNKNOWN","https://antigravity.google/"),)
website              = ("WebSite","https://antigravity.google/")
                

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="Google-Antigravity-Icon-Full-Color.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Antigravity Failed",
                            ifremovefailmsg="Remove Antigravity Failed",
                            parallel_install=False)


    def check(self):
        return not os.path.isfile("/usr/bin/antigravity")
        
    def install(self):
        if os.path.isfile("/etc/yum.repos.d/antigravity.repo"):
            commands = ["dnf install antigravity -y --best"]
        else:
            commands = ["echo -e '[antigravity-rpm]\nname=Antigravity RPM Repository\nbaseurl=https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm\nenabled=1\ntype=rpm\ngpgcheck=0' > /etc/yum.repos.d/antigravity.repo",
            "dnf install antigravity -y --best"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e antigravity",shell=True)==0:
            return True
        return False


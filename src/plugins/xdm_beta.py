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
title                = "Xdman <span color='red'>Beta</span>"
subtitle             = "Xtreme Download Manager"
keywords             = "downloder xdman"
licenses             = (("License\nGPLv3+","https://www.gnu.org/licenses/gpl-3.0.html"),)
website              = ("WebSite","https://github.com/subhra74/xdm")





class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="xdman.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove Xdman Failed",
                            ifinstallfailmsg="Install Xdman Failed",
                            ifinstallsucessmsg="Install Xdman Done",
                            ifremovesucessmsg="Remove Xdman Done",
                            parallel_install = False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        return not subprocess.call("rpm -q xdman_gtk",shell=True) == 0
        
    def install(self):
        link_pro = "https://github.com/subhra74/xdm/releases/download/8.0.26/xdman_gtk-8.0.29-1.fc36.x86_64.rpm"
        commands = []
        if os.path.isfile("/opt/xdman/uninstall.sh"):
            print("Remove Old Version")
            commands += ["chmod 755 /opt/xdman/uninstall.sh", "/opt/xdman/uninstall.sh"]
        commands.append("dnf install {} -y --best".format(link_pro))
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e xdman_gtk",shell=True)==0:
            return True
        return False

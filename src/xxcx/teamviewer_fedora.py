#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xdm.py
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
from arfedora_welcome import utils
from arfedora_welcome.classesplugin import BasePlugin
from arfedora_welcome.utils import get_uniq_name,write_to_tmp
import subprocess


if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Utils"
category_icon_theme  = "applications-utilities-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "TeamViewer"
subtitle             = "Remote access, control and support software"
keywords             = "remote desktop teamviewer"
licenses             = (("License\nProprietary","https://www.teamviewer.com/"),)
website              = ("WebSite","https://www.teamviewer.com/")
                


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="Team_Viewer.png",
                            button_install_label="Install ",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove TeamViewer Failed",
                            ifinstallfailmsg="Install TeamViewer Failed",
                            ifinstallsucessmsg="Install TeamViewer Done",
                            ifremovesucessmsg="Remove TeamViewer Done",
                            beforeinstallyesorno="Start Install TeamViewer ?",
                            beforeremoveyesorno="Start Remove TeamViewer ?",
                            parallel_install=False,
                            daemon=True)


        
    def check(self):
        return not  utils.check_rpm_package_exists("teamviewer")
        
    def install(self):
        arch = os.uname().machine
        if arch=="x86_64":
            link_pro = "https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm"
        else:
            link_pro = "https://download.teamviewer.com/download/linux/teamviewer.i686.rpm"

        if subprocess.call("pkexec dnf install {} -y --best -v".format(link_pro),shell=True)!=0:
            return False

        return True
        
    def remove(self):
        if subprocess.call("pkexec rpm -v --nodeps -e teamviewer",shell=True)!=0:
            return False
        return True



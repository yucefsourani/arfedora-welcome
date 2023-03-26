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
from arfedora_welcome.classesplugin import BasePlugin
from arfedora_welcome.utils import get_uniq_name,write_to_tmp,DownloadFile
import subprocess
import tempfile
from arfedora_welcome import gui_widgets
import os
                
if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("all",)
distro_version       = ("all",)
category             = "Internet"
category_icon_theme  = "web-browser-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Xdman"
subtitle             = "Xtreme Download Manager"
keywords             = "downloder xdman"
licenses             = (("License\nGPL V2.0","https://www.gnu.org/licenses/gpl-2.0.html"),)
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
                            beforeinstallyesorno="Start Install Xdman ?",
                            beforeremoveyesorno="Start Remove Xdman ?",
                            parallel_install = True,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        return not os.path.isfile("/opt/xdman/uninstall.sh")
        
    def install(self):
        temp     = tempfile.gettempdir()
        link_pro = "https://github.com/subhra74/xdm/releases/download/7.2.11/xdm-setup-7.2.11.tar.xz"
        d = DownloadFile(self,link_pro)
        pro_saveas = d.start()
        if not pro_saveas:
            print("Download Failed.")
            return False
        old_dir = os.getcwd()
        os.chdir(temp)
        if subprocess.call("tar -xJf {}".format(pro_saveas),shell=True)!=0:
            print("Extract {} Failed.".format(pro_saveas))
            gui_widgets.create_toast("Extract {} Failed.".format(pro_saveas),1)
            os.chdir(old_dir)
            return False
        os.chdir(old_dir)
        install_file = os.path.join(temp,"install.sh")
        if subprocess.call("chmod 755 {}".format(install_file),shell=True)!=0:
            print("'chmod 755 {}' Failed.".format(install_file))
            gui_widgets.create_toast("'chmod 755 {}' Failed.".format(install_file),1)
            return False
        if subprocess.call("pkexec {}".format(install_file),shell=True)!=0:
            return False

        return True
        
    def remove(self):
        commands = ["chmod 755 /opt/xdman/uninstall.sh", "/opt/xdman/uninstall.sh"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
            return False
        return True

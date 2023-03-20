#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ArduinoIDE.py
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


if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("all",)
distro_version       = ("all",)
category             = "Developer Tools"
category_icon_theme  = "applications-developmen-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Arduino"
subtitle             = "Open-source electronics prototyping platform\n(Flatpak User Wide)"
keywords             = "arduino electronics"
licenses             = (("License\nLGPL V2.1","https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html"),)
website              = ("WebSite","https://www.arduino.cc/")


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="arduino.svg",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove Arduino IDE Failed",
                            ifinstallfailmsg="Install Arduino IDE Failed",
                            ifinstallsucessmsg="Install Arduino IDE Done\n\n<span foreground=\"red\">Reboot Your System</span>",
                            ifremovesucessmsg="Remove Arduino IDE Done",
                            beforeinstallyesorno="Start Install Arduino IDE?",
                            beforeremoveyesorno="Start Remove Arduino IDE?",
                            parallel_install = False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        self.package_name = "cc.arduino.arduinoide"
        return not self.check_package(self.package_name)
        
    def install(self):
        if not self.check_repo("flathub"):
            if subprocess.call("flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo --user",shell=True) !=0:
                print("Add Flathub repo Failed.")
                return False
        
        if subprocess.call("flatpak --user install flathub {} -y".format(self.package_name),shell=True)==0:
            commands = ["usermod -G dialout -a $USER"]
            to_run = write_to_tmp(commands)
            subprocess.call("pkexec bash  {}".format(to_run),shell=True)
            return True
        return False
        
    def remove(self):
        try:
            if subprocess.call("flatpak --user remove {} -y".format(self.package_name),stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        except:
            if subprocess.call("pkexec flatpak  remove {} -y".format(self.package_name),stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        return False
        
    def check_package(self,package_name):
        if subprocess.call("flatpak list  --app |grep {}".format(package_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False

    def check_repo(self,repo_name):
        if subprocess.call("flatpak --user remote-list  |grep {}".format(repo_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False

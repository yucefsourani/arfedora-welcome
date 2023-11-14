#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gimp_fedora.py
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
type_                = "installer"
arch                 = ("all",)
distro_name          = ("all",)
distro_version       = ("all",)
category             = "Graphics"
category_icon_theme  = "applications-graphics-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Gimp <span color='red'>Beta</span>"
subtitle             = "GIMP is an acronym for GNU Image Manipulation Program\n(Flatpak User wide)"
keywords             = "gimp"
licenses             = (("License\nGPL v3.0+","https://www.gnu.org/licenses/gpl-3.0.html"),("License\nLGPL-3.0+","https://www.gnu.org/licenses/lgpl-3.0.en.html"))
website              = ("WebSite","https://www.gimp.org/")
                


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="gimp.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove gimp beta Failed",
                            ifinstallfailmsg="Install gimp beta Failed",
                            ifinstallsucessmsg="Install gimp beta Done",
                            ifremovesucessmsg="Remove gimp beta Done",
                            beforeinstallyesorno="Start Install gimp beta ?",
                            beforeremoveyesorno="Start Remove gimp beta ?",
                            parallel_install = False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        self.package_name = "org.gimp.GIMP"
        return not self.check_package(self.package_name)
        
    def install(self):
        if not self.check_repo("flathub-beta"):
            if subprocess.call("flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo --user",shell=True) !=0:
                print("Add Flathub Beta repo Failed.")
                return False
        
        if subprocess.call("flatpak --user install flathub-beta {} -y".format(self.package_name),shell=True)==0:
            return True
        return False
        
    def remove(self):
        try:
            if subprocess.call("flatpak --user remove org.gimp.GIMP//beta -y",stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        except:
            if subprocess.call("pkexec flatpak  remove org.gimp.GIMP//beta -y",stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        return False
        
    def check_package(self,package_name):
        if subprocess.call("flatpak list  --app |grep {} |grep -i beta".format(package_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False

    def check_repo(self,repo_name):
        if subprocess.call("flatpak --user remote-list  |grep {}".format(repo_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  geany_fedora.py
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
category             = "Developer Tools"
category_icon_theme  = "applications-science-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Geany"
subtitle             = "A fast and lightweight IDE using GTK3"
keywords             = "geany"
licenses             = (("License\nProprietary","https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"),)
website              = ("WebSite","https://geany.org/")

all_package = ["geany-themes","geany","xterm"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="geany.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Geany Failed",
                            ifremovefailmsg="Remove Geany Failed",
                            parallel_install=False)


    def check(self):
        check_package = all([utils.check_rpm_package_exists(pack) for pack in ["geany","geany-libgeany"]])
        return not check_package     
         
    def install(self):
        to_install = [pack for pack in all_package if not utils.check_rpm_package_exists(pack)]
        to_install = " ".join(to_install)
        if subprocess.call("pkexec dnf install {} -y --best".format(to_install),shell=True)==0:
            return True
        return False
        
    def remove(self):
        to_remove = " ".join([pack for pack in ["geany","geany-libgeany"] if utils.check_rpm_package_exists(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False

        

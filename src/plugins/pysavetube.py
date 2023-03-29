#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pyfbdown.py
#  
#  Copyright 2021 youcef sourani <youssef.m.sourani@gmail.com>
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

if_true_skip         = True # skip
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Multimedia"
category_icon_theme  = "applications-multimedia-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Pysavetube"
subtitle             = "Videos Dowloader"
keywords             = "video pysavetube"
licenses             = (("License\nGPL-3.0","https://www.gnu.org/licenses/gpl-3.0.html"),)
website              = ("WebSite","https://github.com/yucefsourani/pysavetube")

all_package = ["pysavetube"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="com.github.yucefsourani.pysavetube.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install pysavetube Failed",
                            ifremovefailmsg="Remove pysavetube Failed",
                            parallel_install=False)


        
        
    def check(self):
        check_package = all([utils.check_rpm_package_exists(pack) for pack in all_package])
        return not check_package
        
    def install(self):
        to_install = [pack for pack in all_package if not utils.check_rpm_package_exists(pack)]
        to_install = " ".join(to_install)
        if os.path.isfile("/etc/yum.repos.d/_copr:copr.fedorainfracloud.org:youssefmsourani:pysavetube.repo"):
            commands = ["dnf install {} -y --best".format(to_install)]
        else:
            commands = ["dnf copr enable youssefmsourani/pysavetube -y","dnf install {} -y --best".format(to_install)]

        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        to_remove = " ".join([pack for pack in all_package if utils.check_rpm_package_exists(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False

        

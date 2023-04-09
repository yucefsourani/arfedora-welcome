#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mesa_vdpau_drivers_freeworld.py
#  
#  Copyright 2023 yucef sourani <yuceff28@fedora>
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
import os

if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Multimedia"
category_icon_theme  = "applications-multimedia-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Mesa va drivers(INTEL)"
subtitle             = "(freeworld) Drivers contains video acceleration codecs for decoding/encoding H.264 and H.265"
keywords             = "mesa driver"
licenses             = (("License\nUNKNOWN",""),)
website              = ("WebSite","https://www.mesa3d.org/")


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="T3-SiBhZ.svg",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Mesa va drivers freeworld Failed",
                            ifremovefailmsg="Remove Mesa va drivers freeworld Failed",
                            parallel_install=False)


        
        
    def check(self):
        return  not utils.check_rpm_package_exists("mesa-va-drivers-freeworld") 
        
    def install(self):
        rpmfusion  = all([ utils.check_rpm_package_exists(pack) for pack in ["rpmfusion-nonfree-release", "rpmfusion-free-release"]])
        
        if utils.check_rpm_package_exists("mesa-va-drivers"):
            commands = ["dnf swap  mesa-va-drivers mesa-va-drivers-freeworld -y --best"]
        else:
            commands = ["dnf install  mesa-va-drivers-freeworld  -y --best"]

        if not rpmfusion:
            d_version = utils.get_distro_version()
            command_to_install_rpmfusion = "dnf install  --best -y --nogpgcheck  \
    http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{}.noarch.rpm \
    http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{}.noarch.rpm".format(d_version,d_version)
            commands.insert(0,command_to_install_rpmfusion)
        to_run = write_to_tmp(commands)

        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if utils.check_rpm_package_exists("mesa-vdpau-drivers-freeworld"):
            result = subprocess.call("pkexec rpm -v --nodeps -e mesa-va-drivers-freeworld",shell=True)
        else:
            result = subprocess.call("pkexec dnf swap mesa-va-drivers-freeworld mesa-va-drivers  -y --best",shell=True)
        if result==0:
            return True
        return False

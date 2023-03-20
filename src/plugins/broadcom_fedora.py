#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  broadcom_fedora.py
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
from arfedra_welcome import utils
from arfedora_welcome.classesplugin import BasePlugin
from arfedora_welcome.utils import get_uniq_name,write_to_tmp
import subprocess

if_true_skip         = False
type_                = "installer"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "System"
category_icon_theme  = "applications-system-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Broadcom"
subtitle             = "Driver For Broadcom wifi"
keywords             = "driver wifi broadcom"
licenses             = (("License\nUNKNOWN","https://www.broadcom.com/"),)
website              = ("WebSite","https://www.broadcom.com/")
               

def issecureboot():
    out = subprocess.Popen("mokutil --sb-state &>/dev/null",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    if out == "SecureBoot enabled":
        return True
    else:
        return False

if os.path.isfile("/usr/bin/mokutil"):
    secureboot = issecureboot()
else:
    secureboot = None

ifinstallsucessmsg = "Install Broadcom Wifi Driver Sucess\n\n<span foreground=\"red\">Update Your System And Reboot</span>"
if secureboot:
    ifinstallsucessmsg = ifinstallsucessmsg+"\n\n<span foreground=\"red\">And Disable Secure Boot</span>"

elif secureboot==None:
    ifinstallsucessmsg = ifinstallsucessmsg+"\n\n<span foreground=\"red\">And Check Secure Boot If Disabled</span>"

all_package = ["akmod-wl", "broadcom-wl"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="broadcom.jpg",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Broadcom Wifi Driver Failed",
                            ifremovefailmsg="Remove Broadcom Wifi Driver Failed",
                            ifinstallsucessmsg=ifinstallsucessmsg,
                            parallel_install=False)


        
        
    def check(self):
        check_package = all([ utils.check_rpm_package_exists(pack) for pack in all_package])
        return not check_package
        
    def install(self):
        rpmfusion  = all([  utils.check_rpm_package_exists(pack) for pack in ["rpmfusion-nonfree-release", "rpmfusion-free-release"]])
        to_install = [pack for pack in all_package if not  utils.check_rpm_package_exists(pack)] + ["kernel", "kernel-devel", "kernel-headers", "@c-development"]
        to_install = " ".join(to_install)
        commands = ["dnf install {} -y --best".format(to_install)]
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
        to_remove = " ".join([pack for pack in all_package if  utils.check_rpm_package_exists(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False



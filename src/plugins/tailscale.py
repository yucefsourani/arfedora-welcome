#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tailscale.py
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
category             = "Internet"
category_icon_theme  = "web-browser-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Tailscale"
subtitle             = "VPN cross platform way to use WireGuard + oauth2 + 2FA/SSO"
keywords             = "vpn tailscale"
licenses             = (("License\nUNKNOWN","https://github.com/tailscale/tailscale"),)
website              = ("WebSite","https://tailscale.com")
                

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="tailscale.png",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Tailscale Failed",
                            ifremovefailmsg="Remove Tailscale Failed",
                            parallel_install=False)


    def check(self):
        return not os.path.isfile("/usr/bin/tailscale")
        
    def install(self):
        if os.path.isfile("/etc/yum.repos.d/tailscale.repo"):
            commands = ["dnf install tailscale -y --best"]
        else:
            commands = ["echo -e '[tailscale-stable]\nname=Tailscale stable\nbaseurl=https://pkgs.tailscale.com/stable/fedora/$basearch\nenabled=1\ntype=rpm\nrepo_gpgcheck=1\ngpgcheck=1\ngpgkey=https://pkgs.tailscale.com/stable/fedora/repo.gpg' > /etc/yum.repos.d/tailscale.repo",
            "rpm --import https://pkgs.tailscale.com/stable/fedora/repo.gpg",
            "dnf install tailscale -y --best"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e tailscale",shell=True)==0:
            return True
        return False


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  codecs_fedora.py
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
distro_version       = ("43","44","45","46")
category             = "Multimedia"
category_icon_theme  = "applications-multimedia-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Codecs"
subtitle             = "Multimedia coder/decoder"
keywords             = "mp4 mp3 codecs"
licenses             = (("License\nUNKNOWN",""),)
website              = ()




all_package_to_install = ['ffmpeg', 'ffmpeg-libs', 'gstreamer1-plugins-bad-free-extras']

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="codecs.png",
                            button_install_label="Run",
                            button_remove_label="Run",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Codecs Failed",
                            ifremovefailmsg="",
                            parallel_install=False)


        
        
    def check(self):
        return True # make onshot
        
    def install(self):
        commands   = ["dnf group install multimedia -y --best"]
        rpmfusion  = all([ utils.check_rpm_package_exists(pack) for pack in ["rpmfusion-nonfree-release", "rpmfusion-free-release"]])
        to_install = [pack for pack in all_package_to_install if not utils.check_rpm_package_exists(pack)]
        if to_install:
            to_install = " ".join(to_install)
            commands   += [f"dnf install {to_install} -y --best"] 

        to_remove = ""
        for p in (" ffmpeg-free ", " libavcodec-free ", " libavdevice-free ", " libavfilter-free ", " libavformat-free " ," libavutil-free ", " libpostproc-free ", " libswresample-free ", " libswscale-free ") :
            if utils.check_rpm_package_exists(p):
                to_remove += p
        if to_remove:
            commands.insert(0,"rpm -v --nodeps -e {}".format(to_remove))
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
        return True

        


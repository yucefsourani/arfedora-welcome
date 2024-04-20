#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fonts_fedora.py
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
category             = "System"
category_icon_theme  = "applications-system-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
title                = "Fonts"
subtitle             = "Fonts For Arabic Language"
keywords             = "font"
licenses             = (("License\nUNKNOWN",""),)
website              = ()

all_package_to_remove = [ 'kacst-art-fonts', 'kacst-book-fonts',
                          'kacst-decorative-fonts',
                          'kacst-digital-fonts', 'kacst-farsi-fonts',
                          'kacst-letter-fonts', 'kacst-naskh-fonts', 
                          'kacst-office-fonts', 'kacst-one-fonts', 
                          'kacst-pen-fonts', 'kacst-poster-fonts', 
                          'kacst-qurn-fonts', 'kacst-screen-fonts', 
                          'kacst-title-fonts', 'kacst-titlel-fonts', 
                          'paktype-naqsh-fonts', 
                          'paktype-tehreer-fonts',
                          'sil-lateef-fonts', 
                          'google-noto-sans-arabic-fonts', 
                          'google-noto-naskh-arabic-fonts', 
                          'google-noto-naskh-arabic-ui-fonts', 
                          'google-noto-sans-old-south-arabian-fonts',
                          'amiri-quran-fonts',
                          'amiri-fonts',
                          'amiri-quran-colored-fonts']

all_package_to_install = ['dejavu-sans-fonts', 'dejavu-sans-mono-fonts',
                          'kacst-art-fonts', 'kacst-book-fonts',
                          'kacst-decorative-fonts',
                          'kacst-digital-fonts', 'kacst-farsi-fonts',
                          'kacst-letter-fonts', 'kacst-naskh-fonts', 
                          'kacst-office-fonts', 'kacst-one-fonts', 
                          'kacst-pen-fonts', 'kacst-poster-fonts', 
                          'kacst-qurn-fonts', 'kacst-screen-fonts', 
                          'kacst-title-fonts', 'kacst-titlel-fonts', 
                          'paktype-naqsh-fonts', 
                          'paktype-tehreer-fonts',
                          'sil-lateef-fonts', 
                          'google-noto-sans-arabic-fonts', 
                          'google-noto-naskh-arabic-fonts', 
                          'google-noto-naskh-arabic-ui-fonts', 
                          'google-noto-sans-old-south-arabian-fonts',
                          'amiri-quran-fonts',
                          'amiri-fonts',
                          'amiri-quran-colored-fonts']
               


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent,threads):
        BasePlugin.__init__(self,parent=parent,
                            threads=threads,
                            button_image="kacsttitle.gif",
                            button_install_label="Install",
                            button_remove_label="Remove",
                            button_frame=False,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Arabic Fonts Failed",
                            ifremovefailmsg="Remove Arabic Fonts Failed",
                            parallel_install=False)


        
        
    def check(self):
        check_package = all([utils.check_rpm_package_exists(pack) for pack in all_package_to_install])
        return not check_package
        
    def install(self):
        to_install = [pack for pack in all_package_to_install if not utils.check_rpm_package_exists(pack)]
        to_install = " ".join(to_install)
        if subprocess.call("pkexec dnf install {} -y --best".format(to_install),shell=True)==0:
            return True
        return False
        
    def remove(self):
        to_remove = " ".join([pack for pack in all_package_to_remove if utils.check_rpm_package_exists(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False

        

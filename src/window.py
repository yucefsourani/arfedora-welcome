# window.py
#
# Copyright 2023 yucef
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from gi.repository import Adw
from gi.repository import Gtk,GObject,Gio,Gdk
from .about        import AboutPage
from .main_page    import MainPage
from .output_page  import OutPutPage
from .utils        import css
from .gui_widgets  import yes_or_no
import threading



class ArfedoraWelcomeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ArfedoraWelcomeWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Arfedora Welcome")
        self.connect("close-request", self.quit_)
        style_provider = Gtk.CssProvider()
        if (Gtk.get_major_version(), Gtk.get_minor_version()) >= (4, 9):
            style_provider.load_from_data(css.decode("utf-8"), -1)
        else:
            style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display().get_default(),
                                                 style_provider, 
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.app_settings = Gio.Settings.new_with_path("com.github.yucefsourani.Arfedorawelcome","/com/github/yucefsourani/Arfedorawelcome/")
        self._vte = self.app_settings.get_boolean("vte")
        self.app_settings.bind("width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-fullscreen", self, "fullscreened",
                           Gio.SettingsBindFlags.DEFAULT)

        self.mainbox = Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        self.mainbox.props.hexpand = True
        self.mainbox.props.vexpand = True
        self.banner = Gtk.Overlay.new()
        self.set_content(self.banner)
        self.make_header()



            
    def make_header(self):
        self.header = Adw.HeaderBar.new()
        
        self.view_switcher_bar = Adw.ViewSwitcherBar.new()
        self.view_switcher_title = Adw.ViewSwitcherTitle.new()
        self.mainstack = Adw.ViewStack.new()
        self.mainstack.set_hexpand(True)
        self.mainstack.set_vexpand(True)


        self.main_page = MainPage(self)
        self.aboutbox  = AboutPage(self)
        self.outputbox = OutPutPage(self)
        self.mainstack.add_titled_with_icon(self.main_page.mbox,"mhbox",_("Main"),"application-x-executable-symbolic")
        self.mainstack.add_titled_with_icon(self.outputbox.mbox,"output",_("Output"),"utilities-terminal-symbolic")
        self.mainstack.add_titled_with_icon(self.aboutbox.mbox,"aboutbox",_("About"),"help-about-symbolic")

        self.app_settings.bind("visible-stack-child", self.mainstack, "visible-child-name",
                           Gio.SettingsBindFlags.DEFAULT)
        
        self.view_switcher_title.set_stack(self.mainstack)
        self.header.set_title_widget(self.view_switcher_title)

        
        self.view_switcher_bar.set_stack(self.mainstack)
        

        self.mainbox.append(self.header)
        
        self.banner.set_child(self.mainbox)
        self.mainbox.append(self.mainstack)
        self.mainbox.append(self.view_switcher_bar)
        self.view_switcher_title.bind_property("title_visible",self.view_switcher_bar, "reveal",GObject.BindingFlags.DEFAULT )

    def quit_(self,window):
        if threading.active_count()>1:
            dt = [t for t in threading.enumerate()[1:] if not t.daemon]
            if dt:
                print("Threads Not Daemon Running Wait To Finish.")
                for t in dt:
                    print(t)
                return True
            else:
                infobar2 = yes_or_no(self.banner,"Tasks Running In Background,Are You Sure You Want To Exit?",
                                     func=self.quit__)
                return True
        return False
        
    def quit__(self):
        self.get_application().quit()


from gi.repository import Adw
from gi.repository import Gtk

avatar_size    = 160
app_title      = "Arfedora Welcome"
app_icon_name  = "com.github.yucefsourani.Arfedorawelcome"
dev_name       = "Yucef"
app_copyright  = "© 2023 yucef"
app_version    = "1.0"
app_website    = "https://github.com/yucefsourani/arfedora-welcome"
app_license    = ("https://www.gnu.org/licenses/gpl-3.0.html","License GPL V3.0")
license_text   = """
Copyright (C) 2023  yucef sourani <youssef.m.sourani@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

developer_names = [
                 ["yucef mouhammad nazih  sourani","https://github.com/yucefsourani"]
                ]

translator_names = []

class AboutPage():
    def __init__(self,parent):
        self.parent  = parent
        self.mbox    = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)

        viewswitcher_clamp = Adw.Clamp.new()
        viewswitcher_clamp.props.margin_bottom = 15
        viewswitcher_clamp.props.margin_top    = 5
        viewswitcher_clamp.props.margin_start  = 5
        viewswitcher_clamp.props.margin_end    = 5
        viewswitcher_clamp.set_maximum_size(400)
        viewswitcher = Adw.ViewSwitcher.new()
        viewswitcher_clamp.set_child(viewswitcher)
        self.mbox.append(viewswitcher_clamp)
        mainstack = Adw.ViewStack.new()
        viewswitcher.set_css_classes(["wide","linked"])
        viewswitcher.set_stack(mainstack)
        mainstack.props.hexpand = True
        mainstack.props.vexpand = True
        self.mbox.append(mainstack)


        mainsw = Gtk.ScrolledWindow.new()
        mainstack.add_titled_with_icon(mainsw,"info","Info","dialog-information-symbolic")
        mainsw.set_policy( Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box  = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)
        mainsw.set_child(box)
        box.props.margin_bottom = 5
        box.props.margin_top    = 10
        box.props.margin_start  = 5
        box.props.margin_end    = 5
        aboutpage = Adw.Avatar.new(avatar_size,app_title,False)
        aboutpage.set_icon_name(app_icon_name)


        box.append(aboutpage)
        application_name = Gtk.Label.new(app_title)
        application_name.add_css_class("title-2")
        box.append(application_name)

        developer_name = Gtk.Label.new(dev_name)
        developer_name.add_css_class("title-4")
        box.append(developer_name)

        copyright = Gtk.Label.new(app_copyright)
        box.append(copyright)

        versionbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL,spacing=0)
        versionbox.set_halign(Gtk.Align.CENTER)
        version = Gtk.Button.new()
        versionbox.append(version)
        version.props.hexpand = False
        version.props.label = app_version
        version.add_css_class("pill")
        version.add_css_class("accent")
        box.append(versionbox)
        website_b =  Gtk.LinkButton.new_with_label(app_website,"Website")
        box.append(website_b)

        license_b =  Gtk.LinkButton.new_with_label(*app_license)
        box.append(license_b)

        license_clamp = Adw.Clamp.new()
        license_clamp.props.margin_bottom = 15
        license_clamp.set_maximum_size(500)
        box.append(license_clamp)

        license_textview = Gtk.TextView.new()
        license_textview.props.vexpand  = True
        license_textview.add_css_class("caption")
        license_textview.props.justification = Gtk.Justification.CENTER
        license_textview.props.wrap_mode  =  Gtk.WrapMode.WORD
        license_textview.props.editable = False
        license_clamp.set_child(license_textview)
        textview_buffer  = license_textview.get_buffer()
        textview_buffer.set_text(license_text)



        #################################################################################################
        greditssw = Gtk.ScrolledWindow.new()
        mainstack.add_titled_with_icon(greditssw,"gredits","Gredits","applications-science-symbolic")

        greditsbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=20)
        greditssw.set_child(greditsbox)

        developer_listbox_clamp = Adw.Clamp.new()
        developer_listbox_clamp.props.margin_bottom = 15
        developer_listbox_clamp.props.margin_top    = 5
        developer_listbox_clamp.props.margin_start  = 5
        developer_listbox_clamp.props.margin_end    = 5
        developer_listbox_clamp.set_maximum_size(500)
        developer_listbox  = Gtk.ListBox.new()
        developer_listbox.set_show_separators(True)

        developer_listbox_clamp.set_child(developer_listbox)
        developer_listbox.set_css_classes(["boxed-list"])
        developer_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        greditsbox.append(developer_listbox_clamp)


        for i in developer_names:
            row =  Adw.ActionRow.new()
            row.add_suffix( Gtk.LinkButton.new_with_label(i[1],"Website"))
            row.set_title("Developers")
            row.set_title_lines(1)
            row.set_subtitle(i[0])
            row.set_subtitle_lines(4)
            row.set_icon_name("accessories-text-editor-symbolic")
            #row.set_icon_name("lang-typedef-symbolic")
            developer_listbox.append(row)


        translator_listbox_clamp = Adw.Clamp.new()
        translator_listbox_clamp.props.margin_bottom = 15
        translator_listbox_clamp.props.margin_top    = 5
        translator_listbox_clamp.props.margin_start  = 5
        translator_listbox_clamp.props.margin_end    = 5
        translator_listbox_clamp.set_maximum_size(500)
        translator_listbox  = Gtk.ListBox.new()
        translator_listbox.set_show_separators(True)

        translator_listbox_clamp.set_child(translator_listbox)
        translator_listbox.set_css_classes(["boxed-list"])
        translator_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        greditsbox.append(translator_listbox_clamp)


        for i in translator_names:
            row =  Adw.ActionRow.new()
            row.add_suffix( Gtk.LinkButton.new_with_label(i[1],"Website"))
            row.set_title("Translators")
            row.set_title_lines(1)
            row.set_subtitle(i[0])
            row.set_subtitle_lines(4)
            row.set_icon_name("accessories-text-editor-symbolic")
            translator_listbox.append(row)








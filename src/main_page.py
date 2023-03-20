from gi.repository import Adw
from gi.repository import Gtk,GdkPixbuf,Gdk,Gio
from .utils import arch,get_distro_name_like,get_distro_version,get_plugins,load_plugin,display_type,distro_desktop,get_image_location
from .gui_widgets import IconNamePaint,infooverlay,yes_or_no

WIDTH  = 32
HEIGHT = 32


class MainPage():
    def __new__(cls):
        s = super(MainPage, cls).__new__(cls)
        s.__init__()
        return s.mbox

    def __init__(self):
        self.main_overlay  = Gtk.Overlay.new()
        self.mbox     = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=0)
        self.mainbox  = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)
        self.mbox.set_hexpand(True)
        self.mbox.set_vexpand(True)
        self.mainbox.set_hexpand(True)
        self.mainbox.set_vexpand(True)
        self.mbox.append(infooverlay)
        infooverlay.set_child(self.mainbox)
                
        self.flap = Adw.Flap.new()
        self.mbox.flap = self.flap
        self.flap.set_hexpand(True)
        self.flap.set_vexpand(True)
        self.mainbox.append(self.flap)
        
        view_switcher_box  = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)
        #view_switcher_box.set_hexpand(True)
        view_switcher_box.set_vexpand(True)
        view_switcher_sw   = Gtk.ScrolledWindow.new()
        #view_switcher_sw.set_hexpand(True)
        view_switcher_sw.set_vexpand(True)
        view_switcher_sw.set_policy( Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.main_stack = Gtk.Stack.new()
        self.main_stack.set_hexpand(True)
        self.main_stack.set_vexpand(True)
        self.view_switcher_listbox = Gtk.ListBox.new()
        self.view_switcher_listbox.set_css_classes(["navigation-sidebar","background"])
        self.view_switcher_listbox.set_selection_mode( Gtk.SelectionMode.SINGLE )
        self.view_switcher_listbox.set_activate_on_single_click( True )
        self.view_switcher_listbox.connect("row-activated",self.on_view_switcher_row_activated)
        #self.view_switcher = Adw.ViewSwitcher.new()
        #self.view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE )
        #self.view_switcher.set_hexpand(True)
        #self.view_switcher.set_vexpand(True)
        view_switcher_sw.set_child(self.view_switcher_listbox)
        view_switcher_box.append(view_switcher_sw)
        #self.view_switcher.set_stack(self.main_stack)
        
        self.flap.set_flap(view_switcher_box)
        self.flap.set_content(self.main_stack)
        
        self.all_category   = {}
        self.switchcategory = {}
        self.threads        = dict()
        self.loading_all_plugins()
        

    def on_view_switcher_row_activated(self,list_box, row):
        page_name = row.get_child().stack_page_name
        self.main_stack.set_visible_child_name(page_name)
        
    def loading_all_plugins(self):
        distro_name    = get_distro_name_like()
        distro_version = get_distro_version()
        all_plugins    = get_plugins()

        for module_name in all_plugins:
            plugin = load_plugin(module_name)
            if not plugin:
                continue
            try:
                if plugin.if_true_skip:
                    continue
                if "all" not in plugin.desktop_env:
                    if distro_desktop not in plugin.desktop_env:
                        contine
                if "all" not in plugin.display_type:
                    if display_type not in plugin.display_type:
                        contine
                if "all" not in plugin.arch:
                    if arch not in plugin.arch:
                        continue
                if "all" not in plugin.distro_name:
                    if not any([i for i in plugin.distro_name if i in distro_name]):
                        continue
                if "all" not in plugin.distro_version:
                    if distro_version not in plugin.distro_version:
                        continue
                if plugin.category not in self.all_category.keys():
                    banner = Gtk.Overlay.new()
                    box  = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=5)
                    banner.set_child(box)
                    sw = Gtk.ScrolledWindow.new()
                    #box.set_hexpand(True)
                    box.set_vexpand(True)
                    listbox = Gtk.ListBox.new()
                    listbox.set_css_classes(["boxed-list"])
                    listbox.set_selection_mode(Gtk.SelectionMode.NONE)
                    #listbox.set_show_separators(True)
                    
                    searchentry = Gtk.SearchEntry.new()
                    searchlistbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL,spacing=0)
                    searchlistbox.props.margin_top    = 10
                    searchlistbox.set_css_classes(["toolbar"])
                    searchlistbox.set_halign(Gtk.Align.CENTER)
                    #searchlistbox = Gtk.ListBox.new()
                    #searchlistbox.set_css_classes(["frame"])
                    #searchlistbox.set_selection_mode(Gtk.SelectionMode.NONE)
                    #searchlistbox.set_show_separators(True)
                    #searchclamp = Adw.Clamp.new()
                    #searchclamp.props.margin_top    = 10
                    #searchclamp.props.margin_bottom = 3
                    #searchclamp.props.margin_start  = 5
                    #searchclamp.props.margin_end    = 5
                    #searchclamp.set_maximum_size(500)
                    #searchclamp.set_child(searchlistbox)
                    #box.append(searchclamp)
                    box.append(searchlistbox)
                    searchbar    = Gtk.SearchBar.new()
                    searchbar.set_css_classes(["toolbar"])
                    #searchbarrow = Adw.ActionRow.new()
                    #searchbarrow.set_child(searchbar)
                    #searchbar.set_hexpand(True)
                    #searchlistbox.append(searchbarrow)
                    searchlistbox.append(searchbar)
                    #searchbar.props.margin_top    = 3
                    #searchbar.props.margin_bottom = 3
                    #searchbar.props.margin_start  = 3
                    #searchbar.props.margin_end    = 3 
                    searchbar.set_search_mode(True)
                    searchbar.connect_entry(searchentry)
                    searchbar.set_child(searchentry)
                    searchbar.set_key_capture_widget(listbox)

                    clamp = Adw.Clamp.new()
                    clamp.set_vexpand(True)
                    clamp.props.margin_top    = 3
                    clamp.props.margin_bottom = 10
                    clamp.props.margin_start  = 5
                    clamp.props.margin_end    = 5
                    clamp.set_maximum_size(500)
                    clamp.set_child(listbox)
                    sw.set_child(clamp)
                    box.append(sw)
                    self.main_stack.add_titled(banner,plugin.category,plugin.category)
                    
                    listbox.set_filter_func(self.on_filter_invalidate,searchentry)
                    searchentry.connect("search_changed",self.on_search_entry_changed,listbox)
                    
                    category_box = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=0)
                    category_box.stack_page_name = plugin.category
                    category_box.set_homogeneous(True)
                    category_box.props.margin_start  = 3
                    category_box.props.margin_end    = 3
                    category_box.props.margin_top    = 3
                    category_box.props.margin_bottom = 3
                    
                    image = IconNamePaint(plugin.category_icon_theme,25,25,category_box)
                    image.props.halign  = Gtk.Align.CENTER
                    category_box.append(image)
                    category_label = Gtk.Label.new()
                    category_label.add_css_class("caption")
                    category_label.props.hexpand = True
                    category_label.props.halign  = Gtk.Align.CENTER
                    category_box.append(category_label)
                    category_label.props.label = plugin.category
                    self.view_switcher_listbox.append(category_box)
                    category_label.props.use_markup=True
                    category_label.set_markup(plugin.category)
                    self.all_category.setdefault(plugin.category,[listbox,banner])
                else:
                    listbox,banner =  self.all_category[plugin.category]
                if plugin.type_ == "installer":
                    plugin_class = plugin.Plugin(parent=self.mainbox,threads=self.threads)
                    plugin_class.__banner__ = banner
                    action_row          = Adw.ExpanderRow.new()
                    action_row.keywords = plugin.keywords
                    action_row.set_title_lines(2)
                    action_row.set_subtitle_lines(2)
                    action_row.add_prefix(plugin_class.__image__)
                    action_row.set_title(plugin.title)
                    action_row.set_subtitle(plugin.subtitle)
                    action_row.add_action(plugin_class.__button_box__)
                    listbox.append(action_row)
                    
                    row_box = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL,spacing=0)
                    row_box.props.margin_start  = 5
                    row_box.props.margin_end    = 5
                    row_box.props.margin_top    = 2
                    row_box.props.margin_bottom = 2
                    row_box.set_css_classes(["linked","flat"])
                    #row_box.set_homogeneous(True)
                    if plugin.website:
                        link_name    = plugin.website[0]
                        website      = plugin.website[1]
                        link_button  = Gtk.LinkButton.new_with_label(website,link_name)
                        link_button.set_css_classes(["wait-action-button"])
                        row_box.append(link_button)
                    if plugin.licenses:
                        for licenses_info in plugin.licenses:
                            license_type = licenses_info[0]
                            license_web  = licenses_info[1]
                            link_button  = Gtk.LinkButton.new_with_label(license_web,license_type)
                            link_button.set_css_classes(["running-destructive-action-button"])
                            row_box.append(link_button)
                    action_row.add_row(row_box)
                del plugin
            except Exception as e:
                print(e)
                print("Ignored >> Load {} Fail.".format(plugin))
                continue

    def on_search_entry_changed(self,searchentry,listbox):
        """The filter_func will be called for each row after the call, 
        and it will continue to be called each time a row changes (via [method`Gtk`.ListBoxRow.changed]) 
        or when [method`Gtk`.ListBox.invalidate_filter] is called. """
        listbox.invalidate_filter() # run filter (run self.on_filter_invalidate look at self.listbox.set_filter_func(self.on_filter_invalidate) )
        
    def on_filter_invalidate(self,row,searchentry):
        text_to_search = searchentry.get_text().strip()
        if  len(text_to_search)<3:
            return True
        if text_to_search.lower() in row.keywords: 
            return True # if True Show row
        return False 

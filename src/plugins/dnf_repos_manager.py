import dnf
from gi.repository import Adw
from gi.repository import Gtk,GLib
import subprocess
import threading

if_true_skip         = False
type_                = "page"
arch                 = ("all",)
distro_name          = ("fedora",)
distro_version       = ("all",)
category             = "Dnf"
category_icon_theme  = "network-transmit-symbolic"
desktop_env          = ("all",)
display_type         = ("all",)
keywords             = "dnf"
title                = "Dnf"
subtitle             = "Dnf Repos Manager"
icon                 = "aosus.png"
dnf_base = dnf.Base()
dnf_base.read_all_repos()

def on_long_pressed(gesture_long_press, offset_x, offset_y,revealer):
    revealer.props.reveal_child = not revealer.props.reveal_child
    return True

def __on_delete_button_clicked(button,listbox,listboxrow,revealer,repo):
    t = threading.Thread(target=on_delete_button_clicked,args=(button,listbox,listboxrow,revealer,repo))
    t.start()
    return True

def on_delete_button_clicked(button,listbox,listboxrow,revealer,repo):
    if  subprocess.call("pkexec rm {}".format(repo.repofile),shell=True) == 0:
        GLib.idle_add(listbox.remove,listboxrow)
        dnf_base.repos.clear()
        dnf_base.read_all_repos()
    else:
        GLib.idle_add(revealer.set_reveal_child,False)

def on_drag_update(gesture_drag, offset_x, offset_y,revealer):
    x_start = int(gesture_drag.get_start_point()[1])
    x_now = int(gesture_drag.get_offset()[1])
    if x_now > x_start:
        if x_now > 10:
            if not revealer.get_child_revealed():
                revealer.props.reveal_child = True
            #gesture_drag.reset()
            return True

    elif x_now < x_start:
        if x_now < -10:
            if revealer.get_child_revealed():
                revealer.props.reveal_child = False
            #gesture_drag.reset()
            return True
    return True

def __on_switch_changed(switch,property_,repo,action_row):
    t = threading.Thread(target=on_switch_changed,args=(switch,property_,repo,action_row))
    t.start()
    return True

def on_switch_changed(switch,property_,repo,row):
    action = "disable" if switch.status__ else "enable"
    if  subprocess.call("pkexec dnf config-manager --set-{} {}".format(action,repo.id),shell=True) != 0:
        GLib.idle_add(switch.set_active,switch.status__)
    else:
        if switch.status__ :
            row.keywords = row.keywords.replace("enable","disable")
        else:
            row.keywords = row.keywords.replace("disable","enable")
        switch.status__ = not switch.status__
    return True

def add_repo_row(listbox,repo,scrolledwindow,first_position=False):
    repo     = dnf_base.repos[repo]
    title    = repo.id
    subtitle = repo.cfg.getValue(repo.id,"name").replace("$releasever",dnf_base.conf.releasever).replace("$basearch",dnf_base.conf.basearch).replace("$arch",dnf_base.conf.arch)
    status   = True if repo.cfg.getValue(repo.id,"enabled") in ("1","True","true") else False
    action   = "enable" if status else "disable"
    hbox     = Gtk.Box()
    if first_position:
        listbox.insert(hbox,0)
    else:
        listbox.append(hbox)
    hbox.set_css_classes(["linked","flat"])
    revealer = Gtk.Revealer.new()
    revealer.set_transition_type( Gtk.RevealerTransitionType.SLIDE_LEFT )
    revealer.set_transition_duration(500 )
    hbox.append(revealer)
    delete_button = Gtk.Button.new()
    delete_button.set_css_classes(["destructive-action"])
    delete_button.props.hexpand = False
    delete_button.props.vexpand = True
    delete_button.props.label = "Delete"
    delete_button.connect("clicked",__on_delete_button_clicked,listbox,hbox.get_parent(),revealer,repo)
    revealer.set_child(delete_button)
    action_row  = Adw.ActionRow.new()
    longpress  = Gtk.GestureLongPress.new()
    longpress.connect("pressed",on_long_pressed,revealer)
    dragmotion = Gtk.GestureDrag.new()
    dragmotion.connect("drag_update",on_drag_update,revealer)
    action_row.add_controller(dragmotion)
    action_row.add_controller(longpress)
    action_row.props.hexpand = True
    action_row.props.vexpand = True
    hbox.append(action_row)
    row = hbox.get_parent()
    row.keywords = title+" "+ subtitle+" "+action
    if Adw.get_major_version() == 1 and Adw.get_minor_version() >2:
        action_row.set_title_lines(1)
        action_row.set_subtitle_lines(4)
    action_row.set_title(title)
    action_row.set_subtitle(subtitle)
    switch = Gtk.Switch.new()
    switch.set_active(status)
    switch.set_valign(Gtk.Align.CENTER)
    switch.status__ = status
    switch.connect("notify::active",__on_switch_changed,repo,row)
    action_row.add_suffix(switch)
    if first_position:
        scrolledwindow.get_vadjustment().set_value(0)

def __on_apply(entry_row,listbox,scrolledwindow):
    threading.Thread(target=on_apply,args=(entry_row,listbox,scrolledwindow)).start()

def on_apply(entry_row,listbox,scrolledwindow):
    if entry_row.has_css_class("error"):
        GLib.idle_add(entry_row.remove_css_class,"error")
    link = entry_row.get_text().strip()
    if not link:
        return
    if  subprocess.call("pkexec dnf config-manager --add-repo {}".format(link),shell=True) == 0:
        old_repos = list(dnf_base.repos.keys())
        dnf_base.repos.clear()
        dnf_base.read_all_repos()
        new_repos_name = [i for i in dnf_base.repos if i not in old_repos]
        if new_repos_name:
            for i in new_repos_name:
                GLib.idle_add(add_repo_row,listbox,i,scrolledwindow,True)
                GLib.idle_add(entry_row.delete_text,0,-1)
    else:
        GLib.idle_add(entry_row.add_css_class,"error")

def on_text_changed(entry_row,property_):
    if entry_row.has_css_class("error"):
        entry_row.remove_css_class("error")

def create_rows(listbox,box,scrolledwindow,searchlistbox):
    addlistbox = Gtk.ListBox.new()
    addlistbox.set_css_classes(["boxed-list"])
    clamp = Adw.Clamp.new()
    clamp.set_hexpand(True)
    clamp.props.margin_top    = 3
    clamp.props.margin_bottom = 10
    clamp.props.margin_start  = 5
    clamp.props.margin_end    = 5
    clamp.set_maximum_size(500)
    clamp.set_child(addlistbox)
    box.append(clamp)
    box.reorder_child_after(clamp,searchlistbox)
    add_repo_entry_row  = Adw.EntryRow.new()
    add_repo_entry_row.props.hexpand = True
    add_repo_entry_row.connect("apply",__on_apply,listbox,scrolledwindow)
    add_repo_entry_row.connect("notify::text",on_text_changed)
    add_repo_entry_row.set_input_purpose(Gtk.InputPurpose.URL)
    add_repo_entry_row.set_show_apply_button(True)
    addlistbox.append(add_repo_entry_row)

    for repo in dnf_base.repos:
        add_repo_row(listbox,repo,scrolledwindow)


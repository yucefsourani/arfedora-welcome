import os
import sys
import gettext
from site import addsitedir
import importlib
import tempfile
from string import punctuation
import time
import subprocess
from urllib import request
from .gui_widgets import create_toast
from gi.repository import GObject,GLib

arch           = os.uname().machine
distro_desktop = os.getenv("XDG_SESSION_DESKTOP",False).lower()
display_type   = os.getenv("XDG_SESSION_TYPE",False).lower()
is_wayland     = "wayland" in display_type
is_xorg        = not is_wayland

plugins_location = os.path.join(os.path.realpath(os.path.dirname(__file__)),"../plugins")
images_location  = os.path.join(os.path.realpath(os.path.dirname(__file__)),"../images")


css = b"""
.wait-action-button {
  background-color: @warning_bg_color;
  color: @accent_fg_color;
}

.running-destructive-action-button {
  background-color: @success_bg_color;
  color: @accent_fg_color;
}
"""

def get_image_location(image_name):
    location = os.path.join(images_location,image_name)
    if os.path.isfile(location):
        return location
    return False

def get_distro_name(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID") and not l.startswith("ID_"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")

def get_distro_name_like(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID_LIKE") :
                result=l.split("=",1)[1].strip()
    if not result:
        result = get_distro_name(location)
    return result.replace("\"","").replace("'","")

def get_distro_version(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("VERSION_ID"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")

def get_plugins():
    """Searches the plugins folders"""
    depl = []
    result = []
    addsitedir(plugins_location)
    ll = os.listdir(plugins_location)
    ll.sort()
    for  module_file in ll:
        if module_file.endswith(".py") and os.path.isfile(os.path.join(plugins_location,module_file)):
            if module_file not in depl:
                module_name, module_extension = os.path.splitext(module_file)
                result.append((plugins_location,module_name,module_file))
                depl.append(module_file)
    return result

def load_plugin(info):
    spec   = importlib.util.spec_from_file_location(info[1],os.path.join(info[0],info[2]))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_uniq_name(name):
    name = name.replace(" ","")
    return "".join([char for char in name if char not in punctuation])


def write_to_tmp(commands):
    time_now      = int(time.time()) * 4
    file_to_write = os.path.join(tempfile.gettempdir(),"{}.sh".format(time_now))
    with open(file_to_write,"w") as mf:
        for command in commands:
            mf.write(command+"\n")
    subprocess.call("chmod 755 "+file_to_write,shell=True)
    return file_to_write


class DownloadFile(GObject.Object):
    __gsignals__ = { "break"  : (GObject.SignalFlags.RUN_LAST, None, (str,)),
                     "fail"   : (GObject.SignalFlags.RUN_LAST, None, (str,)),
                     "done"   : (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }
    
    def __init__(self,plugin,link,location="",timeout=10,headers={"User-Agent":"Mozilla/5.0"}):
        GObject.Object.__init__(self)
        self.__link         = link
        self.__location     = location
        if not self.__location:
            self.__location = tempfile.gettempdir()
        self.__progressbar       = plugin.__progressbar__
        self.__label             = plugin.__label__
        self.__button            = plugin.__button__
        self.__runningmsg        = plugin._runningmsg
        self.__parent            = plugin.parent
        self.__timeout           = timeout
        self.__headers           = headers
        self.break_download      = False
        self.run_task_handler_id = plugin.run_task_handler_id
        
    def reset(self):
        GLib.idle_add(self.__label.set_label,self.__runningmsg)
        GLib.idle_add(self.__button.set_css_classes,["wait-action-button"])


    def reset_handler(self):
        self.__button.set_sensitive(False)
        self.__button.disconnect(self.bread_handler_id)
        self.__button.handler_unblock(self.run_task_handler_id)
        
    def on_break(self,button):
        self.break_download = True

    def block_(self):
        self.__button.handler_block(self.run_task_handler_id)
        self.connect_to_break()
        self.__button.set_sensitive(True)

    def connect_to_break(self):
        self.bread_handler_id = self.__button.connect("clicked",self.on_break)
        
    def start(self):
        GLib.idle_add(self.block_)
        
        GLib.idle_add(self.__label.set_label,"Downloading")
        GLib.idle_add(self.__button.set_css_classes,["running-destructive-action-button"])
        return self.check_link()
        
    def check_link(self):
        try:
            self.__opurl   = request.urlopen(self.__link)
            try:
                self.__saveas = self.__opurl.headers["Content-Disposition"].split("=",1)[-1]
            except Exception as e:
                self.__saveas = os.path.basename(self.__opurl.url)
        except Exception as e:
            print(e)
            GLib.idle_add(create_toast,"Download {} Failed.".format(self.__link),1)
            GLib.idle_add(self.reset_handler)
            self.reset()
            return False
        self.__saveas = os.path.join(self.__location,self.__saveas)
        return self.start_download()

    def start_download(self):
        GLib.idle_add(self.__progressbar.show)
        try:
            ch_  = 64*1024 
            size = int(self.__opurl.headers["Content-Length"])
            if os.path.isfile(self.__saveas):
                psize = os.path.getsize(self.__saveas)
                if psize == size:
                    GLib.idle_add(self.__progressbar.set_fraction,1.0)
                    GLib.idle_add(self.__progressbar.set_text,"Done")
                    GLib.idle_add(self.emit,"done",self.__saveas)
                    GLib.idle_add(self.__progressbar.hide)
                    GLib.idle_add(self.reset_handler)
                    self.reset()
                    return self.__saveas
                mode  = "ab"
            else:
                psize = 0
                mode  = "wb"

            if "Range" in self.__headers.keys():
                self.__headers["Range"] = "bytes={}-{}".format(psize,size)
            else:
                self.__headers.setdefault("Range", "bytes={}-{}".format(psize,size))
            url   = request.Request(self.__link,headers=self.__headers)
            opurl = request.urlopen(url,timeout=self.__timeout)
            with open(self.__saveas, mode) as op:
                while True:
                    if self.break_download:
                        try:
                            opurl.close()
                            op.close()
                        except Exception as e:
                            pass
                        GLib.idle_add(self.emit,"break",self.__saveas)
                        GLib.idle_add(self.__progressbar.hide)
                        GLib.idle_add(self.reset_handler)
                        self.reset()
                        return
                    chunk = opurl.read(ch_)
                    if not chunk:
                        break
                    count = int((psize*100)//size)
                    fraction = count/100
                    op.write(chunk)
                    op.flush()
                    psize += ch_
                    GLib.idle_add(self.__progressbar.set_fraction,fraction)
                    GLib.idle_add(self.__progressbar.set_text,str(count)+"%")
            
            GLib.idle_add(self.__progressbar.set_fraction,1.0)
            GLib.idle_add(self.__progressbar.set_text,"Done")
            GLib.idle_add(self.emit,"done",self.__saveas)
        except Exception as e:
            print(e)
            GLib.idle_add(self.__progressbar.set_fraction,0.0)
            GLib.idle_add(self.__progressbar.set_text,"Fail")
            GLib.idle_add(create_toast,"Download File To {} Failed.".format(self.__saveas),1)
            GLib.idle_add(self.emit,"fail",self.__saveas)
            GLib.idle_add(self.reset_handler)
            self.reset()
            return False
        finally:
            try:
                opurl.close()
                op.close()
            except Exception as e:
                pass
        GLib.idle_add(self.__progressbar.hide)
        GLib.idle_add(self.reset_handler)
        self.reset()
        return self.__saveas
        
def check_rpm_package_exists(package_name):
    if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
        return True
    return False
  

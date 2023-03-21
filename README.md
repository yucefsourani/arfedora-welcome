# For Fedora Linux Only (Tested on Fedora 38 beta)

# arfedora-welcome BETAAAA (For Testing Only)

مازال لم ينتهي بعد وهو للتجربة فقط وهو موجه لفيدورا لينكس فقط 

# Runtime Requires
 
``` sudo dnf install vte291-gtk4 gettext gtk4 flatpak libadwaita ```



# Install (Build Require Meson glib2-devel gtk4 gettext)

``` sudo dnf install meson glib2-devel gtk4 gettext ```

``` git clone https://github.com/yucefsourani/arfedora-welcome ```

``` cd arfedora-welcome ```

``` meson setup builddir  --prefix /usr &&sudo meson install -C builddir && arfedora-welcome -d ```


![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedora-welcome/main/screenshots/Screenshot11.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedora-welcome/main/screenshots/Screenshot12.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedora-welcome/main/screenshots/Screenshot13.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedora-welcome/main/screenshots/Screenshot14.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedora-welcome/main/screenshots/Screenshot15.png "Screenshot")

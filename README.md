# For Fedora Linux Only (Tested on Fedora 38 beta)

# arfedora-welcome BETAAAA (For Testing Only)

مازال لم ينتهي بعد وهو للتجربة فقط وهو موجه لفيدورا لينكس فقط 

# Runtime Requires
 
``` sudo dnf install vte291-gtk4 gettext gtk4 flatpak ```



# Install (Build Require Meson glib2-devel gtk4 gettext)

``` sudo dnf install meson glib2-devel gtk4 gettext ```

``` git clone https://github.com/yucefsourani/arfedora-welcome ```

``` cd arfedora-welcome ```

``` meson setup builddir  --prefix /usr &&sudo meson install -C builddir && arfedora-welcome -d ```



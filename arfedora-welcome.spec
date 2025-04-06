Name:           arfedora-welcome
Version:        1.0
Release:        14%{?dist}
Summary:        makes it easy to install software in Fedora
Obsoletes:      luniversalinstaller
Provides:       luniversalinstaller
Conflicts:      luniversalinstaller
License:        GPLv3     
URL:            https://github.com/yucefsourani/arfedora-welcome
Source0:        https://github.com/yucefsourani/arfedora-welcome/archive/main.zip
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  meson
BuildRequires:  glib2-devel
BuildRequires:  gettext
Requires:       python3-gobject
Requires:       gtk4
Requires:       python3-beautifulsoup4
Requires:       flatpak
Requires:       gnome-icon-theme
Requires:       vte291-gtk4 
Requires:       gettext
Requires:       libadwaita
Requires:       mokutil
Requires:       python3-dnf

%description
Makes it easy to install software in Fedora.


%prep
%autosetup -n arfedora-welcome-main

%build
%meson

%install
rm -rf $RPM_BUILD_ROOT
%meson_install


%files
%license LICENSE
%doc README.md
%{_bindir}/arfedora-welcome
%{_datadir}/applications/*
%{_datadir}/arfedora-welcome/plugins/*
%{_datadir}/arfedora-welcome/images/*
%{_datadir}/arfedora-welcome/arfedora_welcome/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/appdata/com.github.yucefsourani.Arfedorawelcome.appdata.xml
%{_datadir}/glib-2.0/schemas/com.github.yucefsourani.Arfedorawelcome.gschema.xml



%changelog
* Sun Apr 6 2025 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-14
- Release 14
- Remove Microsoft Edge
- Remove Skype
- Remove Visual Studio Code
- Remove Viber


* Thu Mar 20 2025 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-13
- Release 13
- Support F42

* Mon Sep 23 2024 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-12
- Release 12
- Support F41

* Sat Apr 20 2024 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-11
- Release 11
- Support F40

* Mon Nov 20 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-10
- Release 10
- Add Dnf Plugin
- Fix running in gnome xorg

* Tue Nov 14 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-9
- Release 9
- Add Gimp Beta
- Add xdman Beta

* Sun Nov 12 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-8
- Release 8

* Wed Nov 1 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-7
- Release 7

* Sun Sep 17 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-6
- Release 6
- Codecs Plugin Support F39

* Sat May 13 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-5
- Release 5
- Add links section
- Add mpv plugin

* Tue Apr 11 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-4
- Release 4

* Sun Apr 9 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-3
- Release 3

* Sun Apr 9 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-2
- Release 2

* Wed Mar 29 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-1
- Initial For Fedora 38



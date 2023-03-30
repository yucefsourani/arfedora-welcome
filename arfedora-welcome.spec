Name:           arfedora-welcome
Version:        1.0
Release:        1%{?dist}
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
* Wed Mar 29 2023 yucuf sourani <youssef.m.sourani@gmail.com> 1.0-1
- Initial For Fedora 38



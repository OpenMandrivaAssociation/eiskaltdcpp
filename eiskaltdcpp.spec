%define	major		2.2
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d


Name:		eiskaltdcpp
Version:	2.2.9
Release:	3
License:	GPLv3+
Summary:	Cross-platform program that uses the Direct Connect and ADC protocol
Url:		http://code.google.com/p/eiskaltdc
Group:		Networking/File transfer
Source0:	https://eiskaltdc.googlecode.com/files/%{name}-%{version}.tar.xz
Patch0:		eiskaltdcpp-2.2.8-fix-linkage.patch

BuildRequires:  cmake >= 2.6.3
BuildRequires:  boost-devel
BuildRequires:  aspell-devel
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  qt4-devel
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(openssl) >= 0.9.8
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(gail-3.0)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(gladeui-2.0)
BuildRequires:  pkgconfig(libidn)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  miniupnpc-devel
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(libcanberra-gtk3)


%description
EiskaltDC++ is a cross-platform program that uses the Direct Connect and ADC
protocol. It is compatible with other DC clients, such as the original DC from
Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates with all
common DC hub software. The minimum number of our patches to original DC++
kernel makes it easy to upgrade to new versions and ensures compatibility with
other clients.


%files -f lib%{name}.lang
%doc AUTHORS COPYING LICENSE ChangeLog.txt ChangeLog_ru.txt ChangeLog_uk.txt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/update_geoip
%{_datadir}/%{name}/sounds
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/emoticons
%{_datadir}/%{name}/luascripts
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic library used by EiskaltDC++
Group:		System/Libraries

%description -n %{libname}
Dynamic library used by EiskaltDC++.

%files -n %{libname}
%doc COPYING
%{_libdir}/lib%{name}.so.%{major}*

#-----------------------------------------------------------------------------


%package qt
Summary:	Qt frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description qt
EiskaltDC++ is a cross-platform program that uses the Direct Connect and ADC
protocol. It is compatible with other DC clients, such as the original DC from
Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates with all
common DC hub software. The minimum number of our patches to original DC++
kernel makes it easy to upgrade to new versions and ensures compatibility with
other clients. This is the Qt front end.



%files qt -f %{name}-qt.lang
%doc COPYING
%dir %{_datadir}/%{name}/qt
%dir %{_datadir}/%{name}/qt/ts
%{_datadir}/%{name}/qt/icons
%{_datadir}/%{name}/qt/qtscripts
%{_datadir}/%{name}/qt/resources
%{_mandir}/man1/%{name}-qt.1.*
%{_datadir}/applications/%{name}-qt.desktop
%{_bindir}/%{name}-qt


#-----------------------------------------------------------------------------
%package gtk
Summary:	GTK frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description gtk
EiskaltDC++ is a cross-platform program that uses the Direct Connect and ADC
protocol. It is compatible with other DC clients, such as the original DC from
Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates with all
common DC hub software. The minimum number of our patches to original DC++
kernel makes it easy to upgrade to new versions and ensures compatibility with
other clients. This is the GTK front end.



%files gtk -f %{name}-gtk.lang
%doc COPYING
%{_datadir}/%{name}/gtk
%{_mandir}/man1/%{name}-gtk.1.*
%{_datadir}/applications/%{name}-gtk.desktop
%{_bindir}/%{name}-gtk


#-----------------------------------------------------------------------------
%package daemon
Summary:	A simple EiskaltDC++ daemon
Group:		Networking/File transfer
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	perl(Term::UI)

%description daemon
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. This is a simple daemon for running
EiskaltDC++ without any GUI; it can be controlled via XMLRPC or JSONRPC.

%files daemon
%doc AUTHORS COPYING LICENSE README TODO
%{_datadir}/%{name}/cli/*
%{_mandir}/man1/%{name}-daemon.1.*
%{_mandir}/man1/%{name}-cli-*.1.*
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-cli-*


#-----------------------------------------------------------------------------
%package -n %{develname}
Summary:	Development files for the main EiskaltDC++ library
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software.
This package contains the header files needed to use the main EiskaltDC++
library.

%files -n %{develname}
%doc COPYING ChangeLog.txt ChangeLog_ru.txt ChangeLog_uk.txt
%{_includedir}/%{name}/dcpp/*.h


#-----------------------------------------------------------------------------

%prep
%setup -q
#https://github.com/eiskaltdcpp/eiskaltdcpp/issues/27
lua_version=`lua -v 2>&1 | cut -d ' ' -f2 | cut -d '.' -f1,2`
if [ "$lua_version" = "5.2" ]
then
    sed -i -e 's/Lua51/Lua52/' CMakeLists.txt cmake/FindLua52.cmake
fi

%patch0 -p1 -b .linkage

%build
rm -rf data/examples/*.php eiskaltdcpp-qt/qtscripts/gnome/*.php

%cmake	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DLOCAL_BOOST=OFF \
	-DLUA_SCRIPT=ON \
	-DUSE_IDNA=ON \
	-DPERL_REGEX=ON \
	-DUSE_QT=ON \
	-DUSE_QT_SQLITE=ON \
	-DUSE_QT_QML=ON \
	-DUSE_JS=ON \
	-DUSE_ASPELL=ON \
	-DFREE_SPACE_BAR_C=ON \
	-DDBUS_NOTIFY=ON \
	-DUSE_GTK3=ON \
	-DUSE_LIBGNOME2=OFF \
	-DUSE_LIBNOTIFY=ON \
	-DUSE_LIBCANBERRA=ON \
	-DNO_UI_DAEMON=ON \
	-DXMLRPC_DAEMON=OFF \
	-DJSONRPC_DAEMON=ON \
	-DUSE_CLI_XMLRPC=ON \
	-DUSE_CLI_JSONRPC=ON \
	-DWITH_DEV_FILES=ON \
	-DEISKALTDCPP_INCLUDE_DIR="%{_includedir}/%{name}" \
	-DWITH_EMOTICONS=ON \
	-DWITH_SOUNDS=ON \
	-DWITH_EXAMPLES=ON \
	-DWITH_LUASCRIPTS=ON \
	-DWITH_DHT=ON \
	-DUSE_MINIUPNP=ON \
	-DCREATE_MO=ON \
	-DINSTALL_RUNTIME_PATH=OFF
%make


%install
%makeinstall_std -C build

%find_lang %{name}-gtk

find %{buildroot} -name "*.qm" | sed 's:'%{buildroot}':: 
s:.*/\([a-zA-Z]\{2\}\).qm:%lang(\1) \0:' > %{name}-qt.lang

%find_lang lib%{name} lib%{name}.lang





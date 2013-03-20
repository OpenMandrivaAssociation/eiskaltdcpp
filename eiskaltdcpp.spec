#define		_enable_debug_packages	%{nil}
#define		debug_package		%{nil}

%define	major	2.2
%define	libname	%mklibname %{name} %{major}
%define	develname %mklibname %{name} -d

# Now QT build requires gcc >= 4.5.0
# so disable it on 2010.2
%if %{mdvver} >= 201100
%define	with_qt		1
%else
%define	with_qt		0
%endif

%if %{mdvver} >= 201100
%define	with_gtk		1
%else
%define	with_gtk		0
%endif

%define	with_daemon	0
%define	with_devel	1

Name:		eiskaltdcpp
Version:		2.2.7
Release:		3
License:		GPLv3+
Summary:		Cross-platform program that uses the Direct Connect and ADC protocol
Url:		http://code.google.com/p/eiskaltdc
Group:		Networking/File transfer
Source0:		%{name}-%{version}.tar.bz2
Patch0:		eiskaltdcpp-2.2.7-includes.patch
Patch1:		eiskaltdcpp-2.2.7-linkage.patch

# Core requirements
BuildRequires:	boost-devel >= 1.42.0
BuildRequires:	cmake >= 2.6.3
BuildRequires:	pcre-devel
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	zlib-devel
BuildRequires:	gettext
BuildRequires:	attr-devel
BuildRequires:	idn-devel
BuildRequires:	pkgconfig(lua)
# When enabling miniupnpc in the cmake command line this is needed
BuildRequires:	miniupnpc-devel

%if %{with_daemon}
# Requirements for eiskaltdcpp deamon
BuildRequires:	xmlrpc-c-devel >= 1.19
%endif
# Qt requirements
%if %{with_qt}
BuildRequires:	aspell-devel
# Now QT build requires gcc >= 4.5.0
BuildRequires:	gcc >= 4.5.0
# For QT_QML qt4 >= 4.7.0 is needed
BuildRequires:	qt4-devel >= 4.7.0
%endif
# Gtk requirements
%if %{with_gtk}
BuildRequires:	pkgconfig(libgnome-2.0)
BuildRequires:	pango-devel
BuildRequires:	glib2-devel >= 2.24
BuildRequires:	gtk2-devel >= 2.24
BuildRequires:	libcanberra-devel
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libnotify)
%endif

%description
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. The minimum number of our patches to
original DC++ kernel makes it easy to upgrade to new versions and ensures
compatibility with other clients.

%package -n %{libname}
Summary:		Dynamic library used by EiskaltDC++
Group:		System/Libraries

%description -n %{libname}
Dynamic library used by EiskaltDC++.

%if %{with_qt}
%package qt
Summary:		Qt frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}

%description qt
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. The minimum number of our patches to
original DC++ kernel makes it easy to upgrade to new versions and ensures
compatibility with other clients. This is the Qt front end.
%endif

%if %{with_gtk}
%package gtk
Summary:		GTK frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}

%description gtk
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. The minimum number of our patches to
original DC++ kernel makes it easy to upgrade to new versions and ensures
compatibility with other clients. This is the GTK front end.
%endif

%if %{with_daemon}
%package daemon
Summary:		A simple EiskaltDC++ daemon
Group:		Networking/File transfer
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	perl-Term-UI

%description daemon
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. This is a simple daemon for running
EiskaltDC++ without any GUI; it can be controlled via XMLRPC or JSONRPC.
%endif

%if %{with_devel}
%package -n %{develname}
Summary:		Development files for the main EiskaltDC++ library
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}

%description -n %{develname}
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software.
This package contains the header files needed to use the main EiskaltDC++
library.
%endif

%prep
%setup -q
%patch0 -p1 -b .includes
%patch1 -p1 -b .linkage

%build
%cmake	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DLOCAL_BOOST=OFF \
	-DLUA_SCRIPT=ON \
	-DUSE_IDNA=ON \
	-DPERL_REGEX=ON \
%if %{with_qt}
	-DUSE_QT=ON \
	-DUSE_QT_SQLITE=ON \
	-DUSE_JS=ON \
	-DUSE_ASPELL=ON \
	-DFREE_SPACE_BAR_C=ON \
	-DDBUS_NOTIFY=ON \
	-DUSE_QT_QML=ON \
%else
	-DUSE_QT=OFF \
%endif
%if %{with_gtk}
	-DUSE_GTK=ON \
	-DUSE_GTK3=OFF \
	-DUSE_LIBGNOME2=ON \
	-DUSE_LIBNOTIFY=ON \
%endif
%if %{with_daemon}
	-DNO_UI_DAEMON=ON \
	-DXMLRPC_DAEMON=OFF \
	-DJSONRPC_DAEMON=ON \
	-DUSE_CLI_XMLRPC=ON \
	-DUSE_CLI_JSONRPC=ON \
%else
	-DNO_UI_DAEMON=OFF \
	-DXMLRPC_DAEMON=OFF \
	-DJSONRPC_DAEMON=OFF \
	-DUSE_CLI_XMLRPC=OFF \
	-DUSE_CLI_JSONRPC=OFF \
%endif
%if %{with_devel}
	-DWITH_DEV_FILES=ON \
	-DEISKALTDCPP_INCLUDE_DIR="%{_includedir}/%{name}" \
%else
	-DWITH_DEV_FILES=OFF \
%endif
	-DWITH_EMOTICONS=ON \
	-DWITH_SOUNDS=ON \
	-DWITH_EXAMPLES=ON \
	-DWITH_LUASCRIPTS=ON \
	-DWITH_DHT=ON \
	-DUSE_MINIUPNP=ON \
	-DLOCAL_MINIUPNP=OFF \
	-DCREATE_MO=ON

%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

# We don't want install php only for 3 example scripts (in russian moreover),
# nor we want remove all the example scripts,
# so removing the offenders and make find-provides happy
rm -f %{buildroot}/%{_datadir}/%{name}/examples/*.php
rm -rf %{buildroot}/%{_datadir}/%{name}/qt/qtscripts/gnome

%if %{with_gtk}
%find_lang %{name}-gtk
%endif

%if %{with_qt}
find %{buildroot} -name "*.qm" | sed 's:'%{buildroot}':: 
s:.*/\([a-zA-Z]\{2\}\).qm:%lang(\1) \0:' > %{name}-qt.lang
%endif

# The language files are named "libeiskaltdcpp.mo"
# and the filelist name is "libeiskaltdcpp.lang"
%find_lang lib%{name} lib%{name}.lang


%files -f lib%{name}.lang
%doc AUTHORS COPYING COPYING.DCPP COPYING.OpenSSL LICENSE ChangeLog.txt ChangeLog_ru.txt ChangeLog_uk.txt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/update_geoip
%{_datadir}/%{name}/sounds
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/emoticons
%{_datadir}/%{name}/luascripts
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%if %{with_qt}
%files qt -f %{name}-qt.lang
%dir %{_datadir}/%{name}/qt
%dir %{_datadir}/%{name}/qt/ts
%{_datadir}/%{name}/qt/icons
%{_datadir}/%{name}/qt/qtscripts
%{_datadir}/%{name}/qt/resources
%{_mandir}/man1/%{name}-qt.1.*
%{_datadir}/applications/%{name}-qt.desktop
%{_bindir}/%{name}-qt
%endif

%if %{with_gtk}
%files gtk -f %{name}-gtk.lang
%{_datadir}/%{name}/gtk
%{_mandir}/man1/%{name}-gtk.1.*
%{_datadir}/applications/%{name}-gtk.desktop
%{_bindir}/%{name}-gtk
%endif

%if %{with_daemon}
%files daemon
%{_datadir}/%{name}/cli/*
%{_mandir}/man1/%{name}-daemon.1.*
%{_mandir}/man1/%{name}-cli-*.1.*
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-cli-*
%endif

%if %{with_devel}
%files -n %{develname}
%doc ChangeLog.txt ChangeLog_ru.txt ChangeLog_uk.txt
%{_includedir}/%{name}/dcpp/*.h
%endif


%changelog
* Fri Oct 12 2012 Giovanni Mariani <mc2374@mclink.it> 2.2.7-2
- Keep enabled debug packages
- Dropped BuildRoot, %%mkrel and %%clean section
- Added BReqs for attr and gcc, accordingly to the CMakeLists.txt file
- Release 2.2.7 comes with daemon program: added provision to optionally
  build and package it (disabled ATM)
- Made an optional package to accomodate development files for the main library
- Added P1 to fix linking error with boost library

* Fri Jun 01 2012 Andrey Bondrov <abondrov@mandriva.org> 2.2.7-1
+ Revision: 801731
- Move library to separate package to make rpmlint happy
- Add eiskaltdcpp-2.2.7-includes patch to fix build, do some minor fixes

  + Sergey Zhemoitel <serg@mandriva.org>
    - update to 2.2.7

* Tue Feb 21 2012 Sergey Zhemoitel <serg@mandriva.org> 2.2.6-3
+ Revision: 778673
- add new relase 2.2.6

* Thu Jan 12 2012 Sergey Zhemoitel <serg@mandriva.org> 2.2.5-3
+ Revision: 760555
+ rebuild (emptylog)

* Thu Jan 12 2012 Sergey Zhemoitel <serg@mandriva.org> 2.2.5-2
+ Revision: 760536
- add new spec whith several changes
- new release 2.2.5

* Sun Nov 06 2011 Sergey Zhemoitel <serg@mandriva.org> 2.2.4-2
+ Revision: 722835
+ rebuild (emptylog)

* Mon Oct 03 2011 Sergey Zhemoitel <serg@mandriva.org> 2.2.4-1
+ Revision: 702481
- new version 2.2.4
- import source from new release 2.2.3
- new release 2.2.3

* Fri May 20 2011 Александр Казанцев <kazancas@mandriva.org> 2.2.2-1
+ Revision: 676356
- new version 2.2.2

* Mon Apr 25 2011 Sergey Zhemoitel <serg@mandriva.org> 2.2.1-1
+ Revision: 658705
- imported package eiskaltdcpp

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - repackage from mandriva (from serg | 2011-04-12 15:16:34 +0200)


* Thu Aug 12 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 2.1.0-alt0.1.svn1521
- svn r1521
- split to subpackages(qt,gtk,common,libdcpp)

* Wed Jun 09 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 2.0.3-alt1
- 2.0.3 release 

* Thu May 06 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 2.0.2-alt1
- 2.0.2 release

* Mon Apr 19 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 2.0.1-alt1
- 2.0.1 release

* Mon Mar 22 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 2.0-alt1
- 2.0 release

* Fri Mar 19 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 1.99-alt0.2
- Updated to revision 366
  +  Fixed crushing on Oxygen theme
  +  Fixed desktop file (repocop)
  +  Added aspell support

* Sat Mar 06 2010 Aeliya Grevnyov <gray_graff@altlinux.org> 1.99-alt0.1
- 1.99 (beta!)
- Initial build for sisyphus

#define	use_ccache	1
#define	ccachedir	~/.ccache-OOo%{mdvsuffix}
#			%{?_with_ccache: %global use_ccache 1}%{?_without_ccache: %global use_ccache 0}
%define			_enable_debug_packages	%{nil}
%define			debug_package		%{nil}

# Now QT build requires gcc >= 4.5.0
# so disable it on 2010.2
%if %mdkversion <= 201010
%define	with_qt		0
%else
%define with_qt		1
%endif

%define	with_gtk	1


Name:		eiskaltdcpp
Version:	2.2.5
Release:	%mkrel 2
License:	GPLv3+
Summary:	Cross-platform program that uses the Direct Connect and ADC protocol
Url:		http://code.google.com/p/eiskaltdc
Group:		Networking/File transfer
Source0:	%{name}-%{version}.tar.bz2
Patch0:		eiskaltdcpp-cmake-unset.patch
Patch1:		eiskaltdcpp-qt4.4.patch

# Core requirements
BuildRequires:	boost-devel >= 1.38.0
BuildRequires:	cmake >= 2.6.3
BuildRequires:	pcre-devel
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRequires:	gettext
BuildRequires:	idn-devel
BuildRequires:	liblua5.1-devel
# When enabling miniupnpc in the cmake command line this is needed
#BuildRequires:	miniupnpc-devel

# Qt requirements
%if %{with_qt}
BuildRequires:	aspell-devel
BuildRequires:	gcc >= 4.5.0
# For QT_QML qt4 >= 4.7.0 is needed
BuildRequires:	qt4-devel >= 4.7.0
%endif
# Gtk requirements
%if %{with_gtk}
BuildRequires:	libgnome2-devel
BuildRequires:	pango-devel
BuildRequires:	glib2-devel >= 2.24
#BuildRequires:	pkgconfig(libgtk)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	libnotify-devel >= 0.4.1
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}


%description
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. The minimum number of our patches to
original DC++ kernel makes it easy to upgrade to new versions and ensures
compatibility with other clients.


%if %{with_qt}
%package qt
Summary:	Qt frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{version}

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
Summary:	GTK frontend for EiskaltDC++
Group:		Networking/File transfer
Requires:	%{name} = %{version}

%description gtk
EiskaltDC++ is a cross-platform program that uses the Direct Connect and
ADC protocol. It is compatible with other DC clients, such as the original
DC from Neomodus, DC++ and derivatives. EiskaltDC++ also inter operates
with all common DC hub software. The minimum number of our patches to
original DC++ kernel makes it easy to upgrade to new versions and ensures
compatibility with other clients. This is the GTK front end.
%endif


%prep
%setup -q
%patch0 -p1 -b .cmake_unset
#patch1 -p1 -b .qt44


%build
%cmake	.. -DCMAKE_BUILD_TYPE=Release \
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
	-DUSE_LIBGNOME2=ON \
	-DUSE_LIBNOTIFY=ON \
%endif
	-DWITH_EMOTICONS=ON \
	-DWITH_SOUNDS=ON \
	-DWITH_EXAMPLES=ON \
	-DWITH_LUASCRIPTS=ON \
	-DWITH_DHT=ON \
	-DWITH_DEV_FILES=OFF \
	-DUSE_MINIUPNP=OFF \
	-DLOCAL_MINIUPNP=OFF \
	-DCREATE_MO=ON \
	-DLINGUAS="*"
# TODO: When enabling some of the below, adjust the BReqs accordingly
#-DUSE_MINIUPNP: library not available in Mandriva yet; to enable it: ON to USE_MINIUPNP, OFF to LOCAL_MINIUPNP

%make


%install
rm -rf %{buildroot}
#pushd build
%makeinstall_std -C build
#popd

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


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f lib%{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.DCPP COPYING.OpenSSL LICENSE ChangeLog.txt ChangeLog_ru.txt ChangeLog_uk.txt
%dir %{_datadir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_datadir}/%{name}/update_geoip
%{_datadir}/%{name}/sounds
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/emoticons
%{_datadir}/%{name}/luascripts/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%if %{with_qt}
%files qt -f %{name}-qt.lang
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_datadir}/%{name}/gtk
%{_mandir}/man1/%{name}-gtk.1.*
%{_datadir}/applications/%{name}-gtk.desktop
%{_bindir}/%{name}-gtk
%endif



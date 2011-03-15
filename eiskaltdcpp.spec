Name: eiskaltdcpp
Version: 2.2.1
Release: %mkrel 1
Summary: EiskaltDC++ - Direct Connect client
License: GPLv3
Group: Networking/File transfer
Url: http://code.google.com/p/eiskaltdc/
#Packager: Aeliya Grevnyov <gray_graff@altlinux.org>

Source: %name-%version.tar.bz2

#BuildRequires(pre): rpm-macros-cmake
BuildRequires: cmake gcc-c++ libqt4-devel libupnp-devel libbzip2-devel libboost-devel libaspell-devel
BuildRequires: libgtk+2-devel libglade2.0_0-devel glib2-devel libpango-devel libnotify-devel phonon-devel libopenssl-devel  
BuildRequires: pcre liblua-devel

#%add_findreq_skiplist *xmms2_audacious2.ru_RU.UTF-8.php
#%add_findreq_skiplist *commands.ru_RU.UTF-8.php

%description
EiskaltDC++ is a program for UNIX-like systems that uses the Direct Connect and ADC protocol. 
It is compatible with other DC clients, such as the original DC from Neomodus, DC++ and derivatives. 
EiskaltDC++ also interoperates with all common DC hub software. 


%package common
Group: Networking/File transfer
Summary: Common files for %name
Requires: libdcpp = %version-%release
%description common
Common files for %name

%package gtk
Group: Networking/File transfer
Summary: GTK-based graphical interface
Requires: %name-common = %version-%release
%description gtk
Gtk interface based on code of FreeDC++ and LinuxDC++

%package qt
Group: Networking/File transfer
Summary: Qt-based graphical interface
Provides: %name = %version-%release
#Obsoletes: %name <= 2.0.3-alt1
Requires: %name-common = %version-%release
%description qt
Qt-based graphical interface

%package -n libdcpp
Group: System/Libraries
Summary: dcpp libraries
%description -n libdcpp
dcpp libraries


%prep
%setup

%build
%cmake \
%if %_lib == lib64
 -DLIBDIR=lib64 \
%endif
 -DUSE_ASPELL=ON \
 -DUSE_QT=ON \
 -DFREE_SPACE_BAR_C=ON \
 -DUSE_LIBUPNP=ON \
 -DUSE_GTK=ON \
 -DDBUS_NOTIFY=ON \
 -DUSE_JS=ON \
 -DLOCAL_BOOST=ON \
 -DPERL_REGEX=ON \
 -DLUA_SCRIPT=OFF
 
make %{?_smp_mflags}
#%make_build -C BUILD

%install
%makeinstall -C BUILD DESTDIR="%buildroot/"

%files qt
%_bindir/*qt
%_desktopdir/*qt.desktop

%files gtk
%_bindir/*gtk
%_desktopdir/*gtk.desktop

%files -n libdcpp
%_libdir/*

%files common
%_datadir/%name/*                                                                                                                                                                                        
%_miconsdir/%name.png                                                                                                                                                                                    
%_niconsdir/%name.png                                                                                                                                                                                    
%_liconsdir/%name.png                                                                                                                                                                                    
%_iconsdir/hicolor/128x128/apps/%name.png                                                                                                                                                                
%_iconsdir/hicolor/64x64/apps/%name.png                                                                                                                                                                  
%_iconsdir/hicolor/24x24/apps/%name.png                                                                                                                                                                  
%_iconsdir/hicolor/22x22/apps/%name.png                                                                                                                                                                  
%_pixmapsdir/*                                                                                                                                                                                           
%_man1dir/*


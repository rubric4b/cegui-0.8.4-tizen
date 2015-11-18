%define _prefix		/usr
%define _libdir		%{_prefix}/lib

Name:           cegui
Version:        0.8.4
Release:        1
License:        MIT
Summary:        CeGUI project
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	packaging/cegui.manifest

BuildRequires: cmake
#BuildRequires: pkgconfig(dlog)
#%if 0%{?_include_tc}
#BuildRequires: pkgconfig(turbojpeg)
#%endif
BuildRequires: model-build-features

%description

%package -n cegui-devel
Summary:	Development components for the CeGUI library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n cegui-devel
cegui development libraries and head files

#%if 0%{?_include_tc}
#%package -n native-buffer-tc
#Summary:	Test case for the Native Buffer library
#Group:		Development/Libraries
#Requires:	%{name} = %{version}-%{release}
#BuildRequires: pkgconfig(opengl-es-20)

#%description -n native-buffer-tc
#native buffer test cases
#%endif

%prep
%setup -q

%build
%if 0%{?tizen_build_binary_release_type_eng}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif

CFLAGS+=" -fvisibility=hidden -fdata-sections -ffunction-sections -Wl,--gc-sections"
cp %{SOURCE1001} .

%if 0%{?_include_tc}
%global extra_option -DBUILD_TC=TRUE
%endif

%if "%{?model_build_feature_graphics_gpu_info}" == "mali400"
%global extra_option -DUSE_MALI=TRUE
%endif

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIB_DIR=%{_libdir} -DPACKAGE_VERSION=%{version} %{?extra_option}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest cegui.manifest
%{_libdir}/libCEGUI*.so*
%{_libdir}/cegui-0.8/libCEGUI*.so*
/usr/share/cegui-0/*

%files -n cegui-devel
%{_includedir}/cegui-0/*
%{_libdir}/pkgconfig/CEGUI-0.pc


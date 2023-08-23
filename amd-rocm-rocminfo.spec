%global commit0 f2220a00fe635b27f493da1fa30843bf7bbd440d
%global _lto_cflags %{nil}
%global build_cxxflags %{nil}
%global build_ldflags %{nil}
%global _name amd-rocm-rocminfo
%global rocm_path /opt/rocm
%global hipcc %{rocm_path}/bin/hipcc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global toolchain clang
%global up_name rocminfo

%define patch_level 3

%bcond_with debug
%bcond_with static

%if %{without debug}
  %if %{without static}
    %global suf %{nil}
  %else
    %global suf -static
  %endif
%else
  %if %{without static}
    %global suf -debug
  %else
    %global suf -static-debug
  %endif
%endif

Name: %{_name}%{suf}

Version:        5.6
Release:        %{patch_level}.git%{?shortcommit0}%{?dist}
Summary:        TBD
License:        TBD

URL:            https://github.com/trixirt/%{up_name}
Source0:        %{url}/archive/%{commit0}/%{up_name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  numactl-devel

%if %{without debug}
%global debug_package %{nil}
%endif

%description
TBD

%package devel
Summary:        TBD

%description devel
%{summary}

%prep
%autosetup -p1 -n %{up_name}-%{commit0}

%build
%cmake \
%if %{with static}
       -DBUILD_SHARED_LIBS=OFF \
%endif
%if %{without debug}
       -DROCRTST_BLD_TYPE=RELEASE \
%else
       -DROCRTST_BLD_TYPE=DEBUG \
%endif
       -DCMAKE_CXX_FLAGS=-I%{rocm_path}/include \
       -DCMAKE_EXE_LINKER_FLAGS=-L%{rocm_path}/lib64 \
       -DCMAKE_INSTALL_PREFIX=%{rocm_path} \
       -DCMAKE_SHARED_LINKER_FLAGS=-L%{rocm_path}/lib64
      
%cmake_build

%install
mkdir -p %{buildroot}%{rocm_path}/bin
install -m 755 redhat-linux-build/rocminfo %{buildroot}%{rocm_path}/bin
install -m 755 rocm_agent_enumerator %{buildroot}%{rocm_path}/bin

%files devel
%{rocm_path}

%changelog
* Mon Aug 07 2023 Tom Rix <trix@redhat.com>
- Stub something together

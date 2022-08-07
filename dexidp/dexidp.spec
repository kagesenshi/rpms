# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define dex_version 2.33.0
%global debug_package %{nil}

Name: dexidp
Version: %{dex_version}
Release: 0%{?dist}
Summary: Dex OpenID Connect provider

License: Apache
URL: https://dexidp.io
Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/dexidp/dex/archive/refs/tags/v%{dex_version}.tar.gz

BuildRequires: go-compilers-golang-compiler
#Requires:

%description


%prep
%setup -q 
tar xvf %{SOURCE1}


%build
cd dex-%{dex_version}
make %{?_smp_mflags} build


%install
cd dex-%{dex_version}
mkdir -p %{buildroot}/%{_bindir}
mv bin/dex %{buildroot}/%{_bindir}/dex


%files
%defattr(-, root, root, -)
%attr(0755, root, root) %{_bindir}/dex


%changelog


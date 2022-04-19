# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/
%define debug_package %{nil}

Name: aedv-logos
Version: 1.4.2
Release: 2%{?dist}
Summary: AE Data Visualization logo resources

License: Proprietary
URL: https://aet.abyres.net/
Source0: %{name}-%{version}.tar.gz

Provides: apache-superset-logos = %{version}

%description
Logo resources override for AE Data Visualization

%prep
%setup -q


%build
%install

BRAND_DIR=${RPM_BUILD_ROOT}/opt/apache-superset/superset-frontend/src/assets/branding/

mkdir -p ${BRAND_DIR}

cp src/* ${BRAND_DIR}

%files
%defattr(644,root,root,755)
/opt/apache-superset/superset-frontend/src/assets/branding/*.png
/opt/apache-superset/superset-frontend/src/assets/branding/*.svg

%changelog
* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.2-2
- new package built with tito




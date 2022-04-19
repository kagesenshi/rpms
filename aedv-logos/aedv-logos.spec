# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/
%define debug_package %{nil}
%define python_version 3.8

Name: aedv-logos
Version: 1.4.2
Release: 4%{?dist}
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
ASSET_DIR=${RPM_BUILD_ROOT}/opt/apache-superset/lib/python%{python_version}/site-packages/superset/static/assets/images/

mkdir -p ${BRAND_DIR}
mkdir -p ${ASSET_DIR}

cp src/* ${BRAND_DIR}
cp src/superset-logo-horiz.png ${ASSET_DIR}

%files
%defattr(644,root,root,755)
/opt/apache-superset/superset-frontend/src/assets/branding/*.png
/opt/apache-superset/superset-frontend/src/assets/branding/*.svg
/opt/apache-superset/lib/python%{python_version}/site-packages/superset/static/assets/images/superset-logo-horiz.png

%changelog
* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.2-4
- fix asset path in files (kagesenshi.87@gmail.com)

* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.2-3
- add logo to asset dir (kagesenshi.87@gmail.com)

* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.2-2
- new package built with tito




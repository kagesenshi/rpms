# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/
%define python_version 3.8
%define debug_package %{nil}

Name: aedwf-logos
Version: 2.2.5
Release: 0%{?dist}
Summary: AE Data Workflow logo resources

License: Proprietary
URL: https://aet.abyres.net/
Source0: %{name}-%{version}.tar.gz

Provides: apache-airflow-logos = %{version}

%description
Logo resources override for AE Data Workflow

%prep
%setup -q


%build
%install

STATIC_DIR=${RPM_BUILD_ROOT}/opt/apache-airflow/lib/python%{python_version}/site-packages/airflow/www/static/
TEMPLATE_DIR=${RPM_BUILD_ROOT}/opt/apache-airflow/lib/python%{python_version}/site-packages/airflow/www/templates/appbuilder/

mkdir -p ${STATIC_DIR}
mkdir -p ${TEMPLATE_DIR}

cp src/navbar.html ${TEMPLATE_DIR}
cp src/aedwf-logo.png ${STATIC_DIR}


%files
%defattr(644,root,root,755)
/opt/apache-airflow/lib/python%{python_version}/site-packages/airflow/www/static/*.png
/opt/apache-airflow/lib/python%{python_version}/site-packages/airflow/www/templates/appbuilder/*.html

%changelog


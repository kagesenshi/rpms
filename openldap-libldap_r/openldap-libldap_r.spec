# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/


Name: openldap-libldap_r
Version: 0.1.0
Release: 0%{?dist}
Summary: Workaround for missing libldap_r from openldap 2.6

License: MIT
URL:    https://github.com/python-ldap/python-ldap/issues/432

Requires: openldap

%description


%prep

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
cat > ${RPM_BUILD_ROOT}/%{_libdir}/libldap_r.so << EOF
INPUT ( libldap.so )
EOF

%files
%{_libdir}/libldap_r.so

%changelog


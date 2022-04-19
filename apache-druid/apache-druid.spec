# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define vendor apache

%define druid_version 0.22.1
%define druid_package apache-druid-%{druid_version}-bin
%define python_version 2.7
%define java_version 1.8.0
%define user_name apache-druid
%define group_name apache-druid

Name: %{vendor}-%{druid}
Version: %{druid_version}
Release: 0%{?dist}
Summary: Apache Druid
Requires(pre): shadow-utils
BuildRequires: systemd-rpm-macros 

BuildRequires: /usr/bin/pathfix.py
Requires: mysql-connector-java

BuildArch:      noarch

License: Apache
URL: http://druid.apache.org
Source0: https://dlcdn.apache.org/druid/%{druid_version}/%{druid_package}.zip

Requires: java-%{java_version}-openjdk-headless 
Requires: %{vendor}-%{spark}

%description
High performance OLAP for big data with Apache Druid

%prep
%setup -q -n %{druid_package}

%build


%install
mkdir -p %{buildroot}/opt/%{vendor}/%{druid_package}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{druid}
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/%{druid}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{druid}/
mkdir -p %{buildroot}/%{_datadir}/%{name}/

cp -r * %{buildroot}/opt/%{vendor}/%{druid_package}
cp -r conf/* %{buildroot}/%{_sysconfdir}/%{druid}

ln -s ./%{druid_package} %{buildroot}/opt/%{vendor}/%{druid}

cat << EOF > %{buildroot}/%{_bindir}/%{druid}-server
#!/bin/bash
export LIVY_CONF_DIR=%{_sysconfdir}/%{druid}
/opt/%{vendor}/%{druid}/bin/druid-server \$@

EOF


cat << EOF > %{buildroot}/%{_unitdir}/%{druid}-server.service
[Unit]
Description=Spark Livy Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/%{druid}
ExecStart=%{_bindir}/%{druid}-server
WorkingDirectory=%{_sharedstatedir}/%{druid}
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_sysconfdir}/sysconfig/%{druid}
LIVY_LOG_DIR=%{_localstatedir}/log/%{druid}/
LIVY_CONF_DIR=%{_sysconfdir}/%{druid}/
EOF



cat << EOF > %{buildroot}/%{_sysconfdir}/%{druid}/druid-env.sh

umask 002
export JAVA_HOME=/usr/lib/jvm/jre-%{java_version}/
export SPARK_HOME=/opt/%{vendor}/%{spark}/
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
EOF


%files
%defattr(-, root, root, -)
%attr(0755, root, root) /usr/bin/*
%config %{_sysconfdir}/%{druid}/druid-env.sh
%{_sysconfdir}/%{druid}/*.template
%{_unitdir}/%{druid}-*.service
%{_sysconfdir}/sysconfig/%{druid}
/opt/%{vendor}/%{druid_package}
/opt/%{vendor}/%{druid}
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/%{druid}
%dir %attr(2775, %{user_name}, %{group_name}) %{_localstatedir}/log/%{druid}

%pre

getent group %{group_name} >/dev/null || groupadd -r %{group_name}
getent passwd %{user_name} >/dev/null || \
    useradd -r -g %{group_name} -d %{_sharedstatedir}/%{druid} -s /sbin/nologin \
    -c "Useful comment about the purpose of this account" %{user_name}
exit 0

%post
%systemd_post %{druid}-server.service

%preun
%systemd_preun %{druid}-server.service

%postun
%systemd_postun_with_restart %{druid}-server.service


%changelog


# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define vendor apache
%define hadoop_version 2.7
%define hive_version 3.1.2
%define hive_package apache-hive-%{hive_version}-bin
%define java_version 1.8.0
%define user_name apache-hive
%define group_name apache-hive
%define debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}


Name: %{vendor}-hive
Version: %{hive_version}
Release: 1%{?dist}
Summary: Apache Hive
Requires(pre): shadow-utils
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: /usr/bin/pathfix.py
BuildRequires: perl-interpreter findutils
AutoReq: no
AutoProv: no

License: Apache
URL: http://hive.apache.org
Source0: %{name}-%{version}.tar.gz
Source1: https://archive.apache.org/dist/hive/hive-%{hive_version}/%{hive_package}.tar.gz
Requires: java-%{java_version}-openjdk-headless
Requires: apache-hadoop >= 3.0.0

%description
Big data processing with Apache Hive

%prep
%setup -q 
tar xvf %{SOURCE1}

%build


%install
mkdir -p %{buildroot}/opt/%{vendor}/%{hive_package}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_sharedstatedir}/hive
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/hive
mkdir -p %{buildroot}/%{_localstatedir}/log/hive/
mkdir -p %{buildroot}/%{_localstatedir}/log/hive/event_log/
mkdir -p %{buildroot}/%{_sharedstatedir}/hive/warehouse/
mkdir -p %{buildroot}/%{_datadir}/%{name}/


cp -r %{hive_package}/* %{buildroot}/opt/%{vendor}/%{hive_package}
cp -r %{hive_package}/conf/* %{buildroot}/%{_sysconfdir}/hive
ln -s ./%{hive_package} %{buildroot}/opt/%{vendor}/hive

cat << EOF > %{buildroot}/%{_bindir}/hive
#!/bin/bash
export HIVE_CONF_DIR=%{_sysconfdir}/hive
/opt/%{vendor}/hive/bin/hive "\$@"

EOF

cat << EOF > %{buildroot}/%{_bindir}/beeline
#!/bin/bash
export HIVE_CONF_DIR=%{_sysconfdir}/hive
/opt/%{vendor}/hive/bin/beeline "\$@"

EOF

cat << EOF > %{buildroot}/%{_bindir}/schematool
#!/bin/bash
export HIVE_CONF_DIR=%{_sysconfdir}/hive
/opt/%{vendor}/hive/bin/schematool "\$@"

EOF

cat << EOF > %{buildroot}/%{_bindir}/metatool
#!/bin/bash
export HIVE_CONF_DIR=%{_sysconfdir}/hive
/opt/%{vendor}/hive/bin/metatool "\$@"

EOF

cat << EOF > %{buildroot}/%{_sbindir}/hiveserver2
#!/bin/bash
export HIVE_CONF_DIR=%{_sysconfdir}/hive
/opt/%{vendor}/hive/bin/hiveserver2 "\$@"

EOF

cat << EOF > %{buildroot}/%{_unitdir}/hiveserver2.service
[Unit]
Description=HiveServer2 SQL Thrift Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hive
ExecStart=%{_sbindir}/hiveserver2
WorkingDirectory=%{_sharedstatedir}/hive
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/sysconfig/hive
HIVE_LOG_DIR=%{_localstatedir}/log/hive
HIVE_CONF_DIR=%{_sysconfdir}/hive
EOF


cat << EOF > %{buildroot}/%{_sysconfdir}/hive/hive-site.xml
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://localhost/hive_metastore?createDatabaseIfNotExist=true</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>com.mysql.cj.jdbc.Driver</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>hive</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>hive</value>
        </property>
</configuration>
EOF


cat << EOF > %{buildroot}/%{_sysconfdir}/hive/beeline-site.xml
<configuration>
 <property>
 <name>beeline.hs2.jdbc.url.default</name>
 <value>local</value>
 </property>
 <property>
 <name>beeline.hs2.jdbc.url.local</name>
 <value>jdbc:hive2://localhost:10000</value>
 </property>
</configuration>
EOF

%files
%defattr(-, root, root, -)
%attr(0755, root, root) /usr/bin/*
%attr(0755, root, root) /usr/sbin/*
%{_sysconfdir}/hive/*.template
%config %{_sysconfdir}/hive/*.xml
%config %{_sysconfdir}/hive/*.properties
%{_unitdir}/hiveserver2.service
%{_sysconfdir}/sysconfig/hive
/opt/%{vendor}/%{hive_package}
/opt/%{vendor}/hive
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/hive
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/hive/warehouse
%dir %attr(2775, %{user_name}, %{group_name}) %{_localstatedir}/log/hive
%dir %attr(2777, %{user_name}, %{group_name}) %{_localstatedir}/log/hive/event_log/

%pre

getent group %{group_name} >/dev/null || groupadd -r %{group_name}
getent passwd %{user_name} >/dev/null || \
    useradd -r -g %{group_name} -d %{_sharedstatedir}/%{spark} -s /sbin/nologin \
    -c "Useful comment about the purpose of this account" %{user_name}
exit 0

%post
%systemd_post hiveserver2.service

%preun
%systemd_preun hiveserver2.service

%postun
%systemd_postun_with_restart hiveserver2.service

%changelog
* Sun Jun 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.1.2-1
- new package

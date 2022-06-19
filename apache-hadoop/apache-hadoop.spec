# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define vendor apache
%define hadoop_version 3.2.3
%define hadoop_package hadoop-%{hadoop_version}
%define java_version 1.8.0
%define user_name apache-hadoop
%define group_name apache-hadoop
%define debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}


Name: %{vendor}-hadoop
Version: %{hadoop_version}
Release: 1%{?dist}
Summary: Apache Hadoop
Requires(pre): shadow-utils
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: /usr/bin/pathfix.py
BuildRequires: perl-interpreter findutils
AutoReq: no
AutoProv: no

License: Apache
URL: http://hadoop.apache.org
Source0: %{name}-%{version}.tar.gz
Source1: https://archive.apache.org/dist/hadoop/hadoop-%{hadoop_version}/%{hadoop_package}.tar.gz
Requires: java-%{java_version}-openjdk-headless

%description
Big data processing with Apache Hadoop

%prep
%setup -q 
tar xvf %{SOURCE1}

%build


%install
mkdir -p %{buildroot}/opt/%{vendor}/%{hadoop_package}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_sharedstatedir}/hadoop
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/hadoop
mkdir -p %{buildroot}/%{_localstatedir}/log/hadoop/
mkdir -p %{buildroot}/%{_datadir}/%{name}/


cp -r %{hadoop_package}/* %{buildroot}/opt/%{vendor}/%{hadoop_package}
cp -r %{hadoop_package}/etc/hadoop/* %{buildroot}/%{_sysconfdir}/hadoop
ln -s ./%{hadoop_package} %{buildroot}/opt/%{vendor}/hadoop
rm %{buildroot}/%{_sysconfdir}/hadoop/*.cmd

cat << EOF > %{buildroot}/%{_sysconfdir}/hadoop/hadoop-env.sh
export HADOOP_OS_TYPE=\${HADOOP_OS_TYPE:-\$(uname -s)}
export JAVA_HOME=/usr/lib/jvm/jre-%{java_version}/
EOF

cat << EOF > %{buildroot}/%{_bindir}/hadoop
#!/bin/bash
export HADOOP_CONF_DIR=%{_sysconfdir}/hadoop
/opt/%{vendor}/hadoop/bin/hadoop "\$@"

EOF

cat << EOF > %{buildroot}/%{_bindir}/hdfs
#!/bin/bash
export HADOOP_CONF_DIR=%{_sysconfdir}/hadoop
/opt/%{vendor}/hadoop/bin/hdfs "\$@"

EOF

cat << EOF > %{buildroot}/%{_bindir}/yarn
#!/bin/bash
export HADOOP_CONF_DIR=%{_sysconfdir}/hadoop
/opt/%{vendor}/hadoop/bin/yarn "\$@"

EOF

cat << EOF > %{buildroot}/%{_unitdir}/yarn-resourcemanager.service
[Unit]
Description=Resource Manager Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hadoop
ExecStart=%{_bindir}/yarn resourcemanager
WorkingDirectory=%{_sharedstatedir}/hadoop
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/yarn-nodemanager.service
[Unit]
Description=Node Manager Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hadoop
ExecStart=%{_bindir}/yarn nodemanager
WorkingDirectory=%{_sharedstatedir}/hadoop
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/yarn-timelineserver.service
[Unit]
Description=YARN Timeline Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hadoop
ExecStart=%{_bindir}/yarn timelineserver
WorkingDirectory=%{_sharedstatedir}/hadoop
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/hdfs-namenode.service
[Unit]
Description=HDFS NameNode
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hadoop
ExecStart=%{_bindir}/hdfs namenode
WorkingDirectory=%{_sharedstatedir}/hadoop
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/hdfs-datanode.service
[Unit]
Description=HDFS DataNode
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/hadoop
ExecStart=%{_bindir}/hdfs datanode
WorkingDirectory=%{_sharedstatedir}/hadoop
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/sysconfig/hadoop
HADOOP_LOG_DIR=%{_localstatedir}/log/hadoop
HADOOP_CONF_DIR=%{_sysconfdir}/hadoop
EOF

%files
%defattr(-, root, root, -)
%attr(0755, root, root) /usr/bin/*
%{_sysconfdir}/hadoop/*.template
%config %{_sysconfdir}/hadoop/*.xml
%config %{_sysconfdir}/hadoop/*.properties
%config %{_sysconfdir}/hadoop/*.cfg
%config %{_sysconfdir}/hadoop/*.sh
%config %{_sysconfdir}/hadoop/*.secret
%{_sysconfdir}/hadoop/configuration.xsl
%{_sysconfdir}/hadoop/*.example
%{_sysconfdir}/hadoop/shellprofile.d/example.sh
%config %{_sysconfdir}/hadoop/workers

%{_unitdir}/hdfs-*.service
%{_unitdir}/yarn-*.service
%{_sysconfdir}/sysconfig/hadoop
/opt/%{vendor}/%{hadoop_package}
/opt/%{vendor}/hadoop
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/hadoop
%dir %attr(2775, %{user_name}, %{group_name}) %{_localstatedir}/log/hadoop

%pre

getent group %{group_name} >/dev/null || groupadd -r %{group_name}
getent passwd %{user_name} >/dev/null || \
    useradd -r -g %{group_name} -d %{_sharedstatedir}/%{spark} -s /sbin/nologin \
    -c "Useful comment about the purpose of this account" %{user_name}
exit 0

%post
%systemd_post hdfs-namenode.service
%systemd_post hdfs-datanode.service
%systemd_post yarn-resourcemanager.service
%systemd_post yarn-nodemanager.service

%preun
%systemd_preun hdfs-namenode.service
%systemd_preun hdfs-datanode.service
%systemd_preun yarn-resourcemanager.service
%systemd_preun yarn-nodemanager.service



%postun
%systemd_postun_with_restart hdfs-namenode.service
%systemd_postun_with_restart hdfs-datanode.service
%systemd_postun_with_restart yarn-resourcemanager.service
%systemd_postun_with_restart yarn-nodemanager.service



%changelog
* Sun Jun 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.2.3-1
- new package

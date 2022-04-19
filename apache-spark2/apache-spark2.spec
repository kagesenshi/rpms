# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define vendor apache
%define spark_major 2
%define spark_version 2.4.8
%define hadoop_version 2.7
%define spark_package spark-%{spark_version}-bin-hadoop%{hadoop_version}
%define python_version 2.7
%define java_version 1.8.0
%define user_name apache-spark
%define group_name apache-spark
%define spark spark%{spark_major}

Name: %{vendor}-spark%{spark_major}
Version: %{spark_version}
Release: 0%{?dist}
Summary: Apache Spark
Requires(pre): shadow-utils
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: python2

BuildRequires: /usr/bin/pathfix.py
Requires: mysql-connector-java

BuildArch:      noarch

License: Apache
URL: http://spark.apache.org
Source0: https://archive.apache.org/dist/spark/spark-%{spark_version}/%{spark_package}.tgz
Source1: hive-metastore.sql

Requires: java-%{java_version}-openjdk-headless python%{python_version}

%description
Big data processing with Apache Spark

%prep
%setup -q -n %{spark_package}

%build


%install
mkdir -p %{buildroot}/opt/%{vendor}/%{spark_package}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{spark}
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/%{spark}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{spark}/
mkdir -p %{buildroot}/%{_localstatedir}/log/%{spark}/event_log/
mkdir -p %{buildroot}/%{_sharedstatedir}/%{spark}/warehouse/
mkdir -p %{buildroot}/%{_datadir}/%{name}/

cp %{SOURCE1} %{buildroot}/%{_datadir}/%{name}/hive-metastore.sql


cp -r * %{buildroot}/opt/%{vendor}/%{spark_package}
cp -r conf/* %{buildroot}/%{_sysconfdir}/%{spark}

ln -s ./%{spark_package} %{buildroot}/opt/%{vendor}/%{spark}

cat << EOF > %{buildroot}/%{_bindir}/%{spark}-submit
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
/opt/%{vendor}/%{spark}/bin/spark-submit \$@

EOF

cat << EOF > %{buildroot}/%{_bindir}/%{spark}-beeline
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
/opt/%{vendor}/%{spark}/bin/beeline \$@

EOF

cat << EOF > %{buildroot}/%{_bindir}/%{spark}-pyspark
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
/opt/%{vendor}/%{spark}/bin/pyspark \$@

EOF

cat << EOF > %{buildroot}/%{_bindir}/%{spark}-sql
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
/opt/%{vendor}/%{spark}/bin/spark-sql \$@

EOF

cat << EOF > %{buildroot}/%{_sbindir}/%{spark}-thrift
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
export SPARK_NO_DAEMONIZE=true
/opt/%{vendor}/%{spark}/sbin/start-thriftserver.sh \$@

EOF


cat << EOF > %{buildroot}/%{_sbindir}/%{spark}-master
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
export SPARK_NO_DAEMONIZE=true
/opt/%{vendor}/%{spark}/sbin/start-master.sh \$@

EOF

cat << EOF > %{buildroot}/%{_sbindir}/%{spark}-slave
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
export SPARK_NO_DAEMONIZE=true
/opt/%{vendor}/%{spark}/sbin/start-slave.sh \$@

EOF

cat << EOF > %{buildroot}/%{_sbindir}/%{spark}-historyserver
#!/bin/bash
export SPARK_CONF_DIR=%{_sysconfdir}/%{spark}
export SPARK_NO_DAEMONIZE=true
/opt/%{vendor}/%{spark}/sbin/start-history-server.sh \$@

EOF

cat << EOF > %{buildroot}/%{_unitdir}/%{spark}-thrift.service
[Unit]
Description=Spark%{spark_major} SQL Thrift Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/%{spark}
ExecStart=%{_sbindir}/%{spark}-thrift
WorkingDirectory=%{_sharedstatedir}/%{spark}
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/%{spark}-master.service
[Unit]
Description=Spark%{spark_major} Master Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/%{spark}
ExecStart=%{_sbindir}/%{spark}-master
WorkingDirectory=%{_sharedstatedir}/%{spark}
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/%{spark}-slave.service
[Unit]
Description=Spark%{spark_major} Slave Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/%{spark}
ExecStart=%{_sbindir}/%{spark}-slave
WorkingDirectory=%{_sharedstatedir}/%{spark}
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_unitdir}/%{spark}-historyserver.service
[Unit]
Description=Spark%{spark_major} History Server
After=network-online.target

[Service]
EnvironmentFile=%{_sysconfdir}/sysconfig/%{spark}
ExecStart=%{_sbindir}/%{spark}-historyserver
WorkingDirectory=%{_sharedstatedir}/%{spark}
User=%{user_name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF


cat << EOF > %{buildroot}/%{_sysconfdir}/sysconfig/%{spark}
SPARK_LOG_DIR=%{_localstatedir}/log/%{spark}/
SPARK_CONF_DIR=%{_sysconfdir}/%{spark}/
EOF


cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/spark-defaults.conf

# spark.master                     local[*]
spark.eventLog.enabled           true
spark.eventLog.dir               %{_localstatedir}/log/%{spark}/event_log/
spark.history.fs.logDirectory    %{_localstatedir}/log/%{spark}/event_log/
spark.sql.warehouse.dir          %{_sharedstatedir}/%{spark}/warehouse/
spark.jars                       /usr/share/java/mysql-connector-java.jar
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/spark-env.sh

umask 002
export JAVA_HOME=/usr/lib/jvm/jre-%{java_version}/
export PYSPARK_PYTHON=%{_bindir}/python%{python_version}
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/hive-site.xml
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://localhost/hive_metastore</value>
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


cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/beeline-site.xml
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


%py2_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/bin/
%py2_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/python/pyspark/find_spark_home.py
%py2_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/python/run-tests.py


cat << EOF > %{buildroot}/%{_datadir}/%{name}/README.rst

You will need to create a metastore database in MySQL/MariaDB::

  create database hive_metastore;
  grant all privileges on hive_metastore.* to hive@'%' identified by 'hive';

then initialize using::

  mysql hive_metastore < %{_datadir}/%{name}/hive-metastore.sql

EOF

%files
%defattr(-, root, root, -)
%attr(0755, root, root) /usr/bin/*
%attr(0755, root, root) /usr/sbin/*
%config %{_sysconfdir}/%{spark}/spark-defaults.conf
%config %{_sysconfdir}/%{spark}/spark-env.sh
%config %{_sysconfdir}/%{spark}/hive-site.xml
%config %{_sysconfdir}/%{spark}/beeline-site.xml
%{_datadir}/%{name}/hive-metastore.sql
%{_datadir}/%{name}/README.rst
%{_sysconfdir}/%{spark}/*.template
%{_unitdir}/%{spark}-*.service
%{_sysconfdir}/sysconfig/%{spark}
/opt/%{vendor}/%{spark_package}
/opt/%{vendor}/%{spark}
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/%{spark}
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/%{spark}/warehouse
%dir %attr(2775, %{user_name}, %{group_name}) %{_localstatedir}/log/%{spark}
%dir %attr(2777, %{user_name}, %{group_name}) %{_localstatedir}/log/%{spark}/event_log/

%pre

getent group %{group_name} >/dev/null || groupadd -r %{group_name}
getent passwd %{user_name} >/dev/null || \
    useradd -r -g %{group_name} -d %{_sharedstatedir}/%{spark} -s /sbin/nologin \
    -c "Useful comment about the purpose of this account" %{user_name}
exit 0

%post
%systemd_post %{spark}-thrift.service
%systemd_post %{spark}-master.service
%systemd_post %{spark}-slave.service
%systemd_post %{spark}-historyserver.service

%preun
%systemd_preun %{spark}-thrift.service
%systemd_preun %{spark}-master.service
%systemd_preun %{spark}-slave.service
%systemd_preun %{spark}-historyserver.service



%postun
%systemd_postun_with_restart %{spark}-thrift.service
%systemd_postun_with_restart %{spark}-master.service
%systemd_postun_with_restart %{spark}-slave.service
%systemd_postun_with_restart %{spark}-historyserver.service



%changelog

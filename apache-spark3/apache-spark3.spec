# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

%define vendor apache
%define spark_major 3
%define spark_version 3.2.0
%define hadoop_version 3.2
%define spark_package spark-%{spark_version}-bin-hadoop%{hadoop_version}
%define python_version 3.8
%define java_version 1.8.0
%define user_name apache-spark
%define group_name apache-spark
%define spark spark%{spark_major}
%define debug_package %{nil}
%define venv /opt/%{vendor}/%{spark}-python
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}


Name: %{vendor}-spark%{spark_major}
Version: %{spark_version}
Release: 4%{?dist}
Summary: Apache Spark
Requires(pre): shadow-utils
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: python%{python_version}
BuildRequires: /usr/bin/pathfix.py
BuildRequires: perl-interpreter findutils

License: Apache
URL: http://spark.apache.org
Source0: %{name}-%{version}.tar.gz
Source1: https://archive.apache.org/dist/spark/spark-%{spark_version}/%{spark_package}.tgz
Requires: java-%{java_version}-openjdk-headless 
Requires: python%{python_version}

%package python
Summary: Python virtualenv for Apache Spark
Requires: python%{python_version}
AutoReq: no
AutoProv: no

%description
Big data processing with Apache Spark

%description python
Python virtualenv for Big data processing with Apache Spark

%prep
%setup -q
tar xvf %{SOURCE1}

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

/usr/bin/python%{python_version} -m venv %{buildroot}/%{venv}
%{buildroot}/%{venv}/bin/pip install numpy scikit-learn pandas dask ipykernel
%{buildroot}/%{venv}/bin/pip install %{spark_package}/python/

cp -r %{spark_package}/* %{buildroot}/opt/%{vendor}/%{spark_package}
cp -r %{spark_package}/conf/* %{buildroot}/%{_sysconfdir}/%{spark}
cp jars/*.jar  %{buildroot}/opt/%{vendor}/%{spark_package}/jars/

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
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/spark-env.sh

umask 002
export JAVA_HOME=/usr/lib/jvm/jre-%{java_version}/
export PYSPARK_PYTHON=%{venv}/bin/python
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/%{spark}/hive-site.xml
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://localhost/%{spark}_hive_metastore?createDatabaseIfNotExist=true</value>
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


# strip rpmbuildroot paths from virtualenv
grep -lrZF "#!$RPM_BUILD_ROOT" %{buildroot}/%{venv} | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
find %{buildroot}/%{venv} -type f -regex '.*egg-link$' |xargs -I% grep -lrZF "$RPM_BUILD_ROOT" % | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" %{buildroot}/%{venv} | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"

# cleanup virtualenv
find %{buildroot}/%{venv} -regex '.*\.pyc$' -exec rm '{}' ';'
find %{buildroot}/%{venv} -regex '.*\.pyo$' -exec rm '{}' ';'

%py3_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/bin/
%py3_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/python/pyspark/find_spark_home.py
%py3_shebang_fix %{buildroot}/opt/%{vendor}/%{spark_package}/python/run-tests.py
%py3_shebang_fix %{buildroot}/%{venv}


%files
%defattr(-, root, root, -)
%attr(0755, root, root) /usr/bin/*
%attr(0755, root, root) /usr/sbin/*
%config %{_sysconfdir}/%{spark}/spark-defaults.conf
%config %{_sysconfdir}/%{spark}/spark-env.sh
%config %{_sysconfdir}/%{spark}/hive-site.xml
%config %{_sysconfdir}/%{spark}/beeline-site.xml
%{_sysconfdir}/%{spark}/*.template
%{_unitdir}/%{spark}-*.service
%{_sysconfdir}/sysconfig/%{spark}
/opt/%{vendor}/%{spark_package}
/opt/%{vendor}/%{spark}
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/%{spark}
%dir %attr(2775, %{user_name}, %{group_name}) %{_sharedstatedir}/%{spark}/warehouse
%dir %attr(2775, %{user_name}, %{group_name}) %{_localstatedir}/log/%{spark}
%dir %attr(2777, %{user_name}, %{group_name}) %{_localstatedir}/log/%{spark}/event_log/

%files python
%defattr(-, root, root, -)
%{venv}


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
* Tue Aug 02 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.2.0-4
- fix path of spark3/python (kagesenshi.87@gmail.com)

* Tue Aug 02 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.2.0-3
- added mariadb and mssql drivers (kagesenshi.87@gmail.com)

* Mon Jun 27 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.2.0-2
- added ipykernel and pyspark library (kagesenshi.87@gmail.com)
* Mon Apr 25 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 3.2.0-1
- update to use tito



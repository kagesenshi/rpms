%define debug_package %{nil}
%define _build_id_links none
%define python_version 3.8
%define user_name apache-airflow
%define group_name apache-airflow

Name:       apache-airflow
Version:    2.2.5
Release:    6%{?dist}
Summary:    ETL workflow management and monitoring

License:    Apache2
URL:        http://airflow.apache.org
AutoProv: no
AutoReq: no
Source0:    https://dlcdn.apache.org/airflow/%{version}/%{name}-%{version}-source.tar.gz
BuildRequires:  python%{python_version} 
BuildRequires: pkgconfig(python-%{python_version}) >= %{python_version}
BuildRequires: postgresql-devel mysql-devel
BuildRequires: gcc-c++ cyrus-sasl-devel
BuildRequires: postgresql-devel
BuildRequires: perl-interpreter findutils
BuildRequires: unixODBC-devel libev-devel
BuildRequires: systemd-rpm-macros
BuildRequires: krb5-devel openldap-devel
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: /usr/bin/pathfix.py
#BuildRequires: npm yarnpkg
Requires: %{name}-common = %{version}-%{release}

%package common
Summary: ETL workflow management and monitoring
Requires: python%{python_version}
Requires: pkgconfig(python-%{python_version}) == %{python_version}
Requires: postgresql-libs postgresql 
Requires: libffi krb5-libs openldap-clients openldap
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Provides: %{name} = %{version}-%{release}
Requires: %{name}-logos = %{version}
AutoProv: no
AutoReq: no


%package logos
Summary: Logo files for %{name}
AutoProv: no
AutoReq: no


%description
ETL workflow management and monitoring on Apache Airflow

%description common
ETL workflow management and monitoring on Apache Airflow

%description logos
Logo files for Apache Airflow

%prep
rm -rf %{_builddir}/%{name}/
%setup -q -b 0 

%build
rm -rf $RPM_BUILD_ROOT
#pushd airflow/www
#   ./compile_assets.sh
#popd 

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/%{name}/
#cp -r * ${RPM_BUILD_ROOT}/opt/%{name}/
python%{python_version} -m venv ${RPM_BUILD_ROOT}/opt/%{name}/
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip install "apache-airflow[celery,async,postgres,mysql,odbc,apache.druid,apache.spark,apache.webhdfs,rabbitmq,redis,ftp,grpc,http,imap,jdbc,kerberos,ldap,papermill,sftp,sqlite,ssh]" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-%{version}/constraints-%{python_version}.txt
#pushd ${RPM_BUILD_ROOT}/opt/%{name}/lib/python%{python_version}/site-packages/airflow/www/
#   ./compile_assets.sh
#popd

# create resource dirs
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}/
mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/logrotate.d/
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}

# link to airflow home
ln -s ../../var/log/%{name} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/logs
ln -s ../../var/lib/%{name} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/state


# create environmentfile
cat > ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/%{name} << EOF
AIRFLOW_HOME="/%{_sysconfdir}/%{name}"
PATH="/opt/%{name}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
EOF

# create script
cat > ${RPM_BUILD_ROOT}/%{_bindir}/%{name} << EOF
#!/usr/bin/bash
sudo -u %{user_name} AIRFLOW_HOME="/%{_sysconfdir}/%{name}" /opt/%{name}/bin/airflow \$@;
EOF

# logrotate config
cat << EOF > ${RPM_BUILD_ROOT}/%{_sysconfdir}/logrotate.d/%{name} 
/var/log/%{name}/*.log {
    daily
    dateext
    maxage 7
    dateformat -%Y-%m-%d
    dateyesterday
    size 100M
    rotate 2
    create 0644 %{user_name} %{group_name}
}
EOF

# systemd config
cat << EOF > ${RPM_BUILD_ROOT}/%{_unitdir}/%{name}-web.service
[Unit]
Description="%{name} Web %i"
After=network.target 

[Service]
User=%{user_name}
Group=%{group_name}
Type=simple
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
RuntimeDirectory=%{name}
ExecStart=/opt/%{name}/bin/airflow webserver --pid /run/%{name}/airflow.pid
PIDFile=/run/%{name}/airflow.pid
Restart=on-failure
RestartSec=5s
LimitNOFILE=40960

[Install]
WantedBy=multi-user.target

EOF


cat << EOF > ${RPM_BUILD_ROOT}/%{_unitdir}/%{name}-worker.service

[Unit]
Description="%{name} Worker %i"
After=network.target 

[Service]
User=%{user_name}
Group=%{group_name}
Type=simple
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
ExecStart=/opt/%{name}/bin/airflow celery worker
Restart=on-failure
RestartSec=5s
LimitNOFILE=40960

[Install]
WantedBy=multi-user.target

EOF


cat << EOF > ${RPM_BUILD_ROOT}/%{_unitdir}/%{name}-scheduler.service
[Unit]
Description="%{name} Scheduler %i"
After=network.target 

[Service]
User=%{user_name}
Group=%{user_name}
Type=simple
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
WorkingDirectory=/var/lib/%{name}/
ExecStart=/opt/%{name}/bin/airflow scheduler
Restart=on-failure
RestartSec=5s
LimitNOFILE=40960

[Install]
WantedBy=multi-user.target
EOF

# strip rpmbuildroot paths
grep -lrZF "#!$RPM_BUILD_ROOT" $RPM_BUILD_ROOT | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
find $RPM_BUILD_ROOT -type f -regex '.*egg-link$' |xargs -I% grep -lrZF "$RPM_BUILD_ROOT" % | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/bin/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"

## replace logo
#NAVTMPL=`ls $RPM_BUILD_ROOT/opt/%{name}/eggs/cp*/apache_airflow*/airflow/www/templates/appbuilder/navbar.html`
#cp navbar.html $NAVTMPL
#
#STATIC_DIR=`ls -d $RPM_BUILD_ROOT/opt/%{name}/eggs/cp*/apache_airflow*/airflow/www/static/`
#cp aedwf-logo.png $STATIC_DIR/logo.png

# cleanup
find ${RPM_BUILD_ROOT} -regex '.*\.pyc$' -exec rm '{}' ';'
find ${RPM_BUILD_ROOT} -regex '.*\.pyo$' -exec rm '{}' ';'

%py3_shebang_fix $RPM_BUILD_ROOT/opt/%{name}/

export QA_RPATHS=$(( 0x0002 ))

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
/usr/bin/getent group %{group_name} >/dev/null || /usr/sbin/groupadd -r %{group_name}
/usr/bin/getent passwd %{user_name} >/dev/null || /usr/sbin/useradd -r \
     -g %{group_name} -d /opt/%{name}/ -s /sbin/nologin %{user_name}

%post common
/opt/%{name}/bin/python -m compileall -q /opt/%{name}/ > /dev/null 2>&1 
/usr/bin/systemctl daemon-reload
%systemd_post %{name}-web.service
%systemd_post %{name}-scheduler.service
%systemd_post %{name}-worker.service

%preun common
%systemd_preun %{name}-web.service
%systemd_preun %{name}-scheduler.service
%systemd_preun %{name}-worker.service

%postun common
%systemd_postun_with_restart %{name}-web.service
%systemd_postun_with_restart %{name}-scheduler.service
%systemd_postun_with_restart %{name}-worker.service
/usr/bin/systemctl daemon-reload

%files 
%dir /opt/%{name}/

%files common
%defattr(644, root, root ,755)
%exclude /opt/%{name}/lib/python*/site-packages/airflow/www/templates/appbuilder/navbar.html
/opt/%{name}/*
%attr(755, root, root) %{_bindir}/%{name}
%attr(755, root, root) /opt/%{name}/bin/*
%attr(755, %{user_name}, %{group_name}) %{_sysconfdir}/%{name}
%config %{_sysconfdir}/sysconfig/%{name}
%attr(644, root, root) %{_unitdir}/%{name}-web.service
%attr(-,root,root) %{_unitdir}/%{name}-scheduler.service
%attr(-,root,root) %{_unitdir}/%{name}-worker.service
%attr(755,%{user_name},%{group_name}) /var/log/%{name}
%attr(755,%{user_name},%{group_name}) /var/lib/%{name}

%attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}

%files logos
%attr(644,root,root) /opt/%{name}/lib/python*/site-packages/airflow/www/templates/appbuilder/navbar.html


%changelog
* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 2.2.5-6
- dont use autoreqprov in common (kagesenshi.87@gmail.com)

* Wed Apr 20 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 2.2.5-5
- lock requires logo to version but not to release tag
  (kagesenshi.87@gmail.com)

* Tue Apr 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 2.2.5-4
- build from pypi

* Tue Apr 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 2.2.5-3
- change path of navbar html (kagesenshi.87@gmail.com)

* Tue Apr 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 2.2.5-2
- update to use tito

* Thu Feb 11 2021 Izhar Firdaus <kagesenshi.87@gmail.com> 1.0.0-2
- new package built with tito

* Thu Feb 11 2021 Izhar Firdaus <kagesenshi.87@gmail.com>
- add missing deps (kagesenshi.87@gmail.com)

* Thu Feb 11 2021 Izhar Firdaus <kagesenshi.87@gmail.com> 1.0.1-1
- new package built with tito



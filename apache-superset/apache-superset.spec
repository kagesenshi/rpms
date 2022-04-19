%define debug_package %{nil}
%define __strip /bin/true
%define _build_id_links none
%define python_version 3.8
%define user_name apache-superset
%define group_name apache-superset

Name:       apache-superset
Version:    1.4.2
Release:    8%{?dist}
Summary:    Data visualization and dashboard

License:    Apache2
URL:        http://superset.apache.org
AutoReq: no
AutoProv: no
Source0:    https://dlcdn.apache.org/superset/%{version}/%{name}-%{version}-source.tar.gz
BuildRequires:  python%{python_version}
BuildRequires: pkgconfig(python-%{python_version}) >= %{python_version}
BuildRequires: postgresql-devel mysql-devel
BuildRequires: gcc-c++ cyrus-sasl-devel
BuildRequires: postgresql-devel
BuildRequires: perl-interpreter findutils
BuildRequires: git
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: /usr/bin/pathfix.py
Requires: %{name}-common = %{version}-%{release}

%package common
Summary: Data visualization and dashboard
Requires: python%{python_version}
Requires: pkgconfig(python-%{python_version}) == %{python_version}
Requires:   postgresql-libs postgresql 
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Requires: chromedriver
Requires: %{name}-logos = %{version}
Provides: %{name} = %{version}-%{release}
AutoReq: no
AutoProv: no

%package logos
Summary: Logos for %{name}
AutoReq: no
AutoProv: no

%description
Data visualization and dashboard on Apache Superset

%description common
Data visualization and dashboard on Apache Superset

%description logos
Logo files for Apache Superset

%prep
rm -rf %{_builddir}/%{name}/
%setup -q -b 0 -n %{name}-%{version}rc1

%build
rm -rf $RPM_BUILD_ROOT

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/%{name}/
cp -r * ${RPM_BUILD_ROOT}/opt/%{name}/
cd ${RPM_BUILD_ROOT}/opt/%{name}/
python%{python_version} -m venv ${RPM_BUILD_ROOT}/opt/%{name}/
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip install -r requirements/development.txt
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip uninstall apache-superset -y
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip install %{name}==%{version}
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip install gevent

# create resource dirs
mkdir -p ${RPM_BUILD_ROOT}/usr/bin/
mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d/
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig/
mkdir -p ${RPM_BUILD_ROOT}/etc/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/

# create environmentfile
cat > ${RPM_BUILD_ROOT}/etc/sysconfig/%{name} << EOF
WEB_LISTEN_ADDRESS="0.0.0.0:8999"
CELERY_WORKERS=4
GUNICORN_OPTS="-w 10 -k gevent --timeout 120 --limit-request-line 0 --limit-request-field_size 0"
EOF

# create script
cat > ${RPM_BUILD_ROOT}/usr/bin/%{name} << EOF
#!/usr/bin/bash

export PYTHONPATH="/etc/%{name}"
/opt/%{name}/bin/superset \$@;

EOF

# create default config 
cat > ${RPM_BUILD_ROOT}/etc/%{name}/superset_config.py << EOF
from celery.schedules import crontab
from flask_caching.backends.rediscache import RedisCache

FEATURE_FLAGS = {
    'THUMBNAILS': True,
    'THUMBNAILS_SQLA_LISTENERS': True
}

SECRET_KEY = "\2\1thisismyscretkey\1\2\\e\\y\\y\\h"
SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/%{name}"
DATA_DIR = "/var/lib/%{name}"
class CeleryConfig:  # pylint: disable=too-few-public-methods
    BROKER_URL = "redis://localhost:6379/2"
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks",
                      "superset.tasks.thumbnails")
    CELERY_RESULT_BACKEND = "db+postgresql://postgres@localhost:5432/%{name}_cache"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True
    CELERY_ANNOTATIONS = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": 120,
            "soft_time_limit": 150,
            "ignore_result": True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        }
    }

CELERY_CONFIG = CeleryConfig

THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,
    'CACHE_KEY_PREFIX': 'superset_thumbnail',
    'CACHE_REDIS_URL':  'redis://localhost:6379/3',
}

WEBDRIVER_BASEURL = "http://localhost:8999"
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
]

EOF

# logrotate config
cat << EOF > ${RPM_BUILD_ROOT}/%{_sysconfdir}/logrotate.d/%{name}
/var/log/%{name}/*/*/*/*/*.log {
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
cat << EOF > ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-web.service
[Unit]
Description="%{name} Web %i"
After=network.target 

[Service]
User=%{name}
Group=%{name}
Type=simple
Environment=PYTHONPATH=/etc/%{name}/
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
ExecStart=/opt/%{name}/bin/gunicorn -b \${WEB_LISTEN_ADDRESS} \$GUNICORN_OPTS "superset.app:create_app()"
Restart=on-failure
RestartSec=5s
LimitNOFILE=40960

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-worker.service
[Unit]
Description="%{name} Worker %i"
After=network.target 

[Service]
User=%{name}
Group=%{name}
Type=simple
Environment=PYTHONPATH=/etc/%{name}/
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
ExecStart=/opt/%{name}/bin/celery worker --app=superset.tasks.celery_app:app --pool=prefork -O fair -c \${CELERY_WORKERS}
Restart=on-failure
RestartSec=5s
LimitNOFILE=40960

[Install]
WantedBy=multi-user.target

EOF

cat << EOF > ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-scheduler.service

[Unit]
Description="%{name} Scheduler %i"
After=network.target 

[Service]
User=%{name}
Group=%{name}
Type=simple
Environment=PYTHONPATH=/etc/%{name}/
Environment=ACCESS_LOG=/var/log/%{name}/access.log
Environment=ERROR_LOG=/var/log/%{name}/errors.log
Environment=PYTHONUNBUFFERED=1
Environment=LC_ALL=en_US.utf8
Environment=LANG=en_US.utf8
EnvironmentFile=/etc/sysconfig/%{name}
WorkingDirectory=/var/lib/%{name}/
ExecStart=/opt/%{name}/bin/celery beat --app=superset.tasks.celery_app:app 
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

# cleanup
find ${RPM_BUILD_ROOT} -regex '.*\.pyc$' -exec rm '{}' ';'
find ${RPM_BUILD_ROOT} -regex '.*\.pyo$' -exec rm '{}' ';'
find ${RPM_BUILD_ROOT}/opt/%{name}/lib/python%{python_version}/site-packages/superset/migrations/ \
    -type f -executable -exec chmod -x '{}' ';'
find ${RPM_BUILD_ROOT}/opt/%{name}/lib/python%{python_version}/site-packages/superset/static/ \
    -type f -executable -exec chmod -x '{}' ';'

%py3_shebang_fix $RPM_BUILD_ROOT/opt/%{name}/

export QA_RPATHS=$(( 0x0002 ))

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
/usr/bin/getent group %{group_name} >/dev/null || /usr/sbin/groupadd -r %{group_name}
/usr/bin/getent passwd %{user_name} >/dev/null || /usr/sbin/useradd -r \
     -g %{group_name} -d /opt/%{name}/ -s /sbin/nologin %{user_name}

%post common
/opt/%{name}/venv/bin/python -m compileall -q /opt/%{name}/ > /dev/null 2>&1 
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
%exclude /opt/%{name}/superset-frontend/src/assets/branding/
/opt/%{name}/*
%attr(755, root, root) /usr/bin/%{name}
%attr(755, root, root) /opt/%{name}/bin/*
%config /etc/sysconfig/%{name}
%attr(660, %{user_name}, %{group_name}) %config /etc/%{name}/superset_config.py
%attr(644, root, root) /usr/lib/systemd/system/%{name}-web.service
%attr(-,root,root) /usr/lib/systemd/system/%{name}-scheduler.service
%attr(-,root,root) /usr/lib/systemd/system/%{name}-worker.service
%attr(755,%{user_name},%{group_name}) /var/log/%{name}
%attr(755,%{user_name},%{group_name}) /var/lib/%{name}
%attr(-,root,root) /etc/logrotate.d/%{name}

%files logos
%attr(644, root, root) /opt/%{name}/superset-frontend/src/assets/branding/*

%changelog
* Tue Apr 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.2-8
- bump to 1.4.2

* Tue Apr 19 2022 Izhar Firdaus <kagesenshi.87@gmail.com> 1.4.1rc1-7
- initial update to tito

* Sat May 08 2021 Izhar Firdaus <kagesenshi.87@gmail.com> 1.1.0-3
- fix cython dep issue in CentOS (kagesenshi.87@gmail.com)

* Fri May 07 2021 Izhar Firdaus <kagesenshi.87@gmail.com> 1.1.0-2
- use releasetagger (kagesenshi.87@gmail.com)
- bump version to 1.1.0 (kagesenshi.87@gmail.com)
- configure thumbnail caching with redis (kagesenshi.87@gmail.com)
- added tito release config (kagesenshi.87@gmail.com)
- bump superset version (kagesenshi.87@gmail.com)
- fix ownership config (kagesenshi.87@gmail.com)
- package is now managed using tito (kagesenshi.87@gmail.com)

* Mon Feb 08 2021 Izhar Firdaus <kagesenshi.87@gmail.com> 1.0.0-1
- new package built with tito

* Thu Feb 4 2021 Izhar Firdaus - 1.0.0
- initial package

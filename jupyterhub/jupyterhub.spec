%define debug_package %{nil}
%define _build_id_links none
%define python_version 3.8
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%define jupyterlab_version 3.2.8

Name:       jupyterhub
Version:    2.0.2
Release:    3%{?dist}
Summary:    Multi-user jupyter hub

License:    GPLv3+
URL:        https://jupyter.org
AutoReqProv: no
Source0:    https://github.com/jupyterhub/jupyterhub/archive/refs/tags/2.0.2.zip#/%{name}-%{version}.zip
BuildRequires:  python%{python_version}
BuildRequires: pkgconfig(python-%{python_version}) >= %{python_version}
BuildRequires: postgresql-devel mysql-devel
BuildRequires: gcc-c++ cyrus-sasl-devel
BuildRequires: postgresql-devel
BuildRequires: perl-interpreter findutils
BuildRequires: git npm
BuildRequires: systemd-rpm-macros python-rpm-macros
BuildRequires: /usr/bin/pathfix.py
BuildRequires: desktop-file-utils

Requires: python%{python_version}
Requires: pkgconfig(python-%{python_version}) == %{python_version}
Requires:   postgresql-libs postgresql 
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Requires: /usr/bin/xelatex /usr/bin/mf /usr/bin/bibtex
Requires: texlive-tcolorbox texlive-parskip texlive-upquote
Requires: texlive-eurosym texlive-adjustbox
Requires: texlive-titling texlive-ulem texlive-jknapltx
Requires: tex(rsfs10.tfm)

%description
Multi-user jupyter

%prep
rm -rf %{_builddir}/%{name}-%{version}/
%setup -q 

%build
rm -rf $RPM_BUILD_ROOT

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}/
mkdir -p ${RPM_BUILD_ROOT}/opt/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/applications/
mkdir -p ${RPM_BUILD_ROOT}/%{_sharedstatedir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_unitdir}/

cp -r * ${RPM_BUILD_ROOT}/opt/%{name}/
cd ${RPM_BUILD_ROOT}/opt/%{name}/
python%{python_version} -m venv ${RPM_BUILD_ROOT}/opt/%{name}/
${RPM_BUILD_ROOT}/opt/%{name}/bin/pip install . psycopg2-binary pymssql "jupyterlab==%{jupyterlab_version}" jupyter-server-proxy \
    jupyterlab-git jupyterlab_latex jupyterlab-pullrequests jupyterlab-fasta \
    jupyterlab-geojson jupyterlab-katex  jupyterlab-mathjax3 jupyterlab-vega2 \
    jupyterlab-vega3 jupyterlab_widgets
pushd ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}
   ${RPM_BUILD_ROOT}/opt/%{name}/bin/jupyterhub --generate-config
popd
pushd ${RPM_BUILD_ROOT}/opt/%{name}/
   npm install configurable-http-proxy
   chmod a+x ./node_modules/.bin/configurable-http-proxy
   chmod a+x ./node_modules/configurable-http-proxy/bin/configurable-http-proxy
popd
ln -s /opt/%{name}/node_modules/.bin/configurable-http-proxy %{buildroot}/%{_bindir}/configurable-http-proxy
ln -s /opt/%{name}/bin/jupyterhub %{buildroot}/%{_bindir}/jupyterhub
ln -s /opt/%{name}/bin/jupyterhub-singleuser %{buildroot}/%{_bindir}/jupyterhub-singleuser


# strip rpmbuildroot paths
grep -lrZF "#!$RPM_BUILD_ROOT" $RPM_BUILD_ROOT | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
find $RPM_BUILD_ROOT -type f -regex '.*egg-link$' |xargs -I% grep -lrZF "$RPM_BUILD_ROOT" % | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/bin/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/node_modules/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/lib/python%{python_version}/site-packages/jupyterhub-%{version}.dist-info/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/jupyterhub_config.py | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"

cat << EOF > %{buildroot}/%{_unitdir}/%{name}.service
[Unit]
Description=JupyterHub
After=network-online.target

[Service]
AmbientCapabilities=CAP_SETUID CAP_SETGID
EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}
ExecStart=%{_bindir}/jupyterhub -f %{_sysconfdir}/%{name}/jupyterhub_config.py
WorkingDirectory=%{_sharedstatedir}/%{name}

Type=simple
KillSignal=SIGTERM
Restart=on-failure
SendSIGKILL=no

[Install]
WantedBy=default.target

EOF

cat << EOF > ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/%{name}
PATH=/opt/%{name}/bin:/usr/local/bin:/usr/bin:/bin/
EOF



# cleanup
find ${RPM_BUILD_ROOT} -regex '.*\.pyc$' -exec rm '{}' ';'
find ${RPM_BUILD_ROOT} -regex '.*\.pyo$' -exec rm '{}' ';'

%py3_shebang_fix $RPM_BUILD_ROOT/opt/%{name}/

export QA_RPATHS=$(( 0x0002 ))

%post
%systemd_post %{name}.service
/opt/%{name}/venv/bin/python -m compileall -q /opt/%{name}/ > /dev/null 2>&1 
/usr/bin/systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root ,755)
%attr(755, root, root) /opt/%{name}/bin/*
%attr(755, root, root) %{_bindir}/*
%attr(755, root, root) /opt/%{name}/node_modules/.bin/*
%attr(755, root, root) /opt/%{name}/node_modules/configurable-http-proxy/bin/*
/opt/%{name}/
%dir %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%config %{_sysconfdir}/%{name}/jupyterhub_config.py
%config %{_sysconfdir}/sysconfig/%{name}

%changelog
* Sun Jan 16 2022 Izhar Firdaus - 2.0.2
- initial package

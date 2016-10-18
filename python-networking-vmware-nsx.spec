%global drv_vendor VMware
%global srcname vmware-nsx
%global docpath doc/build/html
%global service neutron

Name:           python-networking-%{srcname}
Version:        1.0.1
Release:        1
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
# TODO: really, there are no packages on PyPI or anywhere else
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://tarballs.openstack.org/%{srcname}/%{srcname}-%{version}.tar.gz

# TODO: some of those dependencies are not available in repos, so left them version-less
BuildArch:      noarch
BuildRequires:  python2-devel
#BuildRequires:  python-mock >= 1.1
BuildRequires:  python-mock
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

#Requires:	python-eventlet >= 0.17.4
Requires:	python-eventlet
Requires:	python-httplib2 >= 0.7.5
Requires:	python-netaddr >= 0.7.12
Requires:	python-neutron
Requires:	python-oslo-concurrency >= 2.1.0
Requires:	python-oslo-config >= 2:1.11.0
Requires:	python-oslo-db >= 1.12.0
Requires:	python-oslo-i18n >= 1.5.0
Requires:	python-oslo-log >= 1.6.0
Requires:	python-oslo-serialization >= 1.4.0
Requires:	python-oslo-service >= 0.1.0
Requires:	python-oslo-utils >= 1.9.0
Requires:	python-oslo-vmware >= 0.13.1
Requires:	python-pbr >= 1.3
Requires:	python-retrying >= 1.2.3
Requires:	python-six >= 1.9.0
Requires:	python-sqlalchemy >= 0.9.7
Requires:	python-stevedore >= 1.5.0
#Requires:	python-tooz >= 0.16.0
Requires:	python-tooz


%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%package doc
Summary:        %{summary} documentation
Requires:       %{name} = %{version}-%{release}


%description doc
This package contains documentation for %{drv_vendor} networking driver for
OpenStack Neutron.


%prep
%setup -q -n %{srcname}-%{upstream_version}

rm requirements.txt test-requirements.txt


%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/plugins/*/*.ini


%files
%license LICENSE
%{_bindir}/neutron-check-nsx-config
%{_bindir}/nsxadmin
%{python2_sitelib}/vmware_nsx
%{python2_sitelib}/vmware_nsx-%{version}-py%{python2_version}.egg-info
%dir %{_sysconfdir}/%{service}/plugins/vmware
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/vmware/*.ini


%files doc
%license LICENSE
%doc %{docpath}


%changelog
* Mon Jun 06 2016 Haikel Guemar <hguemar@fedoraproject.org> 1.0.1-1
- Update to 1.0.1


%global vendor VMware
%global srcname vmware-nsx
%global docpath doc/build/html

Name:           python-networking-%{srcname}
Version:        XXX
Release:        XXX
Summary:        %{vendor} OpenStack Neutron driver

License:        ASL 2.0
# TODO: really, there are no packages on PyPI or anywhere else
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

Requires:	python-eventlet >= 0.16.1
Requires:	python-httplib2 >= 0.7.5
Requires:	python-netaddr >= 0.7.12
Requires:	python-neutron
Requires:	python-oslo-concurrency >= 1.8.0
Requires:	python-oslo-config >= 2:1.9.3
Requires:	python-oslo-db >= 1.7.0
Requires:	python-oslo-i18n >= 1.5.0
Requires:	python-oslo-log >= 1.0.0
Requires:	python-oslo-serialization >= 1.4.0
Requires:	python-oslo-utils >= 1.4.0
Requires:	python-oslo-vmware >= 0.11.2
Requires:	python-pbr >= 0.6
Requires:	python-retrying >= 1.2.3
Requires:	python-six >= 1.7.0
Requires:	python-sqlalchemy >= 0.9.7
Requires:	python-stevedore >= 1.3.0


%description
This package contains %{vendor} networking driver for OpenStack Neutron.


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
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%license LICENSE
%doc %{docpath}
%{_bindir}/neutron-check-nsx-config
%{python2_sitelib}/vmware_nsx
%{python2_sitelib}/vmware_nsx-%{version}-py%{python2_version}.egg-info


%changelog

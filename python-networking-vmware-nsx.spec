%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global drv_vendor VMware
%global srcname vmware-nsx
%global docpath doc/build/html
%global service neutron
%global pyname vmware_nsx

%global with_doc 1

Name:           python-networking-%{srcname}
Version:        XXX
Release:        XXX
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
# TODO: really, there are no packages on PyPI or anywhere else
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://tarballs.openstack.org/%{srcname}/%{srcname}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python2-mock
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-tenacity
BuildRequires:  python2-vmware-nsxlib
# Required for config file generation
BuildRequires:  python2-debtcollector
BuildRequires:  python2-oslo-config >= 2:5.1.0
BuildRequires:  python2-oslo-i18n >= 3.15.3
BuildRequires:  python2-oslo-vmware >= 2.17.0
BuildRequires:  python-neutron
BuildRequires:  openstack-macros

Requires:       python-decorator
Requires:       python-enum34
Requires:       python2-eventlet
Requires:       python-httplib2 >= 0.9.1
Requires:       python2-netaddr >= 0.7.18
Requires:       python-neutron >= 1:13.0.0
Requires:       python-neutron-lib >= 1.18.0
Requires:       python2-openstackclient >= 3.12.0
Requires:       python2-osc-lib >= 1.8.0
Requires:       python2-oslo-concurrency >= 3.25.0
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-context >= 2.19.2
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-service >= 1.24.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-oslo-vmware >= 2.17.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-prettytable
Requires:       python2-six >= 1.10.0
Requires:       python2-sqlalchemy >= 1.0.10
Requires:       python2-stevedore >= 1.20.0
Requires:       python2-tenacity >= 3.2.1
Requires:       python2-tooz >= 1.58.0
Requires:       python2-vmware-nsxlib
Requires:       python2-ovsdbapp >= 0.10.0

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%if 0%{?with_doc}
%package doc
Summary:        %{summary} documentation
Requires:       %{name} = %{version}-%{release}


%description doc
This package contains documentation for %{drv_vendor} networking driver for
OpenStack Neutron.
%endif

%prep
%setup -q -n %{srcname}-%{upstream_version}

%py_req_cleanup


%build
%{__python2} setup.py build

%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo
%endif


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}

# Build config file
PYTHONPATH=. tools/generate_config_file_samples.sh

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware
mv etc/nsx.ini.sample %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware/nsx.ini

%files
%license LICENSE
%{_bindir}/nsx-migration
%{_bindir}/neutron-check-nsx-config
%{_bindir}/nsxadmin
%{python2_sitelib}/%{pyname}
%{python2_sitelib}/%{pyname}-%{version}-py%{python2_version}.egg-info
%dir %{_sysconfdir}/%{service}/plugins/vmware
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/vmware/*.ini


%if 0%{?with_doc}
%files doc
%license LICENSE
%doc %{docpath}
%endif

%changelog


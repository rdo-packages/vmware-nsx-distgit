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

# TODO: some of those dependencies are not available in repos, so left them version-less
BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
#BuildRequires:  python-mock >= 1.1
BuildRequires:  python-mock
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-tenacity
BuildRequires:  python-vmware-nsxlib
# Required for config file generation
BuildRequires:  python-debtcollector
BuildRequires:  python-oslo-config >= 2:1.11.0
BuildRequires:  python-oslo-i18n >= 1.5.0
BuildRequires:  python-oslo-vmware >= 0.13.1
BuildRequires:  python-neutron

#Requires:      python-eventlet >= 0.17.4
Requires:       python-decorator
Requires:       python-enum34
Requires:       python-eventlet
Requires:       python-httplib2 >= 0.7.5
Requires:       python-netaddr >= 0.7.12
Requires:       python-neutron
Requires:       python-neutron-lib >= 1.1.0
Requires:       python-openstackclient >= 3.3.0
Requires:       python-osc-lib >= 1.2.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 2:3.14.0
Requires:       python-oslo-db >= 4.15.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.11.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.10.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-oslo-vmware >= 2.17.0
Requires:       python-pbr >= 1.8
Requires:       python-prettytable
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-stevedore >= 1.17.1
#Requires:       python-tenacity >= 3.1.1
Requires:       python-tenacity
#Requires:      python-tooz >= 1.28.0
Requires:       python-tooz
Requires:       python-vmware-nsxlib

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

rm requirements.txt test-requirements.txt


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

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/vmware-nsx/commit/?id=3f56cc86699c685c7328b340dd4990eff5bd64c9

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-tenacity
BuildRequires:  python%{pyver}-vmware-nsxlib
# Required for config file generation
BuildRequires:  python%{pyver}-debtcollector
BuildRequires:  python%{pyver}-oslo-config >= 2:5.1.0
BuildRequires:  python%{pyver}-oslo-i18n >= 3.15.3
BuildRequires:  python%{pyver}-oslo-vmware >= 2.17.0
BuildRequires:  python%{pyver}-neutron
BuildRequires:  openstack-macros

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

%package -n python%{pyver}-networking-%{srcname}
%{?python_provide:%python_provide python%{pyver}-networking-%{srcname}}
Summary:        %{drv_vendor} OpenStack Neutron driver

Requires:       python%{pyver}-decorator
Requires:       python%{pyver}-enum34
Requires:       python%{pyver}-eventlet
Requires:       python%{pyver}-httplib2 >= 0.9.1
Requires:       python%{pyver}-netaddr >= 0.7.18
Requires:       python%{pyver}-neutron >= 1:13.0.0
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-openstackclient >= 3.12.0
Requires:       python%{pyver}-osc-lib >= 1.8.0
Requires:       python%{pyver}-oslo-concurrency >= 3.25.0
Requires:       python%{pyver}-oslo-config >= 2:5.1.0
Requires:       python%{pyver}-oslo-context >= 2.19.2
Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-service >= 1.24.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-vmware >= 2.17.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-prettytable
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-sqlalchemy >= 1.0.10
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-tenacity >= 3.2.1
Requires:       python%{pyver}-tooz >= 1.58.0
Requires:       python%{pyver}-vmware-nsxlib
Requires:       python%{pyver}-ovsdbapp >= 0.10.0

%description -n python%{pyver}-networking-%{srcname}
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
%{pyver_build}

%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx
rm %{docpath}/.buildinfo
%endif


%install
export PBR_VERSION=%{version}
%{pyver_install}

# Build config file
PYTHONPATH=. tools/generate_config_file_samples.sh

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware
mv etc/nsx.ini.sample %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware/nsx.ini

%files -n python%{pyver}-networking-%{srcname}
%license LICENSE
%{_bindir}/nsx-migration
%{_bindir}/neutron-check-nsx-config
%{_bindir}/nsxadmin
%{pyver_sitelib}/%{pyname}
%{pyver_sitelib}/%{pyname}-%{version}-py%{python2_version}.egg-info
%dir %{_sysconfdir}/%{service}/plugins/vmware
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/vmware/*.ini


%if 0%{?with_doc}
%files doc
%license LICENSE
%doc %{docpath}
%endif

%changelog

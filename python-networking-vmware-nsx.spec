%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global drv_vendor VMware
%global srcname vmware-nsx
%global docpath doc/build/html
%global service neutron
%global pyname vmware_nsx
%global rhosp 0

%global with_doc 1

Name:           python-networking-%{srcname}
Version:        XXX
Release:        XXX
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
# TODO: really, there are no packages on PyPI or anywhere else
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://tarballs.opendev.org/x/%{srcname}/%{srcname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/x/%{srcname}/%{srcname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-tenacity
BuildRequires:  python3-vmware-nsxlib
# Required for config file generation
BuildRequires:  python3-debtcollector
BuildRequires:  python3-oslo-config >= 2:5.1.0
BuildRequires:  python3-oslo-i18n >= 3.15.3
BuildRequires:  python3-oslo-vmware >= 2.17.0
BuildRequires:  python3-neutron
BuildRequires:  openstack-macros

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

%package -n python3-networking-%{srcname}
%{?python_provide:%python_provide python3-networking-%{srcname}}
Summary:        %{drv_vendor} OpenStack Neutron driver
Obsoletes: python2-%{srcname} < %{version}-%{release}

%if 0%{?rhosp} == 0
Requires:       openstack-neutron-vpnaas >= 1:17.0.0.0
%endif
Requires:       openstack-neutron-common >= 1:17.0.0
Requires:       python3-eventlet >= 0.24.1
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-networking-l2gw >= 15.0.0
Requires:       python3-networking-sfc >= 10.0.0.0
Requires:       python3-neutron >= 1:17.0.0
Requires:       python3-neutron-dynamic-routing >= 15.0.0
Requires:       python3-neutron-lib >= 2.6.1
Requires:       python3-openstackclient >= 5.3.0
Requires:       python3-osc-lib >= 2.0.0
Requires:       python3-oslo-concurrency >= 3.26.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-context >= 2.22.0
Requires:       python3-oslo-db >= 4.44.0
Requires:       python3-oslo-i18n >= 3.20.0
Requires:       python3-oslo-log >= 4.3.0
Requires:       python3-oslo-serialization >= 2.28.1
Requires:       python3-oslo-service >= 1.31.0
Requires:       python3-oslo-utils >= 4.4.0
Requires:       python3-oslo-vmware >= 2.17.0
Requires:       python3-paramiko >= 2.4.0
Requires:       python3-pbr >= 4.0.0
Requires:       python3-prettytable >= 0.7.2
Requires:       python3-sqlalchemy >= 1.2.0
Requires:       python3-stevedore >= 2.0.1
Requires:       python3-tenacity >= 6.0.0
Requires:       python3-tooz >= 2.7.1
Requires:       python3-vmware-nsxlib >= 15.0.1
Requires:       python3-ovsdbapp >= 0.10.0
Requires:       python3-octavia-lib >= 1.3.1
Requires:       python3-oslo-policy >= 3.6.0
Requires:       python3-requests >= 2.14.2

Requires:       python3-decorator
Requires:       python3-httplib2 >= 0.9.1

%description -n python3-networking-%{srcname}
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%if 0%{?with_doc}
%package doc
Summary:        %{summary} documentation


%description doc
This package contains documentation for %{drv_vendor} networking driver for
OpenStack Neutron.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%setup -q -n %{srcname}-%{upstream_version}

%py_req_cleanup


%build
%{py3_build}

%if 0%{?with_doc}
sphinx-build-3 -b html doc/source doc/build/html
rm -rf %{docpath}/.buildinfo %{docpath}/.doctrees
%endif


%install
export PBR_VERSION=%{version}
%{py3_install}

# Generate configuration files
PYTHONPATH=.
for file in `ls etc/oslo-config-generator/*`; do
    oslo-config-generator-3 --config-file=$file
done

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware
mv etc/nsx.ini.sample %{buildroot}%{_sysconfdir}/%{service}/plugins/vmware/nsx.ini

%files -n python3-networking-%{srcname}
%license LICENSE
%{_bindir}/nsx-migration
%{_bindir}/neutron-check-nsx-config
%{_bindir}/nsxadmin
%{python3_sitelib}/%{pyname}
%{python3_sitelib}/%{pyname}-%{version}-*.egg-info
%dir %{_sysconfdir}/%{service}/plugins/vmware
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/vmware/*.ini


%if 0%{?with_doc}
%files doc
%license LICENSE
%doc %{docpath}
%endif

%changelog

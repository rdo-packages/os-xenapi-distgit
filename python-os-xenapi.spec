# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library os-xenapi
%global module os_xenapi
# ox-xenapi does not support building docs with sphinx >= 2.0 which is required
# for python3
%if %{pyver} == 3
%global with_doc 0
%else
%global with_doc 1
%endif

%global common_desc XenAPI library for OpenStack projects.

Name:       python-%{library}
Version:    0.3.4
Release:    1%{?dist}
Summary:    XenAPI library for OpenStack projects
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python%{pyver}-%{library}
Summary:    XenAPI client library for OpenStack projects
%{?python_provide:%python_provide python%{pyver}-%{library}}
%if %{pyver} == 3
Obsoletes: python2-%{library} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-babel
BuildRequires:  python%{pyver}-paramiko
# Required for tests
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-eventlet >= 0.18.2

Requires:   python%{pyver}-eventlet >= 0.18.2
Requires:   python%{pyver}-oslo-concurrency >= 3.26.0
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-pbr >= 2.0.0
Requires:   python%{pyver}-babel
Requires:   python%{pyver}-paramiko

%description -n python%{pyver}-%{library}
%{common_desc}

%package -n python%{pyver}-%{library}-tests
Summary:    Tests for XenAPI library for OpenStack projects
Requires:   python%{pyver}-%{library} = %{version}-%{release}
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-os-testr
Requires:   python%{pyver}-testrepository
Requires:   python%{pyver}-testscenarios
Requires:   python%{pyver}-testtools

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the XenAPI library test files.


%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Documentation for XenAPI library for OpenStack projects

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}
# Remove the dom0 bits, we're not supporting them
rm -rf %{buildroot}%{pyver_sitelib}/%{module}/dom0
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s xenapi_bootstrap %{buildroot}%{_bindir}/xenapi_bootstrap-%{pyver}


%check
export PYTHON=%{pyver_bin}

%if %{pyver} == 3
# Skip some tests based on https://github.com/openstack/os-xenapi/blob/master/tox.ini#L21
ostestr --color --slowest --blacklist_file exclusion_py3.txt
%else
%{pyver_bin} setup.py test
%endif

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%{_bindir}/xenapi_bootstrap
%{_bindir}/xenapi_bootstrap-%{pyver}
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 0.3.4-1
- Update to 0.3.4


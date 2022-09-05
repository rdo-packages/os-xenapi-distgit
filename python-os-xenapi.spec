%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library os-xenapi
%global module os_xenapi
# ox-xenapi does not support building docs with sphinx >= 2.0 which is required
# for python3
%global with_doc 0

%global common_desc XenAPI library for OpenStack projects.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    XenAPI library for OpenStack projects
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%package -n python3-%{library}
Summary:    XenAPI client library for OpenStack projects
%{?python_provide:%python_provide python3-%{library}}
Obsoletes: python2-%{library} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-babel
BuildRequires:  python3-paramiko
# Required for tests
BuildRequires:  python3-mock
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslotest
BuildRequires:  python3-os-testr
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-eventlet >= 0.18.2

Requires:   python3-eventlet >= 0.18.2
Requires:   python3-oslo-concurrency >= 3.26.0
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-six >= 1.10.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-babel
Requires:   python3-paramiko

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    Tests for XenAPI library for OpenStack projects
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-oslotest
Requires:   python3-os-testr
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools

%description -n python3-%{library}-tests
%{common_desc}

This package contains the XenAPI library test files.


%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Documentation for XenAPI library for OpenStack projects

BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
python3 setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}
# Remove the dom0 bits, we're not supporting them
rm -rf %{buildroot}%{python3_sitelib}/%{module}/dom0
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s xenapi_bootstrap %{buildroot}%{_bindir}/xenapi_bootstrap-3

%check
export PYTHON=python3

# Skip some tests based on https://github.com/openstack/os-xenapi/blob/master/tox.ini#L21
stestr --test-path os_xenapi/tests run --color --slowest --exclude-list exclusion_py3.txt

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%{_bindir}/xenapi_bootstrap
%{_bindir}/xenapi_bootstrap-3
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog

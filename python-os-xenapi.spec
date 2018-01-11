%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library os-xenapi
%global module os_xenapi

%global common_desc XenAPI library for OpenStack projects.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    XenAPI library for OpenStack projects
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python2-%{library}
Summary:    XenAPI client library for OpenStack projects
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-setuptools
BuildRequires:  python-babel
BuildRequires:  python-paramiko
# Required for tests
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslotest
BuildRequires:  python-os-testr
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-eventlet >= 0.18.2

Requires:   python-eventlet >= 0.18.2
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-six >= 1.9.0
Requires:   python-pbr >= 2.0.0
Requires:   python-babel
Requires:   python-paramiko

%description -n python2-%{library}
%{common_desc}

%package -n python2-%{library}-tests
Summary:    Tests for XenAPI library for OpenStack projects
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python-oslotest
Requires:   python-os-testr
Requires:   python-testrepository
Requires:   python-testscenarios
Requires:   python-testtools

%description -n python2-%{library}-tests
%{common_desc}

This package contains the XenAPI library test files.


%package -n python-%{library}-doc
Summary:    Documentation for XenAPI library for OpenStack projects

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    XenAPI library for OpenStack projects
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-paramiko
# Required for tests
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
Requires:   python3-oslo-concurrency >= 3.8.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-six >= 1.9.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-babel
Requires:   python3-paramiko

%description -n python3-%{library}
%{common_desc}


%package -n python3-%{library}-tests
Summary:    Tests XenAPI library for OpenStack projects
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-oslotest
Requires:   python3-os-testr
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools

%description -n python3-%{library}-tests
%{common_desc}

This package contains the XenAPI library test files.

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
# Remove the dom0 bits, we're not supporting them
rm -rf %{buildroot}%{python2_sitelib}/%{module}/dom0
%if 0%{?with_python3}
%py3_install
# Remove the dom0 bits, we're not supporting them
rm -rf %{buildroot}%{python3_sitelib}/%{module}/dom0
%endif



%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%{python3_sitelib}/%{module}/tests

%endif # with_python3

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/os-xenapi/commit/?id=f88521682e3c9a4a8c3cdff16bf845c1a672cbbe

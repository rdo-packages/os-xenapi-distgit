%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library os-xenapi
%global module os_xenapi

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    XenAPI library for OpenStack projects
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    XenAPI client library for OpenStack projects
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  python-babel
# Required for tests
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslotest
BuildRequires:  python-os-testr
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools

Requires:   python-eventlet >= 0.18.2
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-six >= 1.9.0


%description -n python2-%{library}
XenAPI client library for OpenStack projects.

# NOTE: XenServer still only supports Python 2.4 in its dom0 userspace,
#       so there is no python3 subpackage
%package -n python2-%{library}-plugins
Summary:    Dom0 files for XenAPI support
%{?python_provide:%python_provide python2-%{library}-plugins}

%description -n python2-%{library}-plugins
Dom0 files that are required for XenAPI support for OpenStack.


%package -n python2-%{library}-tests
Summary:    Tests for XenAPI library for OpenStack projects
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
XenAPI library for OpenStack projects.

This package contains the XenAPI library test files.


%package -n python-%{library}-doc
Summary:    Documentation for XenAPI library for OpenStack projects

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
XenAPI library for OpenStack projects.

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    XenAPI library for OpenStack projects
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
# Required for tests
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslotest
BuildRequires:  python3-os-testr
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:   python3-eventlet >= 0.18.2
Requires:   python3-oslo-concurrency >= 3.8.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-six >= 1.9.0

%description -n python3-%{library}
XenAPI library for OpenStack projects.


%package -n python3-%{library}-tests
Summary:    Tests XenAPI library for OpenStack projects
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
XenAPI library for OpenStack projects.

This package contains the XenAPI library test files.

%endif # with_python3


%description
XenAPI library for OpenStack projects.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
mkdir -p %{buildroot}/etc/xapi.d
mv %{buildroot}%{python2_sitelib}/%{module}/dom0/etc/xapi.d/* %{buildroot}%{_sysconfdir}/xapi.d
chmod +x %{buildroot}%{_sysconfdir}/xapi.d/plugins/*
rm -rf %{buildroot}%{python2_sitelib}/%{module}/dom0

%if 0%{?with_python3}
%py3_install
rm -rf %{buildroot}%{python3_sitelib}/%{module}/dom0
%endif



%check
# TODO(jpena): os-xenapi does some evil stuff that does not work in a chroot,
# like opening a socket to /dev/log. This makes tests fail.
%if 0%{?with_python3}
%{__python3} setup.py test || :
rm -rf .testrepository
%endif
%{__python2} setup.py test || :

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-plugins
%license LICENSE
%defattr(-,root,root,-)
%{_sysconfdir}/xapi.d/plugins/*

%files -n python2-%{library}-tests
%license LICENSE
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
%license LICENSE
%{python3_sitelib}/%{module}/tests

%endif # with_python3

%changelog

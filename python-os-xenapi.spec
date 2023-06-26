%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

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
License:    Apache-2.0
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
Obsoletes: python2-%{library} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
python3 setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
# Remove the dom0 bits, we're not supporting them
rm -rf %{buildroot}%{python3_sitelib}/%{module}/dom0
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s xenapi_bootstrap %{buildroot}%{_bindir}/xenapi_bootstrap-3

%check
export PYTHON=python3

# Skip some tests based on https://github.com/openstack/os-xenapi/blob/master/tox.ini#L21
%tox -e %{default_toxenv}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.dist-info
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

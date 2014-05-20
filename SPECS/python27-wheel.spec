# Created by pyp2rpm-1.0.1
%global pypi_name wheel

Name:           python-%{pypi_name}
Version:        0.22.0
Release:        1%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            http://bitbucket.org/dholth/wheel/
Source0:        https://pypi.python.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         wheel-0.22-add-test-files-to-manifest.path
Patch1:         wheel-0.22-legacy-keyring-compatibility.patch
Patch2:         wheel-0.22-fix-tests-broken-by-keyring-fix.patch
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildRequires:  pytest
BuildRequires:  python-jsonschema
BuildRequires:  python-keyring
 

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.


%prep
%setup -q -n %{pypi_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py


%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}


%check
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
rm setup.cfg
py.test --ignore build


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/egg2wheel
%{_bindir}/wheel
%{_bindir}/wininst2wheel
%{python_sitelib}/%{pypi_name}*
%exclude %{python_sitelib}/%{pypi_name}/test


%changelog
* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.

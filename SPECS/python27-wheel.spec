# Created by pyp2rpm-1.0.1
%global pypi_name wheel
%global with_python3 1

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
 
%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3


%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        A built-package format for Python

%description -n python3-%{pypi_name}
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

This is package contains Python 3 version of the package.
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
pushd %{buildroot}%{_bindir}
for f in $(ls); do mv $f python3-$f; done
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}


%check
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
rm setup.cfg
py.test --ignore build
# no test for Python 3, no python3-jsonschema yet
%if 0
pushd %{py3dir}
rm setup.cfg
py.test-%{python3_version} --ignore build
popd
%endif # with_python3


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/egg2wheel
%{_bindir}/wheel
%{_bindir}/wininst2wheel
%{python_sitelib}/%{pypi_name}*
%exclude %{python_sitelib}/%{pypi_name}/test
%if 0%{?with_python3}

%files -n python3-%{pypi_name}
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/python3-egg2wheel
%{_bindir}/python3-wheel
%{_bindir}/python3-wininst2wheel
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/test
%endif # with_python3


%changelog
* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.

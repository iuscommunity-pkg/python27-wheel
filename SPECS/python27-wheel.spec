%global pymajor 2
%global pyminor 7
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}
%global __python2 %{_bindir}/python%{pyver}
%global python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __os_install_post %{__python27_os_install_post}
%global srcname wheel
%global src %(echo %{srcname} | cut -c1)

Name:           python%{iusver}-%{srcname}
Version:        0.30.0
Release:        1.ius%{?dist}
Summary:        A built-package format for Python %{pyver}
Vendor:         IUS Community Project
Group:          Development/Libraries
License:        MIT
URL:            https://bitbucket.org/pypa/%{srcname}
Source0:        https://pypi.io/packages/source/w/wheel/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python%{iusver}-devel
BuildRequires:  python%{iusver}-setuptools
Requires:       python%{iusver}-setuptools
# disable the test suite, for now
#BuildRequires:  pytest
#BuildRequires:  python-jsonschema
#BuildRequires:  python-keyring
 

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.


%prep
%setup -q -n %{srcname}-%{version}
find -name '*.py' -type f -print0 | xargs -0 sed -i '1s|python|&%{pyver}|'


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --optimize 1 --skip-build --root %{buildroot}
%{__mv} %{buildroot}%{_bindir}/wheel{,%{pyver}}


#%check
## remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
#rm setup.cfg
#py.test --ignore build


%files
%license LICENSE.txt
%doc CHANGES.txt
%{_bindir}/wheel%{pyver}
%{python2_sitelib}/%{srcname}*


%changelog
* Wed Sep 13 2017 Ben Harper <ben.harper@rackspace.com> - 0.30.0-1.ius
- Latest upstream
- update URL
- update Source0
- use %license
- remove README.txt and test directory, removed upstream

* Mon Feb 08 2016 Ben Harper <ben.harper@rackspace.com> - 0.29.0-1.ius
- Latest upstream

* Mon Oct 05 2015 Carl George <carl.george@rackspace.com> - 0.26.0-1.ius
- Latest upstream

* Thu Sep 17 2015 Ben Harper <ben.harper@rackspace.com> - 0.25.0-1.ius
- Latest upstream

* Mon Jul 07 2014 Carl George <carl.george@rackspace.com> - 0.24.0-1.ius
- Latest upstream
- Remove egg2wheel and wininst2wheel scripts since they are no longer installed by default

* Fri Jun 06 2014 Carl George <carl.george@rackspace.com> - 0.23.0-2.ius
- Override __os_install_post to fix .pyc/pyo magic

* Wed May 21 2014 Carl George <carl.george@rackspace.com> - 0.23.0-1.ius
- Initial port to IUS
- Remove patches (merged upstream)
- Implement python packaging best practicies
- Disable test suite

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.

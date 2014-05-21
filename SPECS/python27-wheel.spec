%global pymajor 2
%global pyminor 7
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}
%global __python2 %{_bindir}/python%{pyver}
%global python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global srcname wheel
%global src %(echo %{srcname} | cut -c1)

Name:           python%{iusver}-%{srcname}
Version:        0.23.0
Release:        1.ius%{?dist}
Summary:        A built-package format for Python %{pyver}
Vendor:         IUS Community Project
Group:          Development/Libraries
License:        MIT
URL:            https://bitbucket.org/pypa/wheel
Source0:        https://pypi.python.org/packages/source/%{src}/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python%{iusver}-devel
BuildRequires:  python%{iusver}-setuptools
Requires:       python%{iusver}-setuptools
BuildRequires:  pytest
BuildRequires:  python-jsonschema
BuildRequires:  python-keyring
 

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
%{__mv} %{_bindir}/egg2wheel{,%{pyver}}
%{__mv} %{_bindir}/wheel{,%{pyver}}
%{__mv} %{_bindir}/wininst2wheel{,%{pyver}}


%check
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
rm setup.cfg
py.test --ignore build


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/egg2wheel%{pyver}
%{_bindir}/wheel%{pyver}
%{_bindir}/wininst2wheel%{pyver}
%{python2_sitelib}/%{srcname}*
%exclude %{python2_sitelib}/%{srcname}/test


%changelog
* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.

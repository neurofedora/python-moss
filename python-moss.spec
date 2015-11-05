%global modname moss

Name:           python-%{modname}
Version:        0.3.4
Release:        1%{?dist}
Summary:        Assorted utilities for neuroimaging and cognitive science

License:        BSD
URL:            https://github.com/mwaskom/moss
Source0:        https://github.com/mwaskom/moss/archive/v%{version}/%{modname}-%{version}.tar.gz
Patch0:         0001-do-not-check-dependencies-in-runtime.patch
Patch1:         0002-do-not-treat-nipy-as-part-of-moss.patch
BuildRequires:  git-core
BuildArch:      noarch

%description
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written
in as general and lightweight a fashion as possible.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel python2-setuptools
# Test deps
BuildRequires:  python2-nose
BuildRequires:  numpy scipy
%if 0%{?fedora} > 23
BuildRequires:  python2-pandas
%else
BuildRequires:  python-pandas
%endif
BuildRequires:  python2-six
BuildRequires:  python-scikit-learn
BuildRequires:  python-seaborn
BuildRequires:  python-matplotlib
BuildRequires:  python2-nibabel
BuildRequires:  python-statsmodels
BuildRequires:  python2-nipy
Requires:       numpy scipy
%if 0%{?fedora} > 23
Requires:       python2-pandas
%else
Requires:       python-pandas
%endif
Requires:       python2-six
Requires:       python-scikit-learn
Requires:       python-seaborn
Requires:       python-matplotlib
Requires:       python2-nibabel
Requires:       python-statsmodels
Requires:       python2-nipy

%description -n python2-%{modname}
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written
in as general and lightweight a fashion as possible.

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel python3-setuptools
# Test deps
BuildRequires:  python3-nose
BuildRequires:  python3-numpy python3-scipy
BuildRequires:  python3-pandas
BuildRequires:  python3-six
BuildRequires:  python3-scikit-learn
BuildRequires:  python3-seaborn
BuildRequires:  python3-matplotlib
BuildRequires:  python3-nibabel
BuildRequires:  python3-statsmodels
BuildRequires:  python3-nipy
Requires:       python3-numpy python3-scipy
Requires:       python3-pandas
Requires:       python3-six
Requires:       python3-scikit-learn
Requires:       python3-seaborn
Requires:       python3-matplotlib
Requires:       python3-nibabel
Requires:       python3-statsmodels
Requires:       python3-nipy

%description -n python3-%{modname}
Moss is a library of functions, classes, and scripts to that may be useful for
analyzing scientific data. Because this package is developed for neuroimaging
and cognitive science, there is probably some bias towards applications that
are useful in that domain. However, the functions are intended to be written
in as general and lightweight a fashion as possible.

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -S git
# drop bundled nipy
rm -rf moss/nipy/
# Disable one of tests for now due to: https://github.com/mwaskom/moss/issues/17
sed -i -e '/def test_remove_by_group(self):/a \ \ \ \ \ \ \ \ from nose.plugins.skip import SkipTest; raise SkipTest("https://github.com/mwaskom/moss/issues/17")' moss/tests/test_statistical.py

%build
%py2_build
%py3_build

%install
%py3_install
%py2_install

# Rename binaries
pushd %{buildroot}%{_bindir}
  for mod in recon_status recon_movie check_mni_reg recon_process_stats ts_movie
  do
    mv $mod python2-$mod

    sed -i '1s|^.*$|#!/usr/bin/env %{__python2}|' python2-$mod
    for i in $mod $mod-2 $mod-%{python2_version}
    do
      ln -s python2-$mod $i
    done

    cp python2-$mod python3-$mod
    sed -i '1s|^.*$|#!/usr/bin/env %{__python3}|' python3-$mod

    for i in $mod-3 $mod-%{python3_version}
    do
      ln -s python3-$mod $i
    done
  done

  # Depends on 'freeview' utility
  rm -f {recon,warp}_qc
popd

%check
nosetests-%{python2_version} -v
nosetests-%{python3_version} -v

%files -n python2-%{modname}
%license LICENSE
%doc README.md
%{_bindir}/recon_status
%{_bindir}/recon_status-2
%{_bindir}/recon_status-%{python2_version}
%{_bindir}/python2-recon_status
%{_bindir}/recon_movie
%{_bindir}/recon_movie-2
%{_bindir}/recon_movie-%{python2_version}
%{_bindir}/python2-recon_movie
%{_bindir}/check_mni_reg
%{_bindir}/check_mni_reg-2
%{_bindir}/check_mni_reg-%{python2_version}
%{_bindir}/python2-check_mni_reg
%{_bindir}/recon_process_stats
%{_bindir}/recon_process_stats-2
%{_bindir}/recon_process_stats-%{python2_version}
%{_bindir}/python2-recon_process_stats
%{_bindir}/ts_movie
%{_bindir}/ts_movie-2
%{_bindir}/ts_movie-%{python2_version}
%{_bindir}/python2-ts_movie
%{python2_sitelib}/%{modname}*

%files -n python3-%{modname}
%license LICENSE
%doc README.md
%{_bindir}/recon_status-3
%{_bindir}/recon_status-%{python3_version}
%{_bindir}/python3-recon_status
%{_bindir}/recon_movie-3
%{_bindir}/recon_movie-%{python3_version}
%{_bindir}/python3-recon_movie
%{_bindir}/check_mni_reg-3
%{_bindir}/check_mni_reg-%{python3_version}
%{_bindir}/python3-check_mni_reg
%{_bindir}/recon_process_stats-3
%{_bindir}/recon_process_stats-%{python3_version}
%{_bindir}/python3-recon_process_stats
%{_bindir}/ts_movie-3
%{_bindir}/ts_movie-%{python3_version}
%{_bindir}/python3-ts_movie
%{python3_sitelib}/%{modname}*

%changelog
* Thu Nov 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3.4-1
- Initial package

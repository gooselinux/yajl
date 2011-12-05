Name: yajl
Version: 1.0.7
Release: 3%{?dist}
Summary: Yet Another JSON Library (YAJL)

Group: Development/Libraries
License: BSD
URL: http://lloyd.github.com/yajl/

#
# NB, upstream does not provide pre-built tar.gz downloads. Instead
# they make you use the 'on the fly' generated tar.gz from GITHub's
# web interface
#
# The Source0 for any version is obtained by a URL
#
#   http://github.com/lloyd/yajl/tarball/1.0.7
#
# Which causes a download of a archive named after
# the GIT hash corresponding to the version tag
#
#   eg lloyd-yajl-45a1bdb.tar.gz
#
# NB even though the tar.gz is generated on the fly by GITHub it
# will always have identical md5sum
#
# So for new versions, update 'githash' to match the hash of the
# GIT tag associated with updated 'Version:' field just above
%global githash 45a1bdb
Source0: lloyd-%{name}-%{githash}.tar.gz
Patch1: lloyd-%{name}-lib64.patch
Patch2: lloyd-%{name}-cflags.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Requires: %{name} = %{version}-%{release}

%description
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

%description devel
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library

%prep
%setup -q -n lloyd-%{name}-%{githash}
# Fix lib vs lib64 problems
%patch1 -p1
# Fix ignoring of CFLAGS
%patch2 -p1

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
mkdir build
cd build
%cmake ..
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# No static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/libyajl_s.a


%check
cd test
./run_tests.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.1
%{_libdir}/libyajl.so.1.0.7

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{_includedir}/yajl
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_libdir}/libyajl.so


%changelog
* Mon Jan 11 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-3
- Fix ignoring of cflags (rhbz #547500)

* Tue Dec  8 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-2
- Change use of 'define' to 'global'

* Mon Dec  7 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-1
- Initial Fedora package

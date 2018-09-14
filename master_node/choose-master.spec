%global _localdir usr/local/bin/
%global _tmpdir tmp/
%global _unpackaged_files_terminate_build 0

# This is a spec file for gluster-collectd
# The following values are provided by passing the following arguments
# to rpmbuild.  For example:
#         --define "_version 1.0" --define "_release 1"
# we support Python 2 version as of now, Testing has to be done for supporting python 3
# and dependencies has also to be tested.

Name     : choose-master
Version  : 1.0.0
Release  : 1%{?dist}
Summary  : python program to choose ovirt node

License  : GPLv2
URL      : https://github.com/gluster/gluster-collectd/master_node
Source0  : https://github.com/gluster/gluster-collectd/archives/choose-master-%{version}.tar.gz
BuildArch: noarch
Requires : python2
Requires : python-ovirt-engine-sdk4

BuildRequires: python2
BuildRequires: python2-rpm-macros
BuildRequires: python-setuptools
 
%description
The gluster plugin for collectd sends metrics to collectd. 
 
%prep
%setup -q -n choose-master-%{version}
 
%build
%{__python2} setup.py build
 
%install
mkdir -p  %{buildroot}/%{_localdir}
mkdir -p %{buildroot}/%{_tmpdir}
cp -rp ./build/lib/choose-master/*.py  %{buildroot}/%{_localdir}
cp -rp ./build/lib/choose-master/choose-master.service %{buildroot}/%{_tmpdir}
# Man Pages

%files
%defattr(-,root,root)
/%{_localdir}/choose_master.py
/%{_tmpdir}/choose-master.service
%exclude /%{_localdir}/*.pyo
%exclude /%{_localdir}/*.pyc

%changelog
* Wed Sep 5 2018 Venkata R Edara <redara@redhat.com> 1.0.0-0
- Initial version of gluster collectd plugin 1.0.0-0

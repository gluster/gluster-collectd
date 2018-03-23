%global _confdir %{_sysconfdir}/collectd.d
%global _collectdir usr/lib64/collectd/gluster-collectd
%global _unpackaged_files_terminate_build 0

# This is a spec file for gluster-collectd
# The following values are provided by passing the following arguments
# to rpmbuild.  For example:
#         --define "_version 1.0" --define "_release 1"
#

%{!?_version:%global _version __PKG_VERSION__}
%{!?_release:%global _release __PKG_RELEASE__}

Name     : gluster-collectd
Version  : %{_version}
Release  : %{_release}%{?dist}
Summary  : Red Hat Gluster Collectd Plugin

License  : GPLv2
URL      : https://github.com/gluster/gluster-collectd
Source0  : gluster-collectd-%{_version}-%{_release}.tar.gz
BuildArch: noarch
Requires : python2
Requires : collectd >= 5.8.0
Requires : collectd-python >= 5.8.0

BuildRequires: python2
BuildRequires: python-setuptools
 
%description
The gluster plugin for collectd sends metrics to collectd. 
 
%prep
%setup -q -n gluster-collectd-%{_version}
 
%build
%{__python2} setup.py build
 
%install
mkdir -p      %{buildroot}/%{_confdir}/
mkdir -p      %{buildroot}/usr/share/collectd/
mkdir -p      %{buildroot}/%{_collectdir}
cp -r conf/* %{buildroot}/%{_confdir}/
cp -r types/* %{buildroot}/usr/share/collectd/
cp -r ./build/lib/src/*  %{buildroot}/%{_collectdir}/

# Man Pages
install -d -m 755 %{buildroot}%{_mandir}/man8
install -p -m 0644 README.md %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root)
%{_mandir}/man8/*
/usr/share/collectd/types.db.gluster
/%{_collectdir}/gluster_plugins/*.py
/%{_collectdir}/gluster_plugins/*.pyc
/%{_collectdir}/gluster_plugins/*.pyo
/%{_collectdir}/*.py
/%{_collectdir}/*.pyc
/%{_collectdir}/*.pyo

%dir %{_confdir}
%dir /%{_collectdir}
%dir /%{_collectdir}/gluster_plugins
%config(noreplace) %{_confdir}/gluster.conf

%changelog
* Wed Jan 31 2018 Venkata R Edara <redara@redhat.com> 1.0.0-0
- Initial version of gluster collectd plugin 1.0.0-0

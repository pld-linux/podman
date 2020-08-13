Summary:	A tool for managing OCI containers and pods
Name:		podman
Version:	2.0.4
Release:	1
License:	Apache v2.0
Group:		Applications/System
#Source0Download: https://github.com/containers/podman/releases
Source0:	https://github.com/containers/podman/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6a84e3ef54559fd3796848aafb8f7a36
URL:		https://github.com/containers/podman
BuildRequires:	go-md2man
BuildRequires:	golang
BuildRequires:	golang-varlink
Requires:	conmon
Requires:	crun
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Podman (the POD MANager) is a tool for managing containers and images,
volumes mounted into those containers, and pods made from groups of
containers. Podman is based on libpod, a library for container
lifecycle management that is also contained in this repository. The
libpod library provides APIs for managing containers, pods, container
images, and volumes.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	BINDIR=%{_bindir} \
	LIBEXECDIR=%{_libexecdir} \
	SYSTEMDDIR=%{systemdunitdir} \
	USERSYSTEMDDIR=%{systemduserunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md changelog.txt
%attr(755,root,root) %{_bindir}/podman
%attr(755,root,root) %{_bindir}/podman-remote
%{systemdunitdir}/podman.service
%{systemdunitdir}/podman.socket
%{systemduserunitdir}/podman.service
%{systemduserunitdir}/podman.socket
%{_mandir}/man1/podman*.1*
%{_mandir}/man5/containers-mounts.conf.5*
%{_mandir}/man5/oci-hooks.5*

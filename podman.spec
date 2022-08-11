Summary:	A tool for managing OCI containers and pods
Name:		podman
Version:	4.2.0
Release:	1
License:	Apache v2.0
Group:		Applications/System
#Source0Download: https://github.com/containers/podman/releases
Source0:	https://github.com/containers/podman/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d4261e2b46342aaf0df285410064955c
Source1:	policy.json
Source2:	registries.conf
URL:		https://github.com/containers/podman
BuildRequires:	device-mapper-devel
BuildRequires:	go-md2man
BuildRequires:	golang
BuildRequires:	golang-varlink
BuildRequires:	gpgme-devel
BuildRequires:	libseccomp-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	systemd-devel
Requires:	conmon
Requires:	containernetworking-plugins
Requires:	crun
Suggests:	slirp4netns
Suggests:	uidmap
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0

%description
Podman (the POD MANager) is a tool for managing containers and images,
volumes mounted into those containers, and pods made from groups of
containers. Podman is based on libpod, a library for container
lifecycle management that is also contained in this repository. The
libpod library provides APIs for managing containers, pods, container
images, and volumes.

%package -n bash-completion-podman
Summary:	bash-completion for podman
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-podman
This package provides bash-completion for podman.

%package -n fish-completion-podman
Summary:	Fish completion for podman command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-podman
Fish completion for podman command.

%package -n zsh-completion-podman
Summary:	Zsh completion for podman command
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-podman
Zsh completion for podman command.

%prep
%setup -q

%build
%{__make} \
	GO=/usr/bin/go \
	GOCMD="CGO_ENABLED=1 %__go" \
	GOPATH=$(pwd)/.gopath \
	PREFIX="%{_prefix}" \
	BINDIR="%{_bindir}" \
	LIBEXECDIR="%{_libexecdir}" \
	MANDIR="%{_mandir}" \
	SHAREDIR_CONTAINERS="%{_datadir}/containers" \
	ETCDIR="%{_sysconfdir}" \
	TMPFILESDIR="%{systemdtmpfilesdir}" \
	SYSTEMDDIR="%{systemdunitdir}" \
	USERSYSTEMDDIR="%{systemduserunitdir}" \
	PYTHON="%{__python3}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/containers,%{bash_compdir},%{fish_compdir},%{zsh_compdir},%{_sharedstatedir}/containers}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	BINDIR="%{_bindir}" \
	LIBEXECDIR="%{_libexecdir}" \
	MANDIR="%{_mandir}" \
	SHAREDIR_CONTAINERS="%{_datadir}/containers" \
	ETCDIR="%{_sysconfdir}" \
	TMPFILESDIR="%{systemdtmpfilesdir}" \
	SYSTEMDDIR="%{systemdunitdir}" \
	USERSYSTEMDDIR="%{systemduserunitdir}" \
	PYTHON="%{__python3}"

cp -p %{SOURCE1} %{SOURCE2} \
	vendor/github.com/containers/common/pkg/config/containers.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/containers

%{__sed} -e 's|/var/lib/containers|%{_sharedstatedir}/containers|g' \
	vendor/github.com/containers/storage/storage.conf \
        > $RPM_BUILD_ROOT%{_sysconfdir}/containers/storage.conf

$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{bash_compdir}/podman bash
$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{fish_compdir}/podman.fish fish
$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{zsh_compdir}/_podman zsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post podman.service podman.socket

%preun
%systemd_preun podman.service podman.socket

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_sysconfdir}/containers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/containers.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/policy.json
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/storage.conf
%attr(755,root,root) %{_bindir}/podman
%attr(755,root,root) %{_bindir}/podman-remote
%dir %{_libexecdir}/podman
%attr(755,root,root) %{_libexecdir}/podman/rootlessport
%{systemdunitdir}/podman.service
%{systemdunitdir}/podman.socket
%{systemdunitdir}/podman-auto-update.service
%{systemdunitdir}/podman-auto-update.timer
%{systemdunitdir}/podman-kube@.service
%{systemdunitdir}/podman-restart.service
%{systemduserunitdir}/podman.service
%{systemduserunitdir}/podman.socket
%{systemduserunitdir}/podman-auto-update.service
%{systemduserunitdir}/podman-auto-update.timer
%{systemduserunitdir}/podman-kube@.service
%{systemduserunitdir}/podman-restart.service
%{_mandir}/man1/podman*.1*
/usr/lib/tmpfiles.d/podman.conf
%dir %{_sharedstatedir}/containers

%files -n bash-completion-podman
%defattr(644,root,root,755)
%{bash_compdir}/podman

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/podman.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_podman

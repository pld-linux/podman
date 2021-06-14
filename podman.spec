Summary:	A tool for managing OCI containers and pods
Name:		podman
Version:	3.2.1
Release:	1
License:	Apache v2.0
Group:		Applications/System
#Source0Download: https://github.com/containers/podman/releases
Source0:	https://github.com/containers/podman/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8bea2ae7cab3efbc8cc564c9ece91077
Source1:	policy.json
Source2:	registries.conf
Patch0:		%{name}-seccomp_32bit.patch
URL:		https://github.com/containers/podman
BuildRequires:	device-mapper-devel
BuildRequires:	go-md2man
BuildRequires:	golang
BuildRequires:	golang-varlink
BuildRequires:	gpgme-devel
BuildRequires:	libseccomp-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	systemd-devel
Requires:	conmon
Requires:	containernetworking-plugins
Requires:	crun
Suggests:	slirp4netns
Suggests:	uidmap
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
cd vendor/github.com/containers/common
%patch0 -p1

%build
%{__make} \
	GO=/usr/bin/go \
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

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/containers,%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

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

cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/containers

$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{bash_compdir}/podman bash
$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{fish_compdir}/podman.fish fish
$RPM_BUILD_ROOT%{_bindir}/podman completion -f $RPM_BUILD_ROOT%{zsh_compdir}/_podman zsh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md changelog.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cni/net.d/87-podman-bridge.conflist
%dir %{_sysconfdir}/containers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/policy.json
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/containers/registries.conf
%attr(755,root,root) %{_bindir}/podman
%attr(755,root,root) %{_bindir}/podman-remote
%{systemdunitdir}/podman.service
%{systemdunitdir}/podman.socket
%{systemdunitdir}/podman-auto-update.service
%{systemdunitdir}/podman-auto-update.timer
%{systemduserunitdir}/podman.service
%{systemduserunitdir}/podman.socket
%{systemduserunitdir}/podman-auto-update.service
%{systemduserunitdir}/podman-auto-update.timer
%{_mandir}/man1/podman*.1*
%{_mandir}/man5/containers-mounts.conf.5*
%{_mandir}/man5/oci-hooks.5*
/usr/lib/tmpfiles.d/podman.conf

%files -n bash-completion-podman
%defattr(644,root,root,755)
%{bash_compdir}/podman

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/podman.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_podman

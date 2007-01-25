#
# Conditional build:
%bcond_without	startup		# build without resource database initiallization
%bcond_without	udev		# build with hotplug instead of udev
#
Summary:	PCMCIA initialization utils for Linux kernels >= 2.6.13
Summary(pl):	Narzêdzia startowe pcmcia dla j±der Linuksa >= 2.6.13
Name:		pcmciautils
Version:	014
Release:	1.5
License:	GPL v2
Group:		Base
Source0:	http://kernel.org/pub/linux/utils/kernel/pcmcia/%{name}-%{version}.tar.bz2
# Source0-md5:	3f07c926875f6c5dcb83240f39725177
URL:		http://kernel.org/pub/linux/utils/kernel/pcmcia/pcmcia.html
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	sed >= 4.0
BuildRequires:	sysfsutils-devel >= 1.3.0
Requires:	module-init-tools >= 3.2-0.pre4.1
%{!?with_udev:Requires:	hotplug}
%{?with_udev:Requires:	udev}
#if kernel used >= 2.6.13
#Obsoletes:	pcmcia-cs
#else
#BuildRequires:	useless
#endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PCMCIA initialization utils to be used with Linux kernels >= 2.6.13.
They are designed for new PCMCIA subsystem and are replacement for old
pcmcia-cs package.

%description -l pl
Narzêdzia startowe pcmcia dla j±der Linuksa >= 2.6.13. Zosta³y
stworzone dla nowego podsystemu PCMCIA i zastêpuj± stary pakiet
pcmcia-cs.

%prep
%setup -q

%build
%if !%{with startup}
sed -i -e "s#STARTUP =.*#STARTUP = false#g" Makefile
%endif
%if !%{with udev}
sed -i -e "s#UDEV =.*#UDEV = false#g" Makefile
%endif

%{__make} \
	KERNEL_DIR=/usr \
	YACC="bison -y" \
	CC="%{__cc}" \
	OPTIMIZATION="%{rpmcflags}" \
	STRIPCMD=true

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if %{with startup}
%dir %{_sysconfdir}/pcmcia
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/config.opts
%endif
%if %{with udev}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/60-pcmcia.rules
%else
%{_sysconfdir}/hotplug/*
%endif
%attr(755,root,root) /sbin/pccardctl
%attr(755,root,root) /sbin/pcmcia-check-broken-cis
%attr(755,root,root) /sbin/lspcmcia
%if %{with startup}
%attr(755,root,root) /sbin/pcmcia-socket-startup
%endif
%{_mandir}/*/*

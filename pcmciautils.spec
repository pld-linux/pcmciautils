#
# Conditional build:
%bcond_without	startup		# build without resource database initiallization
%bcond_without	udev		# build with hotplug instead of udev
#
Summary:	PCMCIA initialization utils for Linux kernels >= 2.6.13
Summary(pl.UTF-8):	Narzędzia startowe pcmcia dla jąder Linuksa >= 2.6.13
Name:		pcmciautils
Version:	018
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://kernel.org/pub/linux/utils/kernel/pcmcia/%{name}-%{version}.tar.bz2
# Source0-md5:	5d85669b3440baa4532363da6caaf1b4
URL:		http://kernel.org/pub/linux/utils/kernel/pcmcia/pcmcia.html
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	sed >= 4.0
BuildRequires:	sysfsutils-devel >= 1.3.0
Requires:	module-init-tools >= 3.2-0.pre4.1
%{!?with_udev:Requires:	hotplug}
%{?with_udev:Requires:	udev}
Requires:	uname(release) >= 2.6.13
Obsoletes:	pcmcia-cs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PCMCIA initialization utils to be used with Linux kernels >= 2.6.13.
They are designed for new PCMCIA subsystem and are replacement for old
pcmcia-cs package.

%description -l pl.UTF-8
Narzędzia startowe pcmcia dla jąder Linuksa >= 2.6.13. Zostały
stworzone dla nowego podsystemu PCMCIA i zastępują stary pakiet
pcmcia-cs.

%prep
%setup -q

%build
%if %{without startup}
sed -i -e "s#STARTUP =.*#STARTUP = false#g" Makefile
%endif
%if %{without udev}
sed -i -e "s#UDEV =.*#UDEV = false#g" Makefile
%endif

%{__make} -j1 \
	KERNEL_DIR=/usr \
	YACC="bison -y" \
	CC="%{__cc}" \
	OPTIMIZATION="%{rpmcflags}" \
	STRIPCMD=true

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/lspcmcia.8
echo '.so pccardctl.8' >$RPM_BUILD_ROOT%{_mandir}/man8/lspcmcia.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if %{with startup}
%dir %{_sysconfdir}/pcmcia
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/config.opts
%endif
%if %{with udev}
%attr(755,root,root) /lib/udev/pcmcia-check-broken-cis
%if %{with startup}
%attr(755,root,root) /lib/udev/pcmcia-socket-startup
%endif
/lib/udev/rules.d/60-pcmcia.rules
%else
%attr(755,root,root) %{_sysconfdir}/hotplug/pcmcia.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/pcmcia.rc
%if %{with startup}
%attr(755,root,root) %{_sysconfdir}/hotplug/pcmcia_socket.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/pcmcia_socket.rc
%endif
%endif
%attr(755,root,root) /sbin/lspcmcia
%attr(755,root,root) /sbin/pccardctl
%{_mandir}/man8/lspcmcia.8*
%{_mandir}/man8/pccardctl.8*

Summary:	A server process which provides boot information to diskless clients
Summary(pl):	Demon który zapewnia informacje potrzebne do uruchomienia bezdyskowych klientów
Name:		bootparamd
Version:	0.17
Release:	8
License:	BSD
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-install_man_fix.patch
Prereq:		rc-scripts
Requires:	/sbin/chkconfig
Requires:	portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The bootparamd process provides bootparamd, a server process which
provides the information needed by diskless clients in order for them
to successfully boot. Bootparamd looks first in /etc/bootparams for an
entry for that particular client; if a local bootparams file doesn't
exist, it looks at the appropriate Network Information Service (NIS)
map. Some network boot loaders (notably Sun's) rely on special boot
server code on the server, in addition to the rarp and tftp servers.
This bootparamd server process is compatible with SunOS bootparam
clients and servers which need that boot server code.

%prep
%setup -q -n netkit-bootparamd-%{version}
%patch -p1

%build
./configure --with-c-compiler=%{__cc}
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bootparamd

%clean
rm -rf $RPM_BUILD_ROOT

%post
DESC="rpc.bootparamd server"; %chkconfig_post

%postun
%chkconfig_postun

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/bootparamd
%attr(755,root,root) %{_sbindir}/rpc.bootparamd
%attr(755,root,root) %{_bindir}/callbootd
%{_mandir}/man[58]/*

Summary:	A server process which provides boot information to diskless clients
Name:		bootparamd
Version:	0.17
Release:	0
License:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	bootparamd.init
Prereq:		/sbin/chkconfig
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

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bootparamd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bootparamd
if [ -f /var/lock/subsys/rpc.bootparamd ]; then
	/etc/rc.d/init.d/bootparamd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/bootparamd start\" to start rpc.bootparamd server" 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rpc.bootparamd ]; then
		/etc/rc.d/init.d/bootparamd stop 1>&2
	fi
	/sbin/chkconfig --del bootparamd
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/bootparamd
%attr(755,root,root) %{_sbindir}/rpc.bootparamd
%attr(755,root,root) %{_bindir}/callbootd
%{_mandir}/man8/*

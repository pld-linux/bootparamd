Summary:	A server process which provides boot information to diskless clients
Summary(pl.UTF-8):	Demon zapewniający informacje potrzebne do uruchomienia bezdyskowych klientów
Name:		bootparamd
Version:	0.17
Release:	13
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	00d211115b11aec2e214b701fe72f397
Source1:	%{name}.init
Patch0:		%{name}-install_man_fix.patch
BuildRequires:	cpp
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	portmap
Requires:	rc-scripts
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

%description -l pl.UTF-8
Pakiet zawiera program bootparamd - demon, który zapewnia informacje
potrzebne dla uruchomienia bezdyskowych klientów. bootparamd szuka w
/etc/bootparams wpisu dla konkretnego klienta; jeżeli plik ten nie
istnieje, szuka odpowiedniej mapy NIS. Niektóre sieciowe bootloadery
(np. Suna) polegają na specjalnym kodzie bootującym na serwerze. Ten
bootparamd jest kompatybilny z klientami bootparam na SunOS-ie i
serwerami potrzebującymi tego kodu.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch0 -p1

%build
./configure \
	--with-c-compiler="%{__cc}"
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpc.bootparamd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rpc.bootparamd
%service rpc.bootparamd restart "rpc.bootparamd server"

%preun
if [ "$1" = "0" ]; then
	%service rpc.bootparamd stop
	/sbin/chkconfig --del rpc.bootparamd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(754,root,root) /etc/rc.d/init.d/rpc.bootparamd
%attr(755,root,root) %{_sbindir}/rpc.bootparamd
%attr(755,root,root) %{_bindir}/callbootd
%{_mandir}/man[58]/*

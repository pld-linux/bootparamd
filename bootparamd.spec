Summary: A server process which provides boot information to diskless clients.
Name: bootparamd
Version: 0.10
Release: 22
Copyright: BSD
Group: System Environment/Daemons
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-bootparamd-0.10.tar.gz
Source1: bootparamd.init
Patch: netkit-bootparamd-0.10-misc.patch
Prereq: /sbin/chkconfig
Requires: portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The bootparamd process provides bootparamd, a server process which
provides the information needed by diskless clients in order for them
to successfully boot.  Bootparamd looks first in /etc/bootparams for an
entry for that particular client; if a local bootparams file doesn't
exist, it looks at the appropriate Network Information Service (NIS)
map.  Some network boot loaders (notably Sun's) rely on special boot
server code on the server, in addition to the rarp and tftp servers.
This bootparamd server process is compatible with SunOS bootparam clients
and servers which need that boot server code.

You should install bootparamd if you need to provide boot information to
diskless clients on your network.

%prep
%setup -q -n netkit-bootparamd-0.10
%patch -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
make INSTALLROOT=$RPM_BUILD_ROOT install
install -m 755 $RPM_SOURCE_DIR/bootparamd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/bootparamd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bootparamd

%postun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del bootparamd
fi

%files
/usr/sbin/rpc.bootparamd
/usr/bin/callbootd
/usr/man/man8/rpc.bootparamd.8
/usr/man/man8/bootparamd.8
%attr(754,root,root) /etc/rc.d/init.d/bootparamd

Summary:     Logcheck system log analyzer
Name:        logcheck
Version:     1.1
Release:     1d
Copyright:   Free. See LICENSE file.
Group:       Utilities/System
Source:      http://www.psionic.com/abacus/%{name}-%{version}.tar.gz
Patch:       %{name}-pld.patch
Vendor:      Craig Rowland <crowland@psionic.com>
URL:         http://www.psionic.com/abacus
BuildRoot:   /tmp/%{name}-%{version}-%{release}-root
Summary(pl): Logcheck - analizator logów systemu

%description
Logcheck is software package that is designed to automatically run and check
system log files for security violations and unusual activity. Logcheck
utilizes a program called logtail that remembers the last position it read
from in a log file and uses this position on subsequent runs to process new
information. All source code is available for review and the implementation
was kept simple to avoid problems. This package is a clone of the
frequentcheck.sh script from the Trusted Information Systems Gauntlet(tm)
firewall package. TIS has granted permission for me to clone this package.

%description -l pl
Pakiet zawiera logcheck - aplikacjê przeznaczon± do automatycznego analizowania
logów systemowych i przesy³aniu ich po wstêpnjej obróbce poczt± elektroniczn± 
do administratora systemu. Aplikacja ta jest klonem skryptu frequentcheck.sh z
Trusted Information Systems Gauntlet(tm). 

%prep
%setup -q
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/logcheck
install -d $RPM_BUILD_ROOT/usr/sbin

make CC="gcc" CFLAGS="$RPM_OPT_FLAGS" linux

install -d $RPM_BUILD_ROOT/etc/cron.hourly

cat <<EOF > $RPM_BUILD_ROOT/etc/cron.hourly/logcheck
#!/bin/bash
/usr/sbin/logcheck
EOF

strip $RPM_BUILD_ROOT/usr/sbin/logtail

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES CREDITS README* systems/linux/README*

%attr(700,root,root) %dir /etc/logcheck
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logcheck/*
%attr(700,root,root) %config(missingok) /etc/cron.hourly/logcheck
%attr(700,root,root) /usr/sbin/logcheck
%attr(700,root,root) /usr/sbin/logtail

%changelog

* Sat Sep 12 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
[1.1-1d]
- build against glibc-2.1,
- translation modified for pl,
- added %defattr support,
- minor spec's modifications.

* Sun Jul 13 1998 Peter Soos <sp@osb.hu>

- Some modification in handling of tmp files
- Corrected the permission of document directory

* Wed Jul 1 1998 Peter Soos <sp@osb.hu>

- Initial package

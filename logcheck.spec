Summary:	Logcheck system log analyzer
Summary(pl):	Logcheck - analizator logów systemu
Name:		logcheck
Version:	1.1
Release:	2
Copyright:	Free. See LICENSE file.
Group:		Utilities/System
Source:		http://www.psionic.com/abacus/%{name}-%{version}.tar.gz
Patch:		%{name}-pld.patch
Vendor:		Craig Rowland <crowland@psionic.com>
URL:		http://www.psionic.com/abacus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

install -d $RPM_BUILD_ROOT{/etc/logcheck,%{_sbindir}}

make CC="gcc" CFLAGS="$RPM_OPT_FLAGS" linux

install -d $RPM_BUILD_ROOT/etc/cron.hourly

cat <<EOF > $RPM_BUILD_ROOT/etc/cron.hourly/logcheck
#!/bin/sh
exec %{_sbindir}/logcheck
EOF

strip --strip-unneeded $RPM_BUILD_ROOT%{_sbindir}/logtail

gzip -9nf CHANGES CREDITS README* systems/linux/README*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,CREDITS,README*,systems/linux/README*}.gz
%attr(700,root,root) %dir /etc/logcheck
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logcheck/*
%attr(700,root,root) %config(missingok) /etc/cron.hourly/logcheck
%attr(700,root,root) %{_sbindir}/logcheck
%attr(700,root,root) %{_sbindir}/logtail

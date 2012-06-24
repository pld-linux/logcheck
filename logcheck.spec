Summary:	Logcheck system log analyzer
Summary(pl):	Logcheck - analizator log�w systemu
Name:		logcheck
Version:	1.1.1
Release:	1
License:	Free. See LICENSE file.
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://www.psionic.com/tools/%{name}-%{version}.tar.gz
Patch0:		%{name}-pld.patch
Vendor:		Craig Rowland <crowland@psionic.com>
URL:		http://www.psionic.com/abacus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/logcheck

%description
Logcheck is software package that is designed to automatically run and
check system log files for security violations and unusual activity.
Logcheck utilizes a program called logtail that remembers the last
position it read from in a log file and uses this position on
subsequent runs to process new information. All source code is
available for review and the implementation was kept simple to avoid
problems. This package is a clone of the frequentcheck.sh script from
the Trusted Information Systems Gauntlet(tm) firewall package. TIS has
granted permission for me to clone this package.

%description -l pl
Pakiet zawiera logcheck - aplikacj� przeznaczon� do automatycznego
analizowania log�w systemowych i przesy�aniu ich po wst�pnjej obr�bce
poczt� elektroniczn� do administratora systemu. Aplikacja ta jest
klonem skryptu frequentcheck.sh z Trusted Information Systems
Gauntlet(tm).

%prep
%setup -q
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.hourly,%{_sbindir}}

%{__make} linux \
	CC=%{__cc} \
	CFLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS}"

cat <<EOF > $RPM_BUILD_ROOT/etc/cron.hourly/logcheck
#!/bin/sh
exec %{_sbindir}/logcheck
EOF

gzip -9nf CHANGES CREDITS README* systems/linux/README*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz systems/linux/*.gz
%attr(700,root,root) %dir %{_sysconfdir}
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(700,root,root) %config(missingok) /etc/cron.hourly/logcheck
%attr(755,root,root) %{_sbindir}/logcheck
%attr(755,root,root) %{_sbindir}/logtail

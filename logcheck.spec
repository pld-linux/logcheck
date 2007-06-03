Summary:	Mails anomalies in the system logfiles to the administrator
Summary(pl.UTF-8):	Wysyłanie anomalii w logach systemowych pocztą do administratora
Name:		logcheck
Version:	1.2.56
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/l/logcheck/%{name}_%{version}.tar.gz
# Source0-md5:	8fb0066cd0f984622dd47fae55201603
Patch0:		%{name}-pld.patch
Patch1:		%{name}-command_correct.patch
Source1:	%{name}.cron
URL:		http://logcheck.alioth.debian.org/
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-database = %{version}-%{release}
Requires:	/bin/mail
Requires:	crondaemon
Requires:	lockfile-progs
Requires:	logtail = %{version}-%{release}
Requires:	mktemp
#Suggests:	/usr/bin/syslog-summary
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/logcheck

%description
Logcheck is a simple utility which is designed to allow a system
administrator to view the logfiles which are produced upon hosts under
their control.

It does this by mailing summaries of the logfiles to them, after first
filtering out "normal" entries.

Normal entries are entries which match one of the many included
regular expression files contain in the database.

Logcheck was part of the Abacus Project of security tools, but this
version has been rewritten.

%description -l pl.UTF-8
logcheck to proste narzędzie zaprojektowane aby umożliwić
administratorowi systemu oglądanie plików logów tworzonych przez
maszyny, które ma pod kontrolą.

Wykonuje to poprzez wysyłanie pocztą elektroniczną do administratora
podsumowań plików logów po odfiltrowaniu "zwykłych" wpisów.

Zwykłe wpisy to wpisy pasujące do jednego z wielu załączonych plików
wyrażeń regularnych zawartych w bazie danych.

logcheck był częścią projektu Abacus z narzędziami związanymi z 
bezpieczeństwem, ale ta wersja została przepisana.

%package database
Summary:	Database of system log rules for the use of log checkers
Summary(pl.UTF-8):	Baza danych reguł loga systemowego do używania z narzędziami sprawdzającymi logi
Group:		Applications/System

%description database
This database is part of the Logcheck package, but might be used by
others. It brings a database of regular expressions for matching
system log entries after various criteria.

%description database -l pl.UTF-8
Ta baza danych jest częścią pakietu logcheck, ale może być używana
przez inne programy. Zawiera wyrażenia regularne do dopasowywania
wpisów logów systemowych z użyciem różnych kryteriów.

%package -n logtail
Summary:	Print log file lines that have not been read
Summary(pl.UTF-8):	Wypisywanie nieprzeczytanych linii pliku loga
Group:		Applications/System

%description -n logtail
This program will read in a standard text file and create an offset
marker when it reads the end. The offset marker is read the next time
logtail is run and the text file pointer is moved to the offset
location. This allows logtail to read in the next lines of data
following the marker. This is good for marking log files for automatic
log file checkers to monitor system events.

This program is mainly used by logcheck, because it returns only parts
of the system logfiles that have not already been checked.

%description -n logtail -l pl.UTF-8
Ten program czyta standardowy plik tekstowy, a po doczytaniu do końca
tworzy znacznik offsetu. Przy następnym uruchomieniu logtaila
odczytywany jest znacznik offsetu i wskaźnik tekstu jest przesuwany do
tego offsetu. Pozwala to logtailowi czytać kolejne linie danych za
znacznikiem. Jest to dobre narzędzie do oznaczania plików logów dla
narzędzi do automatycznego sprawdzania plików logów i monitorowania
zdarzeń systemowych.

Ten program jest używany głównie przez logcheck, ponieważ zwraca tylko
te części plików logów systemowych, które nie zostały jeszcze
przeczytane.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,%{_sbindir},%{_bindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

mv $RPM_BUILD_ROOT{%{_sbindir},%{_bindir}}/logtail

cat <<'EOF'> $RPM_BUILD_ROOT%{_sysconfdir}/header.txt
This email is sent by logcheck. If you wish to no-longer receive it,
you can either deinstall the logcheck package or modify its
configuration file (%{_sysconfdir}/logcheck.conf).
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 173 %{name}
%useradd -u 173 -d /var/lib/%{name} -g logcheck -c "Logcheck User" %{name}

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES CREDITS TODO
%doc docs/README.{how.to.interpret,keywords,logcheck,Maintainer} docs/tools/log-summary-ssh
%attr(710,root,logcheck) %dir %{_sysconfdir}
%dir %attr(2750,root,logcheck) %{_sysconfdir}/cracking.d
%dir %attr(2750,root,logcheck) %{_sysconfdir}/cracking.ignore.d
%dir %attr(2750,root,logcheck) %{_sysconfdir}/violations.d
%dir %attr(2750,root,logcheck) %{_sysconfdir}/violations.ignore.d
%dir %attr(2750,root,logcheck) %{_sysconfdir}/ignore.d.workstation
%dir %attr(2750,root,logcheck) %{_sysconfdir}/ignore.d.server
%dir %attr(2750,root,logcheck) %{_sysconfdir}/ignore.d.paranoid
%attr(640,root,logcheck) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/logcheck.conf
%attr(640,root,logcheck) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/logcheck.logfiles
%attr(640,root,logcheck) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/header.txt
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_sbindir}/logcheck
%dir %attr(770,root,logcheck) /var/lib/logcheck
%dir %attr(770,root,logcheck) /var/lock/logcheck

%files database
%defattr(644,root,root,755)
%config %verify(not md5 mtime size) %{_sysconfdir}/cracking.d/*
%config %verify(not md5 mtime size) %{_sysconfdir}/violations.d/*
%config %verify(not md5 mtime size) %{_sysconfdir}/violations.ignore.d/*
%config %verify(not md5 mtime size) %{_sysconfdir}/ignore.d.workstation/*
%config %verify(not md5 mtime size) %{_sysconfdir}/ignore.d.server/*
%config %verify(not md5 mtime size) %{_sysconfdir}/ignore.d.paranoid/*

%files -n logtail
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/logtail

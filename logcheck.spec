Summary:	Mails anomalies in the system logfiles to the administrator
Summary(pl):	Wysy³anie anomalii w logach systemowych poczt± do administratora
Name:		logcheck
Version:	1.2.47
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/l/logcheck/%{name}_%{version}.tar.gz
# Source0-md5:	bc26d3ebe3c4f65813299e829cd01c81
Patch0:		%{name}-pld.patch
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

%description -l pl
logcheck to proste narzêdzie zaprojektowane aby umo¿liwiæ
administratorowi systemu ogl±danie plików logów tworzonych przez
maszyny, które ma pod kontrol±.

Wykonuje to poprzez wysy³anie poczt± elektroniczn± do administratora
podsumowañ plików logów po odfiltrowaniu "zwyk³ych" wpisów.

Zwyk³e wpisy to wpisy pasuj±ce do jednego z wielu za³±czonych plików
wyra¿eñ regularnych zawartych w bazie danych.

logcheck by³ czê¶ci± projektu Abacus z narzêdziami zwi±zanymi z 
bezpieczeñstwem, ale ta wersja zosta³a przepisana.

%package database
Summary:	Database of system log rules for the use of log checkers
Summary(pl):	Baza danych regu³ loga systemowego do u¿ywania z narzêdziami sprawdzaj±cymi logi
Group:		Applications/System

%description database
This database is part of the Logcheck package, but might be used by
others. It brings a database of regular expressions for matching
system log entries after various criteria.

%description database -l pl
Ta baza danych jest czê¶ci± pakietu logcheck, ale mo¿e byæ u¿ywana
przez inne programy. Zawiera wyra¿enia regularne do dopasowywania
wpisów logów systemowych z u¿yciem ró¿nych kryteriów.

%package -n logtail
Summary:	Print log file lines that have not been read
Summary(pl):	Wypisywanie nieprzeczytanych linii pliku loga
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

%description -n logtail -l pl
Ten program czyta standardowy plik tekstowy, a po doczytaniu do koñca
tworzy znacznik offsetu. Przy nastêpnym uruchomieniu logtaila
odczytywany jest znacznik offsetu i wska¼nik tekstu jest przesuwany do
tego offsetu. Pozwala to logtailowi czytaæ kolejne linie danych za
znacznikiem. Jest to dobre narzêdzie do oznaczania plików logów dla
narzêdzi do automatycznego sprawdzania plików logów i monitorowania
zdarzeñ systemowych.

Ten program jest u¿ywany g³ównie przez logcheck, poniewa¿ zwraca tylko
te czê¶ci plików logów systemowych, które nie zosta³y jeszcze
przeczytane.

%prep
%setup -q
%patch0 -p1

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

# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Apr/1009838.html
# - put logtail to bin instead of sbin?
Summary:	Logcheck system log analyzer
Summary(es):	Analizador de logs
Summary(pl):	Logcheck - analizator logСw systemu
Summary(pt_BR):	Um analisador de logs
Summary(ru):	Logcheck - анализатор log-файлов
Summary(uk):	Logcheck - анал╕затор log-файл╕в
Summary(zh_CN):	о╣мЁхуж╬╥жнЖ╧╓╬ъ
Name:		logcheck
Version:	1.1.1
Release:	3.1
License:	GPL
Group:		Applications/System
#Source0:	http://www.psionic.com/tools/%{name}-%{version}.tar.gz
# Adopted by Debian ? They have 1.3.14 in pool
# Debian has 1.2.32 now.
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	e97c2f096e219e20310c1b80e9e1bc29
Patch0:		%{name}-pld.patch
Vendor:		Craig H. Rowland <crowland@psionic.com>
#URL:		http://www.psionic.com/abacus
Requires:	/usr/sbin/sendmail
Requires:	crondaemon
Requires:	logtail = %{epoch}:%{version}-%{release}
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

%description -l es
Analizador de logs

%description -l pl
Pakiet zawiera logcheck - aplikacjЙ przeznaczon╠ do automatycznego
analizowania logСw systemowych i przesyЁaniu ich po wstЙpnej obrСbce
poczt╠ elektroniczn╠ do administratora systemu. Aplikacja ta jest
klonem skryptu frequentcheck.sh z Trusted Information Systems
Gauntlet(tm).

%description -l pt_BR
O logcheck И um software que foi desenvolvido para automaticamente
rodar e checar logs do sistema para violaГУes de seguranГa, e
atividade nЦo usual.

%description -l ru
Logcheck - программа для отслеживания в системных логах необычных
действий и попыток несанкционированного доступа.

%description -l uk
Logcheck - програма для в╕дсл╕дковування в системних логах незвичайних
д╕й та спроб несанкц╕онованого доступу.

%package -n logtail
Summary:	logtail program from logcheck package
Group:		Applications/System

%description -n logtail
This package contains logtail that remembers the last position it read
from in a log file and uses this position on subsequent runs to
process new information.

%prep
%setup -q
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.hourly,%{_sbindir}}

%{__make} linux \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

cat <<EOF > $RPM_BUILD_ROOT/etc/cron.hourly/logcheck
#!/bin/sh
exec %{_sbindir}/logcheck
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES CREDITS README* systems/linux/README*
%attr(700,root,root) %dir %{_sysconfdir}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(700,root,root) %config(missingok) /etc/cron.hourly/logcheck
%attr(755,root,root) %{_sbindir}/logcheck

%files -n logtail
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/logtail

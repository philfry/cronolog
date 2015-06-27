%define gitrepo http://github.com/philfry/%{name}.git
%define gitrev %{version}

%global _hardened_build 1

Name: cronolog
Version: 1.6.3
Release: 1%{?dist}
Summary: a flexible log file rotation program for Apache
Group: System Environment/Daemons
License: GPL
URL: https://github.com/philfry/%{name}
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info


%description
cronolog is a simple filter program that reads log file entries from
standard input and writes each entry to the output file specified
by a filename template and the current date and time. When the
expanded filename changes, the current file is closed and a new one
opened. cronolog is intended to be used in conjunction with a Web server,
such as Apache, to split the access log into daily or monthly logs.


%prep
%setup -q


%build
%configure
make %{_smp_mflags}


%install
[ '%{buildroot}' != '/' ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
sed -i 's|/www/sbin|/usr/sbin|g' %{buildroot}/%{_mandir}/man1/*
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}/%{_sbindir}/cronosplit %{buildroot}/%{_bindir}
rm -f %{buildroot}%{_infodir}/dir


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%preun
/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :


%clean
[ '%{buildroot}' != '/' ] && rm -rf %{buildroot}


%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_sbindir}/cronolog
%{_bindir}/cronosplit
%{_mandir}/man1/cronolog.1*
%{_mandir}/man1/cronosplit.1*
%{_infodir}/cronolog.info*


%changelog
* Sat Jun 27 2015 Philippe Kueck <projects@unixadm.org> - 1.6.3-1
- bump to 1.6.3 which is basically 1.6.2 with all patches included

* Thu Jul  7 2011 Philippe Kueck <projects@unixadm.org> - 1.6.2-99
- initial packaging

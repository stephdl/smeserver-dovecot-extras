%define version 0.1.1
%define release 1
%define name smeserver-dovecot-extras


Summary: Additional features for dovecot on SME Server
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArchitectures: noarch
BuildRequires: e-smith-devtools

Requires: smeserver-dovecot
Requires: dovecot-pigeonhole
Requires: acl

%description
Add IMAP acl (sharedmailbox) and sieve capabilities to the IMAP server

%changelog
* Mon Jun 23 2014 Daniel Berteaud <daniel@firewall-services.com> - 0.1.1-1
- Add midding /home/e-smith/db/dovecot dir
- Remove submission_host for sieve

* Tue Oct 29 2013 Daniel Berteaud <daniel@firewall-services.com> - 0.0.2-1
- Use SMTP for sieve notifications

* Tue Nov 29 2011 Daniel Berteaud <daniel@firewall-services.com> - 0.0.1-1
- initial release

%prep
%setup -q -n %{name}-%{version}

%build
perl createlinks
mkdir -p root/home/e-smith/db/dovecot

%install
/bin/rm -rf $RPM_BUILD_ROOT
(cd root   ; /usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)
/bin/rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
   --dir /home/e-smith/db/dovecot 'attr(2770,root,sharedmailbox)' \
   --file /home/e-smith/db/dovecot/sharedmailbox.db 'attr(0660,root,sharedmailbox) %config(noreplace)' \
   --file /usr/bin/imap-postlogin 'attr(0755,root,root)' \
  > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g 439 sharedmailbox 2> /dev/null || :

%post
# Migrate the sharedmailbox dict to its new location
if [ -e /etc/dovecot/sharedmailbox/dict.db ]; then
    mv -f /etc/dovecot/sharedmailbox/dict.db /home/e-smith/db/dovecot/sharedmailbox.db
    rm -rf /etc/dovecot/sharedmailbox
fi

%preun


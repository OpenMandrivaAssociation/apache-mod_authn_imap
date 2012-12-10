#Module-Specific definitions
%define mod_name mod_authn_imap
%define mod_conf B42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for basic IMAP authentication support
Name:		apache-%{mod_name}
Version:	0.01
Release: 	7
Group:		System/Servers
License:	Apache License
URL:		http://www.s5h.net/code/mod-imap/
Source0:	http://www.s5h.net/code/mod-imap/mod_imap-%{version}.tar.gz
Source1:	http://www.s5h.net/code/mod-imap/mod_imap-%{version}.tar.gz.asc
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0

%description
Apache module for basic IMAP authentication support.

%prep

%setup -q -n mod_imap

cp %{SOURCE2} %{mod_conf}

# change the modules name
cp mod_authn_imap_basic.c %{mod_name}.c

%build
%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

# cleanup
rm -f %{buildroot}%{_libdir}/apache-extramodules/*.*a

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc README INSTALL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.01-7mdv2012.0
+ Revision: 772565
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.01-6
+ Revision: 678275
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.01-5mdv2011.0
+ Revision: 587933
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.01-4mdv2010.1
+ Revision: 516062
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.01-3mdv2010.0
+ Revision: 406537
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.01-2mdv2009.1
+ Revision: 325570
- rebuild

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.01-1mdv2009.0
+ Revision: 238141
- fix the config
- import apache-mod_authn_imap


* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.01-1
- initial Mandriva package

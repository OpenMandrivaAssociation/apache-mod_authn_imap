#Module-Specific definitions
%define mod_name mod_authn_imap
%define mod_conf B42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for basic IMAP authentication support
Name:		apache-%{mod_name}
Version:	0.01
Release: 	%mkrel 6
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Apache module for basic IMAP authentication support.

%prep

%setup -q -n mod_imap

cp %{SOURCE2} %{mod_conf}

# change the modules name
cp mod_authn_imap_basic.c %{mod_name}.c

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README INSTALL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


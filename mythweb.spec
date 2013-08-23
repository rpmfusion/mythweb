%global gitrev v0.26.0-220-g92dbb43

Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/
Group:          Applications/Multimedia

Version:        0.26.1
Release:        1%{?dist}

License:        GPLv2 and LGPLv2 and MIT

# https://github.com/MythTV/mythweb/tarball/v0.25
Source0:        %{name}-%{version}.tar.gz
Source1:        mythweb.conf
Source2:        ChangeLog

# Patch generated from mythweb fixes branch. From mythweb git directory:
# git diff -p --stat %{version} > mythweb-fixes.patch
Patch0:         mythweb-0.26-fixes.patch
Patch1:         mythweb-notrans.patch
Patch2:         mythweb-phperror.patch

# The following are required only in mythweb is running on the same computer
# as the backend. They will be pulled in by the mythtv meta package anyway.
#Requires:       mythtv-backend >= %{version}-%{release}
#Requires:       mysql-server >= 5, mysql >= 5

Requires:       httpd
Requires:       php >= 5.1
Requires:       php-mysql
Requires:       php-process
Requires:       php-MythTV >= %{version}
Requires:       mythffmpeg

BuildArch:      noarch


%description
The web interface to MythTV.


%prep
%setup -q
#patch0 -p1
%patch1 -p1
%patch2 -p1

# Fix directory permissions
#find ./ -type d -exec chmod 0755 {} \;

# Non-executable scripts don't need shebangs
sed -i modules/coverart/handler.pl -e '/\/usr\/bin\/perl/d'

# Install ChangeLog
install -m 0644 %{SOURCE2} .


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/mythweb/{image_cache,php_sessions}
cp -a * %{buildroot}%{_datadir}/mythweb/
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/

# Remove stuff covered by %%doc
rm %{buildroot}%{_datadir}/mythweb/{LICENSE,README,INSTALL,ChangeLog}


%files
%doc README LICENSE ChangeLog
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%defattr(-,apache,apache,0755)
%{_datadir}/mythweb/


%changelog
* Fri Aug 23 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.1-1
- Update to latest upstream version.

* Mon Aug 13 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-5
- Update to latest fixes.
- Patch for NoTrans issue with php in Fedora 19 and up. (Fixes #2856)

* Fri Jan 11 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-3
- Update mythweb config to work with apache 2.4.

* Sat Dec 08 2012 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-2
- Update to latest upstream release.

* Sun Oct 28 2012 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-1
- Update to latest upstream release.

* Mon Jul 30 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.2-1
- Update to latests release.

* Fri Jul 06 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-3
- Patch for PHP 5.4 warnings.

* Sun Jul 01 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-2
- Lots of tweaks per review request:
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=2366

* Tue Jun 05 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-1
- Initial package split of mythweb from mythtv.

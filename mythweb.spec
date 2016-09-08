%global vers_string v0.28-8-ga1f2cdf

Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/

Version:        0.28
Release:        2%{?dist}

License:        GPLv2 and LGPLv2 and MIT

Source0:        https://github.com/MythTV/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        mythweb.conf
Source2:        ChangeLog

# Patch generated from mythweb fixes branch. From mythweb git directory:
# git diff -p --stat %{version} > mythweb-fixes.patch
Patch0:         mythweb-0.28-fixes.patch

# The following are required only in mythweb is running on the same computer
# as the backend. They will be pulled in by the mythtv meta package anyway.
#Requires:       mythtv-backend >= %{version}-%{release}
#Requires:       mysql-server >= 5, mysql >= 5

Requires:       httpd
Requires:       php >= 5.1
Requires:       php-mysqli
Requires:       php-process
Requires:       php-MythTV >= %{version}
Requires:       mythffmpeg

BuildArch:      noarch


%description
The web interface to MythTV.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

# Non-executable scripts don't need shebangs
sed -i modules/coverart/handler.pl -e '/\/usr\/bin\/perl/d'

# Install ChangeLog
install -m 0644 %{SOURCE2} .


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/mythweb/{image_cache,php_sessions}
cp -a * %{buildroot}%{_datadir}/mythweb/

# data dir needs to be a directory suitable for writing
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/data %{buildroot}%{_sharedstatedir}/%{name}/
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/data \
       %{buildroot}%{_datadir}/%{name}

# Install httpd config
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/

# Remove stuff covered by %%doc
rm %{buildroot}%{_datadir}/mythweb/{LICENSE,README,INSTALL,ChangeLog}


%pretrans
# If this is an upgrade
if [ $1 -eq 0 ] ; then
    # If data exists and is a directory then we need move it out of the way.
    if [ -d "%{_datadir}/%{name}/data" ] ; then
        mv %{_datadir}/%{name}/data %{_datadir}/%{name}/_tmp_data
    fi
fi

%posttrans
# If this is an upgrade
if [ $1 -eq 0 ] ; then
    # If there is data to migrate, let's do it
    if [ -e "%{_datadir}/%{name}/_tmp_data" ] ; then
        cp -p %{_datadir}/%{name}/_tmp_data/cache/* \
              %{_sharedstatedir}/%{name}/data/cache/ &> /dev/null || :
        cp -p %{_datadir}/%{name}/_tmp_data/tv_icons/* \
              %{_sharedstatedir}/%{name}/data/tv_icons/ &> /dev/null || :
        rm -rf %{_datadir}/%{name}/_tmp_data
    fi
fi


%files
%doc README ChangeLog
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%{_datadir}/%{name}/
%defattr(-,apache,apache,0755)
%{_sharedstatedir}/%{name}/


%changelog
* Thu Sep 08 2016 Sérgio Basto <sergio@serjux.com> - 0.28-2
- v0.28-rc1 already support mysqli, https://code.mythtv.org/trac/ticket/12588
  Requires php-mysqli, because in php7, "php-mysql" package and "mysql.so"
  extension have been removed.

* Tue May  3 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-2
- Update to latest fixes.

* Tue Apr 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-1
- Update to latest fixes.

* Fri Feb 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.6-2
- Update to latest fixes.

* Wed Jul 29 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.5-1
- Update to latest upstream release.

* Wed May 27 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-2
- Update to latest fixes release.

* Thu Oct 23 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-1
- Update to latest upstream release.

* Sun Jul 27 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.3-1
- Update to latest upstream release.

* Mon May 26 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.1-1
- Update to latest upstream release.

* Fri May 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27-2
- Update to latest fixes release.

* Mon Oct 28 2013 Richard Shaw <hobbes1069@gmail.com> - 0.27-1
- Update to 0.27 at latest fixes release.
- Make mythweb write to a more appropriate directory.

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.26.1-3
- Rebuilt

* Mon Sep  2 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.1-2
- Update to latest upstream release.

* Fri Aug 23 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.1-1
- Update to latest upstream version.

* Tue Aug 13 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-5
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

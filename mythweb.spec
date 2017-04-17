%global vers_string v0.28.1-1-gd94cf0b

Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/

Version:        0.28.1
Release:        1%{?dist}

License:        GPLv2 and LGPLv2 and MIT

Source0:        https://github.com/MythTV/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        mythweb.conf
Source2:        ChangeLog

# Patch generated from mythweb fixes branch. From mythweb git directory:
# git diff -p --stat <git_tag> > mythweb-fixes.patch
Patch0:         mythweb-0.28-fixes.patch

# This is needed for perl dependency auto-detection
BuildRequires:  perl-generators

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


#%pretrans
## If this is an upgrade
#if [ $1 -eq 0 ] ; then
#    # If data exists and is a directory then we need move it out of the way.
#    if [ -d "%{_datadir}/%{name}/data" ] ; then
#        mv %{_datadir}/%{name}/data %{_datadir}/%{name}/_tmp_data
#    fi
#fi

#%posttrans
## If this is an upgrade
#if [ $1 -eq 0 ] ; then
#    # If there is data to migrate, let's do it
#    if [ -e "%{_datadir}/%{name}/_tmp_data" ] ; then
#        cp -p %{_datadir}/%{name}/_tmp_data/cache/* \
#              %{_sharedstatedir}/%{name}/data/cache/ &> /dev/null || :
#        cp -p %{_datadir}/%{name}/_tmp_data/tv_icons/* \
#              %{_sharedstatedir}/%{name}/data/tv_icons/ &> /dev/null || :
#        rm -rf %{_datadir}/%{name}/_tmp_data
#    fi
#fi


%files
%doc README ChangeLog
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%{_datadir}/%{name}/
%attr(-,apache,apache) %{_sharedstatedir}/%{name}/


%changelog
* Mon Apr 17 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-1
- Update to latest upstream release, 0.28.1.

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-6
- Remove obsolete scripts. Since data was moved to /var/lib data migration is
  no longer necessary.
- Fixes RFBZ#4357.

* Wed Oct 26 2016 Paul Howarth <paul@city-fan.org> - 0.28-5
- BR: perl-generators for proper dependency generation
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)

* Wed Oct 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-4
- Update to latest fixes.

* Thu Sep 08 2016 Sérgio Basto <sergio@serjux.com> - 0.28-2
- v0.28-rc1 already support mysqli, https://code.mythtv.org/trac/ticket/12588
- Requires php-mysqli, because in php7, "php-mysql" package and "mysql.so"
- extension have been removed.

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

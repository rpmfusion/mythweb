# Mythweb from github.com
# git hash for archive
%global githash1 g89a347c
# git hash for root source directory
%global githash2 ae20c88

Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/
Group:          Applications/Multimedia

Version:        0.25.1
Release:        2%{?dist}

License:        GPLv2 and LGPLv2 and MIT

# https://github.com/MythTV/mythweb/tarball/v0.25
Source0:        MythTV-mythweb-v%{version}-0-%{githash1}.tar.gz
Source1:        mythweb.conf
Source2:        ChangeLog

# Patch generated from mythweb fixes branch. From mythweb git directory:
# git diff -p --stat %{version} > mythweb-fixes.patch
Patch1:         mythweb-fixes.patch

# The following are required only in mythweb is running on the same computer
# as the backend. They will be pulled in by the mythtv meta package anyway.
#Requires:       mythtv-backend >= %{version}-%{release}
#Requires:       mysql-server >= 5, mysql >= 5

Requires:       httpd
Requires:       php >= 5.1
Requires:       php-mysql
Requires:       php-process
Requires:       php-MythTV >= %{version}

BuildArch:      noarch


%description
The web interface to MythTV.


%prep
%setup -q -n MythTV-mythweb-%{githash2}
#patch1 -p1 -b .mythweb

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
# drop .htaccess file, settings handled in the above
rm -f %{buildroot}%{_datadir}/mythweb/data/.htaccess


%files
%doc README LICENSE ChangeLog
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%{_datadir}/mythweb/


%changelog
* Sun Jul 01 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-2
- Lots of tweaks per review request:
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=2366

* Tue Jun 05 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-1
- Initial package split of mythweb from mythtv.

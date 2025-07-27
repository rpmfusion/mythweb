Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/

Version:        34.0
Release:        4%{?dist}

License:        GPLv2 and LGPLv2 and MIT

Source0:        https://github.com/MythTV/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        mythweb.conf
Source2:        ChangeLog

# This is needed for perl dependency auto-detection
BuildRequires:  perl-generators

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
%autosetup -p1

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

%files
%doc README ChangeLog
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%{_datadir}/%{name}/
%attr(-,apache,apache) %{_sharedstatedir}/%{name}/

%changelog
* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 34.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 01 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 34.0-1
- 34.0 release

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 33.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Feb 26 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-1
- Update to 33.1

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Fri Jun 03 2022 Richard Shaw <hobbes1069@gmail.com> - 32.0-2
- Update to v32.0-40-gb05906a6.

* Thu May 12 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-1
- Update to 32.0

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 31.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Richard Shaw <hobbes1069@gmail.com> - 31.0-5
- Add patch for PHP8 from upstream.

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-1
- Update to 31.0.

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 30.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Feb 27 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-1
- Update to 30.0.

* Sun Sep 23 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-4
- Addresses PHP 7.2 issue, fixes #4937.

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 29.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 15 2018 Sérgio Basto <sergio@serjux.com> - 29.1-1
- Update to 29.1

* Sun Sep 17 2017 Richard Shaw <hobbes1069@gmail.com> - 29.0-1
- Update to latest upstream release, 29.0.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.28.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-2
- Rebuild for perl 5.26.0.

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

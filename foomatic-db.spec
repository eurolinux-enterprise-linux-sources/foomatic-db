%define dbver_rel 4.0
%define dbver_snap 20091126

Summary: Database of printers and printer drivers
Name: foomatic-db
Version: %{dbver_rel}
Release: 7.%{dbver_snap}%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-ppds = %{version}-%{release}

Source0: http://www.openprinting.org/download/foomatic/foomatic-db-%{dbver_rel}-%{dbver_snap}.tar.gz

Url: http://www.openprinting.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# The foomatic oki8w driver works for printers that this old package
# use to drive:
Obsoletes: oki4linux < 2.1gst-5
# Note: no "Provides:" as it was not a dependency of any package.

%description
This is the database of printers, printer drivers, and driver options
for Foomatic.

The site http://www.openprinting.org/ is based on this database.

%package filesystem
Summary: Directory layout for the foomatic package
License: Public Domain
Group: System Environment/Base

%description filesystem

Directory layout for the foomatic package.

%package ppds
Summary: PPDs from printer manufacturers
License: GPLv2+ and MIT
Group: System Environment/Libraries
# We ship a symlink in a directory owned by cups
BuildRequires: cups
Requires: cups
Requires: sed
Requires: %{name}-filesystem = %{version}-%{release}

%description ppds
PPDs from printer manufacturers.

%prep
%setup -q -n %{name}-%{dbver_snap}

find -type d | xargs chmod g-s

cd db/source

# For gutenprint printers, use gutenprint-ijs-simplified.5.2.
perl -pi -e 's,>gutenprint<,>gutenprint-ijs-simplified.5.2<,' printer/*.xml

# Remove references to foo2zjs, foo2oak, foo2hp and foo2qpdl (bug #208851).
# Also foo2lava, foo2kyo, foo2xqx (bug #438319).
# Also foo2slx and foo2hiperc (bug #518267).
for x in zjs oak hp qpdl lava kyo xqx slx hiperc
do
  find printer -name '*.xml' |xargs grep -l "<driver>foo2${x}"|xargs rm -vf
  rm -f driver/foo2${x}.xml opt/foo2${x}-*
done
# Same for m2300w/m2400w
find printer -name '*.xml' |xargs grep -l '<driver>m2[34]00w<'|xargs rm -vf
rm -f driver/m2300w.xml driver/m2400w.xml opt/m2300w-*
# Same for all these.
for x in drv_x125 ml85p pbm2lwxl pbmtozjs bjc800j
do
  find printer -name '*.xml' |xargs grep -l "<driver>${x}</driver>"|xargs rm -vf
  rm -vf driver/${x}.xml opt/${x}-*
done

# Use sed instead of perl in the PPDs (bug #512739).
find PPD -type f -name '*.ppd' | xargs perl -pi -e 's,perl -p,sed,'

%build
%configure
make PREFIX=%{_prefix}


%install
rm -rf $RPM_BUILD_ROOT

make	DESTDIR=%buildroot PREFIX=%{_prefix} \
	install

# Remove ghostscript UPP drivers that are gone in 7.07
rm -f %{buildroot}%{_datadir}/foomatic/db/source/driver/{bjc6000a1,PM760p,PM820p,s400a1,sharp,Stc670pl,Stc670p,Stc680p,Stc760p,Stc777p,Stp720p,Stp870p}.upp.xml

find %{buildroot}%{_datadir}/foomatic/db/source/ -type f | xargs chmod 0644

mkdir %{buildroot}%{_datadir}/foomatic/db/source/PPD/Custom

rm -f	%{buildroot}%{_datadir}/foomatic/db/source/PPD/Kyocera/*.htm \
	%{buildroot}%{_datadir}/cups/model/3-distribution

# Convert absolute symlink to relative.
rm -f %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds
ln -sf ../../foomatic/db/source/PPD %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds

%clean
rm -rf %{buildroot}

%files filesystem
%defattr(-,root,root,-)
%dir %{_datadir}/foomatic
%dir %{_datadir}/foomatic/db
%dir %{_datadir}/foomatic/db/source

%files
%defattr(-,root,root,-)
%doc db/source/PPD/Kyocera/*.htm
%doc README
%doc COPYING
%{_datadir}/foomatic/db/oldprinterids
%{_datadir}/foomatic/db/source/printer
%{_datadir}/foomatic/db/source/driver
%{_datadir}/foomatic/db/source/opt

%files ppds
%defattr(-,root,root,-)
%{_datadir}/foomatic/db/source/PPD
%{_datadir}/cups/model/foomatic-db-ppds

%changelog
* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 4.0-7.20091126
- Updated to foomatic-db-4.0-20091126 (bug #538994).

* Thu Aug 20 2009 Tim Waugh <twaugh@redhat.com> 4.0-6.20090819
- Removed references to foo2slx and foo2hiperc (bug #518267).

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 4.0-5.20090819
- Updated to foomatic-db-4.0-20090819.
- Removed deprecated foomatic-db-hpijs tarball.
- Use buildroot macro throughout.

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 4.0-4.20090702
- Use stcolor driver for Epson Stylus Color 200 (bug #513676).

* Mon Aug 17 2009 Tim Waugh <twaugh@redhat.com> 4.0-3.20090702
- License for ppds sub-package should include GPLv2+.
- Ship COPYING file in main package.
- Added filesystem sub-package for directory ownership.

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 4.0-2.20090702
- Move foomatic-db-ppds symlink to ppds sub-package.
- Use sed instead of perl in raster PPDs (bug #512739).
- Removed code to convert old-style printer IDs (there are none).
- Ship README file.

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 4.0-1.20090702
- Split database out from main foomatic package.

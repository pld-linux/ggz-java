#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
#
%include	/usr/lib/rpm/macros.java
Summary:	Java core client for the GGZ Gaming Zone
Summary(pl.UTF-8):	Klient GGZ Gaming Zone w Javie
Name:		ggz-java
Version:	0.0.14.1
Release:	1
License:	LGPL v2.1+
Group:		Applications/Games
Source0:	http://mirrors.dotsrc.org/ggzgamingzone/ggz/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df1c433df4d310cb9ee90a7091bf2cf1
URL:		http://www.ggzgamingzone.org/
BuildRequires:	ant
BuildRequires:	jdk >= 1.4
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GGZ Java client is a port of the following C libraries:
- libggz
- ggz-client-libs 
- ggz-gtk-client (redeveloped from scratch)
- ggz-gtk-games/ggzcards (redeveloped from scratch)

%description -l pl.UTF-8
Klient GGZ w Javie to port następujących bibliotek C:
- libggz
- ggz-client-libs
- ggz-gtk-client (utworzony od podstaw)
- ggz-gtk-games/ggzcards (utworzony od podstaw)

%package javadoc
Summary:	GGZ Java client API documentation
Summary(pl.UTF-8):	Dokumentacja API klienta GGZ w Javie
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
GGZ Java client API documentation.

%description javadoc -l pl.UTF-8
Dokumentacja API klienta GGZ w Javie.

%prep
%setup -q

%build
export JAVA_HOME="%{java_home}"

%ant jar %{?with_javadoc:javadoc} \
	-Dsvnant.unspec=true

# see Makefile
cp -p ggz-java-unspec.jar ggz-java-client.jar

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}
cp -a javadoc $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.GGZ README.txt TODO.txt
%attr(755,root,root) %{_bindir}/ggz-java
%dir %{_datadir}/ggz/ggz-java
%{_datadir}/ggz/ggz-java/ggz-java-unspec.jar
%{_mandir}/man6/ggz-java.6*

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif

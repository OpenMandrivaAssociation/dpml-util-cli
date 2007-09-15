%define short_name      cli
%define category        util
%define section         free
%define gcj_support     1

Name:           dpml-%{category}-%{short_name}
Version:        1.0.0
Release:        %mkrel 3
Epoch:          0
Summary:        DPML Metro Common Utilities
License:        Apache License
Group:          Development/Java
URL:            http://dpml.net/util/cli/index.html
# svn checkout https://svn.berlios.de/svnroot/repos/dpml/trunk/main
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-build.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  ant >= 0:1.6
#BuildRequires: ant-junit >= 0:1.6
#BuildRequires: junit
BuildRequires:  jpackage-utils >= 0:1.5

%description
The CLI index provides an API for processing command line interfaces.

The implementation is based on the Jakarta Commons CLI2 library written 
by John Keyes and Rob Oxspring.

CLI1 was formed by the merger of ideas and code from three different 
libraries and allows most simple interfaces to be modelled. CLI1 became 
increasingly difficult to maintain and develop further and so CLI2 was 
developed with the goals of clearer responsibilities and being more 
flexible. The intention was that CLI2 would be able to model a far 
greater selection of interfaces and do so more completely, validating 
as much as possible.

The DPML codebase was established in late 2005 based on a fork of the 
Jarkata Commons CL2 content as CLI2 development with Jakarta Commons 
appears to have stopped around April 2005. Modification to the codebase 
applied during incorporation under DPML include removal of CLI1 
content, resolution of a number of testcase failures, removal of file 
validation hidden feature (due to platform inconsitencies at the JVM 
level), removal of Maven dependencies in the build and test procedures, 
resolution of issues in the Help formatter, package renaming, 
documentation enhancements, upgrading of the codebase to be compliant 
with DPML style guidelines, and additions to the argument validator 
package.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}
%{__cp} -a %{SOURCE1} build.xml

%build
#export OPT_JAR_LIST="ant/ant-junit junit"
export OPT_JAR_LIST=
export CLASSPATH=
%ant jar javadoc #test

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}



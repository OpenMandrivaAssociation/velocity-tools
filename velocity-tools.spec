# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0
# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section		free

Name:           velocity-tools
Version:        1.4
Release:        %mkrel 2.0.1
Epoch:          0
Summary:        Velocity application building tools
License:        Apache Software License
URL:            http://velocity.apache.org/tools
Group:          Development/Java
Source0:         http://www.apache.org/dist/velocity/tools/%{version}/%{name}-%{version}-src.tar.gz
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Source3:        sslext-1.2-0.jar
Source4:        %{name}-site.xml

Patch0:		velocity-tools-1.3-download_xml.patch
Patch1:		velocity-tools-pom_xml.patch
BuildRequires:  ant
BuildRequires:  jakarta-commons-beanutils >= 0:1.7.0
BuildRequires:  jakarta-commons-collections >= 0:3.2
BuildRequires:  jakarta-commons-digester >= 0:1.7
BuildRequires:  jakarta-commons-lang >= 0:2.2
BuildRequires:  jakarta-commons-logging >= 0:1.1
BuildRequires:  jakarta-commons-validator >= 0:1.1.4
BuildRequires:  dom4j
BuildRequires:	jaxen >= 0:1.1
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  java-rpmbuild
BuildRequires:  servletapi5
BuildRequires:	struts >= 0:1.2.7
# FIXME
#BuildRequires:	struts-sslext >= 0:1.2
BuildRequires:	velocity >= 0:1.4
BuildRequires:	velocity-dvsl
BuildRequires:	oro >= 0:2.0.8
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven-surefire-plugin
BuildRequires:  mojo-maven2-plugin-taglist
BuildRequires:  maven2-default-skin
%endif

Requires:  jakarta-commons-beanutils
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-digester
Requires:  jakarta-commons-lang
Requires:  jakarta-commons-logging
Requires:  jakarta-commons-validator
Requires:  dom4j
Requires:  jaxen >= 0:1.1
Requires:  jpackage-utils >= 0:1.7.2
Requires:  servletapi5
Requires:  struts >= 0:1.2.7
Requires:  velocity
Requires:  velocity-dvsl
Requires:  oro
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
VelocityTools is a collection of Velocity subprojects with a common
goal of creating tools and infrastructure for building both web and
non-web applications using the Velocity template engine.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
Documentation for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}-%{version}-src
# Remove all binary libs used in compiling the package.
#FIXME Use struts-sslext package
find lib -name "*.jar" -and -not -name sslext-1.2.jar -print | xargs rm -f
#%patch0 -b .sav
#%patch1 -b .sav
cp %{SOURCE1} settings.xml
mkdir -p src/site
cp %{SOURCE4} src/site/site.xml
#TODO remove when struts is updated
sed -i -e "s|String varValue =|String varValue = \"\";|g" src/java/org/apache/velocity/tools/struts/ValidatorTool.java
sed -i -e "s|Resources.getVarValue(var, app, request, false);|//Resources.getVarValue(var, app, request, false);|g" src/java/org/apache/velocity/tools/struts/ValidatorTool.java

# dropping this tool: requires sslext
#rm src/java/org/apache/velocity/tools/struts/SecureLinkTool.java
# dropping this tool: needs struts 1.3
#rm src/java/org/apache/velocity/tools/struts/ValidatorTool.java

%if %{with_maven}
mkdir -p .m2/repository/JPP/
cp %{SOURCE3} .m2/repository/JPP/sslext.jar
%else

mkdir -p lib
(cd lib
cp %{SOURCE3} .
ln -sf $(build-classpath commons-beanutils)
ln -sf $(build-classpath commons-collections)
ln -sf $(build-classpath commons-digester)
ln -sf $(build-classpath commons-lang)
ln -sf $(build-classpath commons-logging)
ln -sf $(build-classpath commons-validator)
ln -sf $(build-classpath dom4j)
ln -sf $(build-classpath jaxen)
ln -sf $(build-classpath oro)
ln -sf $(build-classpath servletapi5)
ln -sf $(build-classpath struts)
ln -sf $(build-classpath velocity)
ln -sf $(build-classpath velocity-dvsl)
)
#commons-beanutils-1.7.0.jar
#commons-collections-3.2.jar
#commons-digester-1.8.jar
#commons-lang-2.2.jar
#commons-logging-1.1.jar
#commons-validator-1.3.1.jar
#dom4j-1.1.jar
#oro-2.0.8.jar
#servletapi-2.3.jar
#sslext-1.2-0.jar
#struts-core-1.3.5.jar
#struts-taglib-1.3.5.jar
#struts-tiles-1.3.5.jar
#velocity-1.4.jar
#velocity-dvsl-0.43.jar
%endif

%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc site
%else
%ant -Dskip.jar.loading=true jar.struts jar.view jar.generic javadoc docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%if ! %{with_maven}
install -p -m 644 dist/%{name}-generic-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-generic-%{version}.jar
install -p -m 644 dist/%{name}-view-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-view-%{version}.jar
%endif
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr dist/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr docs/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf docs/javadoc
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/site
cp LICENSE README.txt WHY_THREE_JARS.txt VLS_README.txt STATUS \
                  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/site
%else
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/site
%endif

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples test $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/STATUS
%doc %{_docdir}/%{name}-%{version}/*.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/site

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}

%{?_javapackages_macros:%_javapackages_macros}
Name:          velocity-tools
Version:       2.0
Release:       7.2
Summary:       Collection of useful tools for Velocity template engine
Group:		Development/Java
License:       ASL 2.0
Url:           http://velocity.apache.org/tools/releases/2.0/
Source0:       http://www.apache.org/dist/velocity/tools/%{version}/%{name}-%{version}-src.tar.gz
Patch0:        %{name}-%{version}-junit4.patch
Patch1:        %{name}-%{version}-dont_copy_test_lib.patch
# servlet 3.0 support thanks to mizdebsk
Patch2:        %{name}-%{version}-servlet.patch

BuildRequires: java-devel

BuildRequires: mvn(commons-beanutils:commons-beanutils)
BuildRequires: mvn(commons-chain:commons-chain)
BuildRequires: mvn(commons-collections:commons-collections)
BuildRequires: mvn(commons-digester:commons-digester)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(commons-validator:commons-validator)
BuildRequires: mvn(dom4j:dom4j)
BuildRequires: mvn(org.apache.struts:struts-core)
BuildRequires: mvn(org.apache.struts:struts-taglib)
BuildRequires: mvn(org.apache.struts:struts-tiles)
BuildRequires: mvn(org.apache.tomcat:tomcat-jsp-api)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires: mvn(org.apache.velocity:velocity)
BuildRequires: mvn(oro:oro)
BuildRequires: mvn(sslext:sslext)
# required by tomcat-jsp-api
BuildRequires: mvn(org.apache.tomcat:tomcat-el-api)

# test deps
%if 0
BuildRequires: mvn(httpunit:httpunit) = 1.6.1
BuildRequires: mvn(nekohtml:nekohtml) = 0.9.5
BuildRequires: mvn(org.mortbay.jetty:jetty-embedded) = 6.0.1
BuildRequires: mvn(rhino:js) = 1.6R5
BuildRequires: mvn(xerces:xercesImpl) = 2.8.1
BuildRequires: mvn(xerces:xmlParserAPIs) = 2.6.2
%endif
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-resources-plugin
# required by resources-plugin
BuildRequires: mvn(org.apache.maven.shared:maven-filtering)
BuildRequires: mvn(org.apache.maven.shared:maven-shared-components:pom:)

BuildArch:     noarch

%description
The VelocityTools project is a collection of useful Java classes (aka tools),
as well as infrastructure to easily, automatically and transparently
make these tools available to Velocity templates.

Project include easy integration of Velocity into the view-layer of
web applications (via the VelocityViewTag and
VelocityViewServlet) and integration with Struts 1.x applications.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}-src
find . -name "*.jar" -delete
find . -name "*.class" -delete
%patch0 -p1
%patch1 -p1
%patch2 -p0

sed -i 's/\r//' LICENSE NOTICE WHY_THREE_JARS.txt

# force tomcat 7.x apis
%pom_remove_dep javax.servlet:servlet-api
%pom_add_dep org.apache.tomcat:tomcat-servlet-api::provided
%pom_add_dep org.apache.tomcat:tomcat-jsp-api::provided
# remove non standard build structure
%pom_xpath_remove "pom:project/pom:build/pom:outputDirectory"
%pom_xpath_remove "pom:project/pom:build/pom:directory"

%mvn_file :%{name} %{name}
%mvn_alias :%{name} %{name}:%{name}
%mvn_alias :%{name} org.apache.velocity:%{name}-generic
%mvn_alias :%{name} %{name}:%{name}-generic
%mvn_alias :%{name} %{name}:%{name}-view
%mvn_alias :%{name} org.apache.velocity:%{name}-view

%build

# tests skipped. cause: missing dependencies
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc CONTRIBUTORS LICENSE NOTICE README.txt STATUS WHY_THREE_JARS.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 gil cattaneo <puntogil@libero.it> 2.0-6
- switch to XMvn
- minor changes to adapt to current guideline

* Tue Feb 19 2013 gil cattaneo <puntogil@libero.it> 2.0-5
- added maven-filtering as BR

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 gil cattaneo <puntogil@libero.it> 2.0-1
- initial rpm

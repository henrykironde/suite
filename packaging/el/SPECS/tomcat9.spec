%define __jar_repack %{nil}
%define tomcat_home /opt/tomcat9
%define tomcat_var tomcat9
%define tomcat_group tomcat9
%define tomcat_user tomcat9
%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename boundless-server-tomcat9-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       boundless-server-tomcat9
Version:    9.0.14
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Requires:   java-1.8.0-openjdk-headless >= 1.8.0
Conflicts:  boundless-server-tomcat8
%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.
Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.
This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.
%prep
%setup -q -n apache-tomcat-%{version}
%build
%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/
# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{tomcat_var}/
ln -s /var/log/%{tomcat_var} %{buildroot}/%{tomcat_home}/logs
# Put temp in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/temp
install -d -m 755 %{buildroot}/var/cache/%{tomcat_var}/temp
ln -s /var/cache/%{tomcat_var}/temp %{buildroot}/%{tomcat_home}/temp
# Put work in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/work
install -d -m 755 %{buildroot}/var/cache/%{tomcat_var}/work
ln -s /var/cache/%{tomcat_var}/work %{buildroot}/%{tomcat_home}/work
# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{tomcat_home}/conf/Catalina/localhost
install -m 644 %_sourcedir/context.xml %{buildroot}/%{tomcat_home}/conf/context.xml
# Put docs in /usr/share/doc
#install -d -m 755 %{buildroot}/usr/share/doc/%{tomcat_var}-%{version}
#mv %{buildroot}/%{tomcat_home}/{RUNNING.txt,LICENSE,NOTICE,RELEASE*} %{buildroot}/usr/share/doc/%{tomcat_var}-%{version}
install -d -m 755 %{buildroot}/%{_sysconfdir}/init.d
install -m 644 %_sourcedir/%{tomcat_var} %{buildroot}/%{_sysconfdir}/init.d/%{tomcat_var}
# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -m 644 %_sourcedir/%{tomcat_var}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{tomcat_var}
# Drop tomcat sysconfig file
#install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}/%{_sysconfdir}/%{tomcat_var}
install -m 644 %_sourcedir/%{tomcat_var}.sysconfig %{buildroot}/%{_sysconfdir}/%{tomcat_var}/%{tomcat_var}.conf
#copy conf to /etc
cp -r %{buildroot}/%{tomcat_home}/conf/* %{buildroot}/%{_sysconfdir}/%{tomcat_var}/
#remove /opt/tomcat9/conf/
rm -rf %{buildroot}%{tomcat_home}/conf
#create soft link
ln -s /etc/%{tomcat_var} %{buildroot}%{tomcat_home}/conf
%clean
rm -rf %{buildroot}
%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}
%files
%defattr(-,%{tomcat_user},%{tomcat_group})
/var/log/%{tomcat_var}/
/var/cache/%{tomcat_var}
%dir /opt/%{tomcat_var}/webapps
/opt/%{tomcat_var}/bin
/opt/%{tomcat_var}/conf
/opt/%{tomcat_var}/lib
/opt/%{tomcat_var}/logs
/opt/%{tomcat_var}/temp
/opt/%{tomcat_var}/work
%{_sysconfdir}/init.d/%{tomcat_var}
%{_sysconfdir}/logrotate.d/%{tomcat_var}
%{_sysconfdir}/%{tomcat_var}/%{tomcat_var}.conf
%{_sysconfdir}/%{tomcat_var}
#%doc /usr/share/doc/%{tomcat_var}-%{version}
#%files admin-webapps
%defattr(0644,root,root,0755)
/opt/%{tomcat_var}/webapps/host-manager
/opt/%{tomcat_var}/webapps/manager
#%files docs-webapp
%defattr(0644,root,root,0755)
/opt/%{tomcat_var}/webapps/docs
#%files examples-webapp
%defattr(0644,root,root,0755)
/opt/%{tomcat_var}/webapps/examples
#%files root-webapp
%defattr(0644,root,root,0755)
/opt/%{tomcat_var}/webapps/ROOT
%post
chmod +x /etc/init.d/%{tomcat_var}
chkconfig --add %{tomcat_var}
chkconfig %{tomcat_var} on
%preun
if [ $1 = 0 ]; then
  /etc/init.d/%{tomcat_var} > /dev/null 2>&1
fi
%postun
if [ $1 -ge 1 ]; then
  /etc/init.d/%{tomcat_var} > /dev/null 2>&1
fi

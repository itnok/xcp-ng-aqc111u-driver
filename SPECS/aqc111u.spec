%define uname  %{kernel_version}
%define module_dir updates

Summary: Driver for 5-Gigabit Ethernet adapters based on Marvell/Aquantia AQC111u Multigigabit NIC Family
Name: aqc111u-driver
Version: 1.3.3.0
Release: %{?release}%{!?release:1}
License: GPL
Source0: %{name}-%{version}.tar.gz

BuildRequires: kernel-devel
Provides: %{name}
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
Driver for 5-Gigabit Ethernet adapters based on Marvell/Aquantia AQC111u Multigigabit NIC Family

%prep
curl -sL 'https://www.sabrent.com/download/nt-ss5g/?wpdmdl=86032&ind=1593648240565' > $(dirname $(pwd))/SOURCES/%{name}-%{version}.zip
unzip -o $(dirname $(pwd))/SOURCES/%{name}-%{version}.zip -d /tmp
mkdir -p $(dirname $(pwd))/SOURCES/%{name}-%{version}
tar -xzvf /tmp/fiji.tar.gz -C /tmp
mv /tmp/Linux /tmp/%{name}-%{version}
tar -czvf $(dirname $(pwd))/SOURCES/%{name}-%{version}.tar.gz -C /tmp ./%{name}-%{version}
ls $(dirname $(pwd))/SOURCES/ | grep -v %{name}-%{version}.tar.gz | xargs -I++++ rm -rf $(dirname $(pwd))/SOURCES/++++
%setup -q -n %{name}-%{version}

%build
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
%defattr(-,root,root,-)
/lib/modules/%{uname}/*/*.ko
%doc

%changelog
* Sat Mar 20 2021 Simone Conti <s.conti@itnok.com> - 1.3.3.0
- Driver for Marvell/Aquantia AQC111u-based NICs packing for XCP-ng


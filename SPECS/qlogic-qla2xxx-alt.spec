%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name qla2xxx

# XCP-ng: install to the override directory
%define module_dir override

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 10.02.14.01_k
Release: 2%{?dist}
# Built against new kABI after cip rebase
Requires: xcpng-kernel-kabi = 4.19.325-cip134+

License: GPL

# Source tarball from https://www.marvell.com/support/downloads.html
Source0: qlogic-qla2xxx-10.02.14.01_k.tar.gz
Patch0: fix-livepatching.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: qlogic-qla2xxx-firmware
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{vendor_label}-%{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KVER=%{kernel_version} KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) KVER=%{kernel_version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Mon Aug 31 2026 Quentin Casasnovas <quentin.casasnovas@vates.tech> - 10.02.14.01_k-2
- Rebuild for kernel v4.19.325-cip134

* Thu Dec 11 2025 Thierry Escande <thierry.escande@vates.tech> - 10.02.14.01_k-1
- Synced sources to version 10.02.14.01-k from marvell.com

* Fri May 03 2024 Gael Duperrey <gduperrey@vates.tech> - 10.02.11.00_k-1
- Update to version 10.02.11.00_k
- Synced from XS driver SRPM qlogic-qla2xxx-10.02.11.00_k-1.xs8~2_1.src.rpm

* Thu Jun 29 2023 Gael Duperrey <gduperrey@vates.fr> - 10.02.09.00_k-1
- initial package, version 10.02.09.00_k

---
title: "A Guide to Building, Installing and Booting the Linux Kernel"
date: 2024-06-02
description: "Build, install and boot a Linux kernel."
summary: "Notes on building, installing and booting the Linux kernel on real hardware."
tags: ["C", "linux", "osdev"]
draft: false
---

This is intended to be a note on the steps required to build, install, boot, and troubleshoot a custom Linux kernel on real hardware. I have [another post]({{< ref "/posts/booting-a-custom-linux-kernel.md" >}}) that describes the kernel set-up process using the QEMU emulator.

## Installing dependencies

```sh
sudo apt-get install build-essential vim git cscope libncurses-dev libssl-dev bison flex
```

## Clone the Linux kernel source

```sh
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git linux_mainline
cd linux_mainline
```

### Choosing a Linux version

You can view the versions available by using the *git tag* command:

```sh
git tag -l
```

Choose a Linux version you want to build from the tags and create a branch that is a copy of it. If I wanted to build **v6.8**, I would do:

```sh
git checkout -b my6.8 v6.8
```

## Building and installing the kernel

Starting out with the distribution configuration file is the safest approach for the very first kernel install on any system:

```sh
cp /boot/config-`uname -r` .config
```

### Compiling the kernel

```sh
make oldconfig
```

Another way to trim down the kernel and tailor it to your system is by using `make localmodconfig`. You can use `make help` to view all the *make* options available.

```sh
lsmod > /tmp/my-lsmod
make LSMOD=/tmp/my-lsmod localmodconfig
```

### Options for kernel modules development

If you will be building, and loading kernel modules on the kernel you are going to build, some options should be updated to make you life easier. First, open the `.config` file and ensure `CONFIG_MODVERSIONS` is set to `y`. This allows your to load kernel modules build on one version on another version.

You should also disable module signing so you can freely experiment by loading the modules you develop. Update your `.config` to match the snippet provided below for each option:

```sh
CONFIG_MODULE_SIG=n
CONFIG_MODULE_SIG_ALL=n
# CONFIG_MODULE_SIG_FORCE is not set
# CONFIG_MODULE_SIG_SHA1 is not set
# CONFIG_MODULE_SIG_SHA224 is not set
# CONFIG_MODULE_SIG_SHA256 is not set
# CONFIG_MODULE_SIG_SHA384 is not set
```

### Building the kernel

Build your kernel with:

```sh
make -j12 all
```

### Installing the new kernel

Once the kernel build is complete, install the new kernel:

```sh
su -c "make modules_install install"
```

The above command will install the new kernel and run *update-grub* to add the new kernel to the grub menu.

### Booting the kernel

In `/etc/default/grub`, set the GRUB_TIMEOUT value to 60 seconds, so grub pauses in the menu long enough to choose a kernel to boot and also enable printing early boot messages to *vga* using the *earlyprintk=vga* kernel boot option by adding `GRUB_CMDLINE_LINUX="earlyprintk=vga"` to the file.

The content of my `/etc/default/grub` file is shared below:

```sh
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_TIMEOUT=60
GRUB_TIMEOUT_STYLE=menu
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX="earlyprintk=vga"

# If your computer has multiple operating systems installed, then you
# probably want to run os-prober. However, if your computer is a host
# for guest OSes installed via LVM or raw disk devices, running
# os-prober can cause damage to those guest OSes as it mounts
# filesystems to look for things.
#GRUB_DISABLE_OS_PROBER=false

# Uncomment to enable BadRAM filtering, modify to suit your needs
# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"

# Uncomment to disable graphical terminal
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
# note that you can use only modes which your graphic card supports via VBE
# you can see them in real GRUB with the command `vbeinfo'
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true

# Uncomment to disable generation of recovery mode menu entries
#GRUB_DISABLE_RECOVERY="true"

# Uncomment to get a beep at grub start
#GRUB_INIT_TUNE="480 440 1"
```

Run *update-grub* to update the grub configuration in */boot*:

```sh
sudo update-grub
```

Restart the system. Once the new kernel comes up, compare the *dmesg* from the old kernel with the new one(the next section describes how), and see if there are any regressions.

## Examining kernel logs

You should compare the logs obtained by running the following commands on the current(old) kernel with your new custom kernel to check for regressions. There should be no new *crit*, *alert*, and *emerg* level messages in *dmesg*. There should be no new *err* level messages too.

```sh
dmesg -t -l emerg
dmesg -t -l crit
dmesg -t -l alert
dmesg -t -l err
dmesg -t -l warn
dmesg -t -k
dmesg -t
```

## Useful debug options

The following kernel configurations are useful for debugging if you are going to be hacking the kernel.

```sh
CONFIG_KASAN
CONFIG_KMSAN
CONFIG_UBSAN
CONFIG_LOCKDEP
CONFIG_PROVE_LOCKING
CONFIG_LOCKUP_DETECTOR
```

## Uninstalling custom compiled kernel

To remove a custom Linux kernel installed on your machine, you need to remove the following files/dirs:

1. /boot/vmlinuz*KERNEL-VERSION*
2. /boot/initrd*KERNEL-VERSION*
3. /boot/System-map*KERNEL-VERSION*
4. /boot/config-*KERNEL-VERSION*
5. /lib/modules/*KERNEL-VERSION*/

Then, update the grub configuration file with:

```sh
sudo update-grub
```

## Further reading

1. https://www.freedesktop.org/wiki/Software/PulseAudio/HowToUseGitSendEmail/
2. https://www.opensourceforu.com/2011/01/understanding-a-kernel-oops/
3. https://sanjeev1sharma.wordpress.com/tag/debug-kernel-panics/
4. https://www.kernel.org/doc/html/latest/trace/events.html
5. https://www.kernel.org/doc/html/latest/admin-guide/bug-hunting.html
6. https://www.kernel.org/doc/html/latest/admin-guide/bug-bisect.html
7. https://www.kernel.org/doc/html/latest/admin-guide/dynamic-debug-howto.html
8. https://lwn.net/Articles/592724/

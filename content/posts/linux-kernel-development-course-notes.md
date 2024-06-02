---
title: "A Beginner's Guide to Linux Kernel Development (LFD103)"
date: 2024-05-15
description: "A Beginner's Guide to Linux Kernel Development (LFD103)"
summary: "A Beginner's Guide to Linux Kernel Development (LFD103) Course by Linux Foundation"
tags: ["C", "linux", "osdev"]
draft: true
---

## Installing dependencies

```sh
sudo apt-get install build-essential vim git cscope libncurses-dev libssl-dev bison flex
sudo apt-get install git-email
```

## Seting up an email client

Setting up git email.

### Configure name and email address

```sh
git config --global user.name "Oye Oloyede"
git config --global user.email "oyekunlemac@gmail.com"
```

### Configure the mail sending options

Google mail setup - https://support.google.com/a/answer/176600?hl=en

```sh
git config --global sendemail.smtpencryption tls
git config --global sendemail.smtpserver smtp.gmail.com
git config --global sendemail.smtpserverport 587
git config --global sendemail.smtpuser oyekunlemac@gmail.com
git config --global sendemail.smtppass <password here>
```

This [article](https://www.freedesktop.org/wiki/Software/PulseAudio/HowToUseGitSendEmail/) is a good reference.

## Exploring the linux kernel sources

```sh
cd /linux_work
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git linux_mainline
cd linux_mainline; ls -h
```

You can prepare a patch for any commit using:

```sh
git format-patch 1 <commit-id>
```

## Building and installing the kernel

Starting out with the distribution configuration file is the safest approach for the very first kernel install on any system

```sh
cp /boot/config-6.1.0-21-amd64 .config
```

### Compiling the kernel

```sh
make oldconfig
```

Another way to trim down the kernel and tailor it to your system is by using `make localmodconfig`. This option creates a configuration file based on the list of modules currently loaded on your system.

```sh
lsmod > /tmp/my-lsmod
make LSMOD=/tmp/my-lsmod localmodconfig
```

```sh
make -j12 all
```

### Installing the new kernel

Once the kernel compilation is complete, install the new kernel:

```sh
su -c "make modules_install install"
```

The above command will install the new kernel and run update-grub to add the new kernel to the grub menu.

Before we reboot into the new kernel, let's save logs from the current kernel to compare and look for regressions and new errors, if any.

dmesg -t > dmesg_current
dmesg -t -k > dmesg_kernel
dmesg -t -l emerg > dmesg_current_emerg
dmesg -t -l alert > dmesg_current_alert
dmesg -t -l crit > dmesg_current_crit
dmesg -t -l err > dmesg_current_err
dmesg -t -l warn > dmesg_current_warn
dmesg -t -l info > dmesg_current_info

### Booting the kernel

In `/etc/default/grub` GRUB_TIMEOUT value to 60 seconds, so grub pauses in menu long enough to choose a kernel to boot and also enable printing early boot messages to vga using the earlyprintk=vga kernel boot option by adding `GRUB_CMDLINE_LINUX="earlyprintk=vga"` to the file.

The content of my `/etc/default/grup` file is shown below:

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

Run update-grub to update the grub configuration in /boot:

```sh
sudo update-grub
```

Restart the system. Once the new kernel comes up, compare the saved dmesg from the old kernel with the new one, and see if there are any regressions.

## Examining kernel logs

Checking for regressions in dmesg is a good way to identify problems, if any, introduced by the new code. As a general rule, there should be no new crit, alert, and emerg level messages in dmesg. There should be no new err level messages. Pay close attention to any new warn level messages as well. Please note that new warn messages are not as bad. At times, new code adds new warning messages which are just warnings.

dmesg -t -l emerg
dmesg -t -l crit
dmesg -t -l alert
dmesg -t -l err
dmesg -t -l warn
dmesg -t -k
dmesg -t

Are there any stack traces resulting from WARN_ON in the dmesg? These are serious problems that require further investigation.

## Debug options and proactive testing

As you are making changes to drivers and other areas in the kernel, there are a few things to watch out for. There are several configuration options to test for locking imbalances and deadlocks. It is important to remember to enable the Lock Debugging and CONFIG_KASAN for memory leak detection. We do not intend to cover debugging in depth in this chapter, but we want you to start thinking about debugging and configuration options that facilitate debugging. Enabling the following configuration option is recommended for testing your changes to the kernel:

CONFIG_KASAN
CONFIG_KMSAN
CONFIG_UBSAN
CONFIG_LOCKDEP
CONFIG_PROVE_LOCKING
CONFIG_LOCKUP_DETECTOR

I will leave you to play with these debug configuration options and explore others. Running git grep -r DEBUG | grep Kconfig can find all supported debug configuration options.

## Debugging

### Kernel panics

Read these:
https://www.opensourceforu.com/2011/01/understanding-a-kernel-oops/
https://sanjeev1sharma.wordpress.com/tag/debug-kernel-panics/

## Decode and analyze the panic message

https://lwn.net/Articles/592724/

Panic messages can be decoded using the decode_stacktrace.sh tool.

Usage:
      scripts/decode_stacktrace.sh -r <release> | <vmlinux> [base path] [modules path]

Save (cut and paste) the panic trace in the dmesg between the two following lines of text into a .txt file.

------------[ cut here ]------------
---[ end trace …. ]---

Run this tool in your kernel repo. You will have to supply the [base path], which is the root of the git repo where the vmlinux resides if it is different from the location the tool is run from. If the panic is in a dynamically kernel module, you will have to pass in the [modules path] where the modules reside.

scripts/decode_stacktrace.sh ./vmlinux < panic_trace.txt

Reading code:

    It goes without saying that reading code and understanding the call trace leading up to the failure is an essential first step to debugging and finding a suitable fix.

# Event tracing

https://www.kernel.org/doc/html/latest/trace/events.html
https://www.kernel.org/doc/html/latest/admin-guide/bug-hunting.html
https://www.kernel.org/doc/html/latest/admin-guide/bug-bisect.html
https://www.kernel.org/doc/html/latest/admin-guide/dynamic-debug-howto.html

## Uninstalling custom compiled kernel

If you have a custom compiled Linux kernel running, you need to remove the following files/dirs:

    /boot/vmlinuz*KERNEL-VERSION*
    /boot/initrd*KERNEL-VERSION*
    /boot/System-map*KERNEL-VERSION*
    /boot/config-*KERNEL-VERSION*
    /lib/modules/*KERNEL-VERSION*/

Then:
    Update grub configuration file with sudo update-grub

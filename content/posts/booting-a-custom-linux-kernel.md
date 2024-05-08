---
title: "Build and Boot a Custom Linux Kernel"
date: 2024-05-08
description: "Setup for kernel hacking."
summary: "This tutorial shows you how to get setup your environment for Linux kernel hacking. We will install the required dependencies, build, and boot into the Linux kernel."
tags: ["C", "linux", "osdev"]
draft: true
---

You will expect to run a program after making changes to it. The same is expected even when hacking on a real kernel. This article will document how to install the required packages, build and run the Linux on QEMU and natively on your local Linux host.
I will be using  a Debian distribution to run all commands provided, you might need to modify them if you are using an non-debian based distribution.

## Install the required packages

The kernel is written in C, so we add the usuall assortment of C development packages:

```sh
sudo apt-get install vim libncurses5-dev gcc make git exuberant-ctags libssl-dev bison flex libelf-dev bc dwarves zstd git-email
```

A lot of these packages might already be preinstalled on your machine, depending on your distribution and how minimal your installation was.

We also need to install the QEMU virtual machine as it offers a quick boot for testing changes:

```sh
sudo apt-get install qemu-system
```

## Build the kernel

### Pull the repository

First, pull the mainline repository with:

```sh
git clone http://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
```

`cd` into the folder with:

```sh
cd linux
```

### Configure the kernel

We need a basic config that should work on our current architecture. We can get that with:

```sh
make defconfig
```

An optional change we can make is to disable `CONFIG_MODULES`. I will not be making this config change, but if you wish to do so, first start the config GUI with:

```sh
make menuconfig
```

Then type `/MODULES`, press enter to search, press `1` to take us to the first match, then press `n` to disable this option.
Save, and exit.

### Building the kernel

`make jX` will build the kernel, where `X` is replaced with the number of core on your machine. On my 6 cores computer, I use:

```sh
make -j6
```

## Run in the QEMU VM

Start by downloading a minimal disk image by clicking [here](https://people.debian.org/~aurel32/qemu/amd64/debian_wheezy_amd64_standard.qcow2).

Move the dowloaded file into your *linux* working directory.

Boot into the kernel in the VM with:

```sh
kvm -cpu host -hda debian_wheezy_amd64_standard.qcow2 -kernel arch/x86/boot/bzImage -append "console=ttyS0 root=/dev/sda init=/bin/bash" -serial stdio -no-reboot -display none -m 1G
```

That did not go as planned for me. The kernel panicked because no root filesystem. Here's a snippet of the output:

```sh
[    1.218917] List of all partitions:
[    1.219186] 0800        26214400 sda
[    1.219187]  driver: sd
[    1.219628]   0801        25165824 sda1 00007738-01
[    1.219629]
[    1.220080]   0802               1 sda2
[    1.220081]
[    1.220423]   0805         1045504 sda5 00007738-05
[    1.220424]
[    1.220839] 0b00         1048575 sr0
[    1.220840]  driver: sr
[    1.221266] No filesystem could mount root, tried:
[    1.221267]  ext3
[    1.221690]  ext2
[    1.221831]  ext4
[    1.221955]  vfat
[    1.222079]  msdos
[    1.222200]  iso9660
[    1.222333]
[    1.222570] Kernel panic - not syncing: VFS: Unable to mount root fs on "/dev/sda" or unknown-block(8,0)
[    1.223175] CPU: 0 PID: 1 Comm: swapper/0 Not tainted 6.9.0-rc7-00056-g45db3ab70092 #1
[    1.223792] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.16.2-debian-1.16.2-1 04/01/2014
[    1.224533] Call Trace:
[    1.224733]  <TASK>
[    1.224896]  panic+0x31d/0x350
[    1.225137]  mount_root_generic+0x2d6/0x340
[    1.225455]  prepare_namespace+0x64/0x280
[    1.225751]  kernel_init_freeable+0x286/0x2d0
[    1.226030]  ? __pfx_kernel_init+0x10/0x10
[    1.226281]  kernel_init+0x15/0x1b0
[    1.226500]  ret_from_fork+0x2c/0x50
[    1.226714]  ? __pfx_kernel_init+0x10/0x10
[    1.226979]  ret_from_fork_asm+0x1a/0x30
[    1.227262]  </TASK>
[    1.227488] Kernel Offset: 0x9000000 from 0xffffffff81000000 (relocation range: 0xffffffff80000000-0xffffffffbfffffff)
[    1.228210] ---[ end Kernel panic - not syncing: VFS: Unable to mount root fs on "/dev/sda" or unknown-block(8,0) ]---
```

We will create a ramdisk and pass this to QEMU. Create the ramdisk with:

```sh
mkinitramfs -o ramdisk.img
```

Let's try the previous command, this time, pass the ramdisk in place of the minimal disk image we downloaded:

```sh
kvm -cpu host -kernel arch/x86/boot/bzImage -append "console=ttyS0" -initrd ramdisk.img -nographic -m 1G
```

Success! We are able to boot into the kernel in a VM.

## Running natively

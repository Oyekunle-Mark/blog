---
title: "Build and Boot a Custom Linux Kernel"
date: 2024-05-08
description: "Setup for kernel hacking."
summary: "This tutorial shows you how to set up your environment for Linux kernel hacking. We will install the required dependencies, build, and boot into the Linux kernel."
tags: ["C", "linux", "osdev"]
draft: false
---

You will expect to run a program after making changes to it. The same is expected even when hacking a kernel. This article will document how to install the required packages and build and run Linux on QEMU along with a pointer to where to get started with debugging the kernel with the GDB debugger.

I will be using a Debian distribution to run all the commands provided. You might need to modify some of them if you are using a non-debian-based distribution.

## Install the required packages

The kernel is written in C, so we add the usual assortment of C development packages and some osdev-related packages:

```sh
sudo apt-get install vim libncurses5-dev gcc make git exuberant-ctags libssl-dev bison flex libelf-dev bc dwarves zstd git-email fakeroot
```

A lot of these packages might already be preinstalled on your machine, depending on your distribution and how minimal your installation was.

Next, we install the QEMU virtual machine as we will be using it to boot and run the kernel:

```sh
sudo apt-get install qemu-system
```

Finally, in the installation phase, we want to install the GDB debugger for debugging the kernel.

```sh
sudo apt-get install gdb
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

We need a config file that would work on an `x86_64` architecture. You can find the config file that will be used as a base for the `x86_64` architecture in `arch/x86/configs/x86_64_defconfig`. 

Create one such config file with:

```sh
make ARCH=x86_64 x86_64_defconfig
```

### Build the kernel

`make jX` will build the kernel, where `X` is replaced with the number of cores on your machine. On my 6-core computer, I use:

```sh
make -j6
```

The kernel will be built into `/arch/x86/boot/bzImage`.

## Run the kernel

Boot into the kernel in the VM with:

```sh
kvm -cpu host -hda /dev/zero -kernel arch/x86/boot/bzImage -append "console=ttyS0 root=/dev/zero" -serial stdio -display none -m 1G
```

That did not go as planned. The kernel panicked because it could not find a root filesystem. Here's a snippet of the output:

```sh
[    1.183672] Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
[    1.184077] CPU: 0 PID: 1 Comm: swapper/0 Not tainted 6.9.0-rc7-00136-gf4345f05c0df #1
[    1.184469] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.16.2-debian-1.16.2-1 04/01/2014
[    1.184937] Call Trace:
[    1.185073]  <TASK>
[    1.185186]  panic+0x31d/0x350
[    1.185348]  mount_root_generic+0x20e/0x340
[    1.185560]  prepare_namespace+0x64/0x280
[    1.185762]  kernel_init_freeable+0x286/0x2d0
[    1.185982]  ? __pfx_kernel_init+0x10/0x10
[    1.186189]  kernel_init+0x15/0x1b0
[    1.186368]  ret_from_fork+0x2c/0x50
[    1.186552]  ? __pfx_kernel_init+0x10/0x10
[    1.186758]  ret_from_fork_asm+0x1a/0x30
[    1.186958]  </TASK>
[    1.187153] Kernel Offset: 0x1de00000 from 0xffffffff81000000 (relocation range: 0xffffffff80000000-0xffffffffbfffffff)
[    1.187680] ---[ end Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0) ]---
```

We will need to build a root file system and pass that to QEMU when we boot the kernel.

### Build a root file system

We will use Buildroot to build a root file system.

First, we navigate to the parent directory of our `linux` working directory, clone the Buildroot project and cd into it:

```sh
git clone git://git.buildroot.net/buildroot
cd buildroot
```

We need a `.config` file before building.

We can create one using the text-based configuration interface with:

```sh
make menuconfig
```

Choose **Target options** and ensure you have the `i586` architecture selected. This was selected by default when I checked under the **Target options -> i586 Architecture variants** options.

Next, navigate back to the first page of the menu and choose **Filesystem images**. Enable the **ext2/3/4 root file system** option. Beneath it, choose the variant option and enable **ext4**.

Save, and exit. This creates the required `.config` file.

Then, build with:

```sh
make -j6
```

### Run QEMU with the kernel and a root file system

Let's try again, this time we pass our root file system to QEMU.

```sh
kvm -cpu host -hda ../buildroot/output/images/rootfs.ext4 -kernel arch/x86/boot/bzImage -append "root=/dev/sda rw console=ttyS0,115200 acpi=off nokaslr" -serial stdio -display none -m 2G
```

We also added the `nokaslr` option to *append*. That turns off the [Linux kernel address space layout randomization](https://lwn.net/Articles/569635/).

Buildroot uses `root` as the default login user without a password.

```sh
[    1.420582] EXT4-fs (sda): mounted filesystem 60764e06-39d9-40d0-a708-c9a1b09d76e9 r/w with ordered data mode. Quota mode: none.
[    1.422351] VFS: Mounted root (ext4 filesystem) on device 8:0.
[    1.423929] devtmpfs: mounted
[    1.424876] Freeing unused kernel image (initmem) memory: 2700K
[    1.425605] Write protecting the kernel read-only data: 26624k
[    1.426781] Freeing unused kernel image (rodata/data gap) memory: 1484K
[    1.433053] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    1.433369] Run /sbin/init as init process
[    1.438727] mount (52) used greatest stack depth: 13504 bytes left
[    1.442316] EXT4-fs (sda): re-mounted 60764e06-39d9-40d0-a708-c9a1b09d76e9 r/w. Quota mode: none.
[    1.444099] mkdir (56) used greatest stack depth: 13288 bytes left
Saving 256 bits of creditable seed for next boot
Starting syslogd: OK
Starting klogd: OK
Running sysctl: OK
Starting network: OK

Welcome to Buildroot
buildroot login: root
# ls
# pwd
/root
# whoami
root
# lsmod
Module                  Size  Used by    Not tainted
```

Now we can successfully boot into the kernel.

## Add the QEMU GDB support

To debug the kernel with QEMU and GDB, we need to build the kernel with a config file with debugging options enabled. You can update your config with:

```sh
make menuconfig
```

Find a specific option you want to turn on or off by pressing `/<CONFIG_XXXXX>`, press enter to search for the config, and use the numbers presented in the results to locate where to enable/disable the option.

This [page](https://docs.kernel.org/dev-tools/gdb-kernel-debugging.html) provides the information required for debugging the kernel(v6.9) and modules via gdb. Follow it to find the config required for kernel debugging, and how to have GDB debug your custom kernel.

## Conclusion and next steps

Operating system development is a painful undertaking. Even when it involves learning to read and make small changes to the codebase of an already-matured kernel like Linux. The ability to quickly run the kernel in a VM like QEMU and attach GDB to it for debugging makes the experience less of a pain.

For the next steps, I will be diving into [Understanding the Linux Kernel](https://amzn.eu/d/cmMIN5d). The book is dated, but I expect it to be sufficient in getting me from kernel noob to being ready to hack the kernel. You might be seeing more posts from me on the Linux kernel internals as I progress through the book and dive into the implementation of the kernel.

Thanks for following along.

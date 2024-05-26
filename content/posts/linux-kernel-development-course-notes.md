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

## Setup email client

Article followed - https://www.freedesktop.org/wiki/Software/PulseAudio/HowToUseGitSendEmail/

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

Follow this to complete setup: https://stackoverflow.com/questions/68238912/how-to-configure-and-use-git-send-email-to-work-with-gmail-to-email-patches-to

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

Run the following command to generate a kernel configuration file based on the current configuration. This step is important to configure the kernel, which has a good chance to work correctly on your system. You will be prompted to tune the configuration to enable new features and drivers that have been added since Ubuntu snapshot the kernel from the mainline. `make all` will invoke `make oldconfig` in any case. I am showing these two steps separately just to call out the configuration file generation step.

```sh
make oldconfig
```

Another way to trim down the kernel and tailor it to your system is by using `make localmodconfig`. This option creates a configuration file based on the list of modules currently loaded on your system.

```sh
lsmod > /tmp/my-lsmod
make LSMOD=/tmp/my-lsmod localmodconfig
```

Once this step is complete, it is time to compile the kernel. Using the `-j` option helps the compiles go faster. The `-j` option specifies the number of jobs (make commands) to run simultaneously:

```sh
make -j3 all
```

### Installing the new kernel

Once the kernel compilation is complete, install the new kernel:

su -c "make modules_install install"

The above command will install the new kernel and run update-grub to add the new kernel to the grub menu. Now it is time to reboot the system to boot the newly installed kernel. Before we do that, let's save logs from the current kernel to compare and look for regressions and new errors, if any. Using the -t option allows us to generate dmesg logs without the timestamps, and makes it easier to compare the old and the new.

dmesg -t > dmesg_current
dmesg -t -k > dmesg_kernel
dmesg -t -l emerg > dmesg_current_emerg
dmesg -t -l alert > dmesg_current_alert
dmesg -t -l crit > dmesg_current_crit
dmesg -t -l err > dmesg_current_err
dmesg -t -l warn > dmesg_current_warn
dmesg -t -l info > dmesg_current_info

In general, dmesg should be clean, with no emerg, alert, crit, and err level messages. If you see any of these, it might indicate some hardware and/or kernel problem.

If the dmesg_current is zero length, it is very likely that secure boot is enabled on your system. When secure boot is enabled, you won’t be able to boot the newly installed kernel, as it is unsigned. You can disable secure boot temporarily on startup with MOK manager. Your system should already have mokutil.

Let's first make sure secure boot is indeed enabled:

mokutil --sb-state

If you see the following, you are all set to boot your newly installed kernel:

SecureBoot disabled
Platform is in Setup Mode

If you see the following, disable secure boot temporarily on startup with MOK manager:

SecureBoot enabled
SecureBoot validation is disabled in shim

Disable validation:

sudo mokutil --disable-validation
root password
mok password: 12345678
mok password: 12345678
sudo reboot

The machine will reboot in a blue screen, the MOK manager menu. Type the number(s) shown on the screen: if it is 7, it is the 7th character of the password. So, keep 12345678. The question to answer is Yes to disable secure boot. Reboot.

You’ll see on startup after a new message (top left) saying <<Booting in insecure mode>>. The machine will boot normally after and secure boot remains enabled. This change is permanent, a clean install won't overwrite it. You must keep it that way.

To re-enable it (please note that you won't be able to boot the kernels you build if you re-enable):

sudo mokutil --enable-validation
root password
mok password: 12345678
mok password: 12345678
sudo reboot


### useful link
https://askubuntu.com/questions/1119734/how-to-replace-or-remove-kernel-with-signed-kernels

### Booting the kernel

Booting the Kernel

Let’s take care of a couple of important steps before trying out the newly installed kernel. There is no guarantee that the new kernel will boot. As a safeguard, we want to make sure that there is at least one good kernel installed and we can select it from the boot menu. By default, grub tries to boot the default kernel, which is the newly installed kernel. We change the default grub configuration file /etc/default/grub to the boot menu, and pause for us to be able to select the kernel to boot.

 

🚩
Please note that this option is specific to Ubuntu, and other distributions might have a different way to specify boot menu options.

 

Increase the GRUB_TIMEOUT value to 10 seconds, so grub pauses in menu long enough to choose a kernel to boot:

    Uncomment GRUB_TIMEOUT and set it to 10: GRUB_TIMEOUT=10
    Comment out GRUB_TIMEOUT_STYLE=hidden

If the newly installed kernel fails to boot, it is nice to be able to see the early messages to figure out why the kernel failed to boot.

 

Enable printing early boot messages to vga using the earlyprintk=vga kernel boot option:

GRUB_CMDLINE_LINUX="earlyprintk=vga"

 

Run update-grub to update the grub configuration in /boot

sudo update-grub

 

Now, it’s time to restart the system. Once the new kernel comes up, compare the saved dmesg from the old kernel with the new one, and see if there are any regressions. If the newly installed kernel fails to boot, you will have to boot a good kernel, and then investigate why the new kernel failed to boot.​

These steps are not specific to stable kernels. You can check out linux mainline or linux-next and follow the same recipe of generating a new configuration from an oldconfig, build, and install the mainline or linux-next kernels.





TODO: *

https://www.kernel.org/doc/html/latest/process/email-clients.html
https://kernelnewbies.org/FirstKernelPatch



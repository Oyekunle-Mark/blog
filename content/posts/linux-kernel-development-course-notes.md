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


TODO: *

https://www.kernel.org/doc/html/latest/process/email-clients.html
https://kernelnewbies.org/FirstKernelPatch



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

## Making changes to a driver

Now, let’s select a driver to make a change. Run lsmod to see the modules loaded on your system, and pick a driver to change. I will walk you through changing the uvcvideo driver. If you don’t have uvcvideo on your system, find a different driver and follow along using your driver name instead of uvcvideo.

Once you have the name of a driver, it's time to find out where the .c and .h files for that driver are in the Linux kernel repository. Even though searching Makefiles will get you the desired result, git grep will get you there faster, searching only the checked-in files in the repository. git grep will skip all generated files such as .o’s, .ko’s and binaries. It will skip the .git directory as well. Okay, now let’s run git grep to look for uvcvideo files.

git grep uvcvideo -- '*Makefile'
drivers/media/usb/uvc/Makefile:uvcvideo-objs := uvc_driver.o uvc_queue.o uvc_v4l2.o uvc_video.o uvc_ctrl.o drivers/media/usb/uvc/Makefile:uvcvideo-objs += uvc_entity.o
drivers/media/usb/uvc/Makefile:obj-$(CONFIG_USB_VIDEO_CLASS) += uvcvideo.o

uvcvideo is a USB Video Class (UVC) media driver for video input devices, such as webcams. It supports webcams on laptops. Let’s check the source files for this driver.

ls drivers/media/usb/uvc/
Kconfig uvc_debugfs.c uvc_isight.c uvc_status.c uvcvideo.h
Makefile uvc_driver.c uvc_metadata.c uvc_v4l2.c
uvc_ctrl.c uvc_entity.c uvc_queue.c uvc_video.c

Let's make a small change to the probe function of the uvcvideo driver. A probe function is called when the driver is loaded. Let's edit uvc_driver.c:

vim drivers/media/usb/uvc/uvc_driver.c

Find the probe function by searching for _probe text by typing / in standard mode. Once you've found the probe function, add pr_info() to it and save the file. A pr_info() function writes a message to the kernel log buffer, and we can see it using dmesg.

static int uvc_probe(struct usb_interface *intf,
                     const struct usb_device_id *id)
{
        struct usb_device *udev = interface_to_usbdev(intf);
        struct uvc_device *dev;
        const struct uvc_device_info *info =
                (const struct uvc_device_info *)id->driver_info;
        int function;
        int ret;

        pr_info("I changed uvcvideo driver in the Linux Kernel\n");

        if (id->idVendor && id->idProduct)
                uvc_trace(UVC_TRACE_PROBE, "Probing known UVC device %s "
                                "(%04x:%04x)\n", udev->devpath, id->idVendor,
                                id->idProduct);
        else
                uvc_trace(UVC_TRACE_PROBE, "Probing generic UVC device %s\n",
                                udev->devpath);​

Let’s try configuring uvcvideo as a built-in and as a module to play with installing, loading and unloading modules.

Configure as a module:

    Configure CONFIG_USB_VIDEO_CLASS=y
    Recompile your kernel and install. Please note that you don't have to reboot your system. You can load your newly installed module.

Load module:

    sudo modprobe uvcvideo
    Once you load the module, let's check if you see your message.
    Run dmesg | less and search for "I changed". Do you see the message?
    Run lsmod | grep uvcvideo. Do you see the module?

Unload module:

    sudo rmmod uvcvideo
    Check dmesg for any messages about the uvcvideo module removal.
    Run lsmod | grep uvcvideo. Do you see the module?

Configure Built-in:

    Configure CONFIG_USB_VIDEO_CLASS=y
    Recompile your kernel, install, and reboot the system into the newly installed kernel.
    Run dmesg | less and search for "I changed". Do you see the message?

## Practicing commits

Let's practice committing a change. You can see the files you modified by running the git status command. Let's first check if your changes follow the coding guidelines outlined in the Linux kernel coding style guide. You can run checkpatch.pl on the diff or the generated patch to verify if your changes comply with the coding style. It is good practice to check by running checkpatch.pl on the diff before testing and committing the changes. I find it useful to do this step even before I start testing my patch. This helps avoid redoing testing in case code changes are necessary to address the checkpatch errors and warnings.

You can see my patch workflow below.

Make code changes and compile -> run checkpatch.pl on your changes(git diff > temp; scripts/checkpatch.pl temp) -> fix errors and warns
 

Patch Workflow

Make sure you address checkpatch errors and/or warnings. Once checkpatch is happy, test your changes and commit your changes.

If you want to commit all modified files, run:

git commit -a

If you have changes that belong in separate patches, run:

git commit <filenames>

When you commit a patch, you will have to describe what the patch does. The commit message has a subject or short log and longer commit message. It is important to learn what should be in the commit log and what doesn’t make sense. Including what code does isn’t very helpful, whereas why the code change is needed is valuable. Please read How to Write a Git Commit Message for tips on writing good commit messages.

Now, run the commit and add a commit message. After committing the change, generate the patch running the following command:

git format-patch -1 <commit ID>

## Sending a patch for review

So far, you learned how to make a change, check for coding style compliance, and generate a patch. The next step is learning the logistics of how to send a patch to the Linux Kernel mailing lists for review. The get_maintainer.pl script tells you whom to send the patch to. The two example runs of get_maintainer.pl show the list of people to send patches to. You should send the patch to maintainers, commit signers, supporters, and all the mailing lists shown in the get_maintainer.pl’s o​​​​​​​utput. Mailing lists are on the “cc” and the rest are on the “To” list when a patch is sent.

-------------------------------------------------------------------------------------------------------------------------------------
scripts/get_maintainer.pl drivers/usb/usbip/usbip_common.c
Valentina Manea <valentina.manea.m@gmail.com> (maintainer:USB OVER IP DRIVER)
Shuah Khan <shuah@kernel.org> (maintainer:USB OVER IP DRIVER)
Greg Kroah-Hartman <gregkh@linuxfoundation.org> (supporter:USB SUBSYSTEM)
linux-usb@vger.kernel.org (open list:USB OVER IP DRIVER)
-------------------------------------------------------------------------------------------------------------------------------------
scripts/get_maintainer.pl drivers/media/usb/au0828/au0828-core.c
Mauro Carvalho Chehab <mchehab@kernel.org> (maintainer:MEDIA INPUT INFRASTRUCTURE (V4L/DVB),commit_signer:7/8=88%,authored:2/8=25%,removed_lines:6/72=8%)
Hans Verkuil <hverkuil-cisco@xs4all.nl> (commit_signer:5/8=62%)
Shuah Khan <shuah@kernel.org> (commit_signer:2/8=25%,authored:2/8=25%,added_lines:150/167=90%,removed_lines:46/72=64%)
Brad Love <brad@nextdimension.cc> (commit_signer:2/8=25%,authored:2/8=25%)
Richard Fontana <rfontana@redhat.com> (commit_signer:1/8=12%)
Sean Young <sean@mess.org> (authored:1/8=12%,removed_lines:6/72=8%)
Thomas Gleixner <tglx@linutronix.de> (authored:1/8=12%,removed_lines:11/72=15%)
linux-media@vger.kernel.org (open list:MEDIA INPUT INFRASTRUCTURE (V4L/DVB))
linux-kernel@vger.kernel.org (open list)
-------------------------------------------------------------------------------------------------------------------------------------

Now let’s run the get_maintainer.pl script on your changes.​

------------------------------------------------------------------------------------------------------------------------------------
scripts/get_maintainer.pl drivers/media/usb/uvc/uvc_driver.c
Laurent Pinchart <laurent.pinchart@ideasonboard.com> (maintainer:USB VIDEO CLASS)
Mauro Carvalho Chehab <mchehab@kernel.org> (maintainer:MEDIA INPUT INFRASTRUCTURE (V4L/DVB))
linux-media@vger.kernel.org (open list:USB VIDEO CLASS)
linux-kernel@vger.kernel.org (open list)
------------------------------------------------------------------------------------------------------------------------------------

At this time, you can run:

git format-patch -1 <commit ID> --to=laurent.pinchart@ideasonboard.com --to=mchehab@kernel.org --cc=linux-media@vger.kernel.org --cc=linux-kernel@vger.kernel.org

This will generate a patch. You can send this patch using:

git send-email <patch_file>

You won’t be sending this patch and you can revert this commit.

### the review process

Your patch will get comments from reviewers with suggestions for improvements and, in some cases, learning to know more about the change itself. Please be patient and wait for a minimum of one week before requesting a response. During merge windows and other busy times, it might take longer than a week to get a response. Also, make sure you sent the patch to the right recipients.

Please thank the reviewers for their comments and address them. Don’t hesitate to ask a clarifying question if you don’t understand the comment. When you send a new version of your patch, add version history describing the changes made in the new version. The right place for the version history is after the "---" below the Signed-off-by tag and the start of the changed file list, as shown in the screenshot below. Everything between the Signed-off-by and the diff is just for the reviewers, and will not be included in the commit. Please don’t include version history in the commit log.

### best practices for sending patches

A few tips and best practices for sending patches:

    Run scripts/checkpatch.pl before sending the patch. Note that checkpatch.pl might suggest changes that are unnecessary! Use your best judgement when deciding whether it makes sense to make the change checkpatch.pl suggests. The end goal is for the code to be more readable. If checkpatch.pl suggests a change and you think the end result is not more readable, don't make the change. For example, if a line is 81 characters long, but breaking it makes the resulting code look ugly, don't break that line.
    Compile and test your change.
    Document your change and include relevant testing details and results of that testing.
    Signed-off-by should be the last tag.
    As a general rule, don't include change lines in the commit log.
    Remember that good patches get accepted quicker. It is important to understand how to create good patches.
    Copy mailing lists and maintainers/developers suggested by scripts/get_maintainer.pl.
    Be patient and wait for a minimum of one week before requesting for comments. It could take longer than a week during busy periods such as the merge windows.
    Always thank the reviewers for their feedback and address them.
    Don’t hesitate to ask a clarifying question if you don’t understand the comment.
    When working on a patch based on a suggested idea, make sure to give credit using the Suggested-by tag. Other tags used for giving credit are Tested-by, Reported-by.
    Remember that the reviewers help improve code. Don’t take it personally and handle the feedback gracefully. Please don’t do top post when responding to emails. Responses should be inlined.
    Keep in mind that the community doesn’t have any obligation to accept your patch. Patches are pulled, not pushed. Always give a reason for the maintainer to take your patch.
    Be patient and be ready to make changes and working with the reviewers. It could take multiple versions before your patch gets accepted. It is okay to disagree with maintainers and reviewers. Please don't ignore a review because you disagree with it. Present your reasons for disagreeing, along with supporting technical data such as benchmarks and other improvements.
    In general, getting response and comments is a good sign that the community likes the patch and wants to see it improved. Silence is what you want to be concerned about. If you don't hear any response back from the maintainer after a week, feel free to either send the patch again, or send a gentle "ping" - something like "Hi, I know you are busy, but have you found time to look at my patch?"
    Expect to receive comments and feedback at any time during the review process.
    Stay engaged and be ready to fix problems, if any, after the patch gets accepted into linux-next for integration into the mainline. Kernel build and Continuous Integration (CI) bots and rings usually find problems.
    When a patch gets accepted, you will either see an email from the maintainer or an automated patch accepted email with information on which tree it has been applied to, and some estimate on when you can expect to see it in the mainline kernel. Not all maintainers might send an email when the patch gets merged. The patch could stay in linux-next for integration until the next merge window, before it gets into Linus's tree. Unless the patch is an actual fix to a bug in Linus's tree, in which case, it may go directly into his tree.
    Sometimes you need to send multiple related patches. This is useful for grouping, say, to group driver clean up patches for one particular driver into a set, or grouping patches that are part of a new feature into one set. git format-patch -2 -s --cover-letter --thread --subject-prefix="PATCH v3" --to= “name” --cc=” name” will create a threaded patch series that includes the top two commits and generated cover letter template. It is a good practice to send a cover letter when sending a patch series.
    Including patch series version history in the cover letter will help reviewers get a quick snapshot of changes from version to version.
    When a maintainer accepts a patch, the maintainer assumes maintenance responsibility for that patch. As a result, maintainers have decision power on how to manage patch flow into their individual sub-system(s) and they also have individual preferences. Be prepared for maintainer-to-maintainer differences in commit log content and sub-system specific coding styles.

##########################################
# Look at which part of this document can be replaced by the kernel doc
Like the best practices and coding standard, for eg.
##########################################

## Kernel and Driver building, loading and dependencies

### compiling a single source

So far, we talked about compiling the entire kernel. Next, let's see how we can build a driver or module or a single source file in the kernel.

Compiling a single source file: make path/file.o:

make drivers/media/test-drivers/vimc/vimc-core.o
  CALL    scripts/checksyscalls.s
  CALL    scripts/atomic/check-atomics.sh
  DESCEND objtool
  CC [M]  drivers/media/test-drivers/vimc/vimc-core.o

Compiling at the directory level: make path:

make drivers/media/test-drivers/vimc/
  CALL    scripts/checksyscalls.sh
  CALL    scripts/atomic/check-atomics.sh  
  DESCEND objtool
  CC [M]  drivers/media/test-drivers/vimc/vimc-core.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-common.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-streamer.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-capture.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-debayer.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-scaler.o
  CC [M]  drivers/media/test-drivers/vimc/vimc-sensor.o
  LD [M]  drivers/media/test-drivers/vimc/vimc.o

The two examples we provided show us how to compile a single source file for the driver vimc, which resides at drivers/media/test-drivers/vimc. You can see how the first make command just compiles the source file and the second one builds the driver. Running make <path> localizes a build to the specified path.

### Compiling a module

Next, let's look at the following variation that builds the vimc module:

make M=drivers/media/test-drivers/vimc
  CC [M] drivers/media/test-drivers/vimc/vimc-core.o
  CC [M] drivers/media/test-drivers/vimc/vimc-common.o
  CC [M] drivers/media/test-drivers/vimc/vimc-streamer.o
  CC [M] drivers/media/test-drivers/vimc/vimc-capture.o
  CC [M] drivers/media/test-drivers/vimc/vimc-debayer.o
  CC [M] drivers/media/test-drivers/vimc/vimc-scaler.o
  CC [M] drivers/media/test-drivers/vimc/vimc-sensor.o
  LD [M] drivers/media/test-drivers/vimc/vimc.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC drivers/media/test-drivers/vimc/vimc.mod.o
  LD [M] drivers/media/test-drivers/vimc/vimc.ko

Sometimes, it is hard to figure out all the dependencies for a module, or a driver, or a configuration option. Until all the dependencies are enabled, the driver you are looking to enable will not be enabled.

Let’s take a look at drivers/media/test-drivers/vimc/Kconfig.

config VIDEO_VIMC
    tristate "Virtual Media Controller Driver (VIMC)"
    depends on VIDEO_DEV && VIDEO_V4L2 && VIDEO_V4L2_SUBDEV_API
    select VIDEOBUF2_VMALLOC
    select VIDEO_V4L2_TPG
    help
     Skeleton driver for Virtual Media Controller

     This driver can be compared to the vivid driver for emulating
     a media node that exposes a complex media topology. The topology
     is hard coded for now but is meant to be highly configurable in
     the future.

     When in doubt, say N.

We can see that vimc can be enabled by changing the CONFIG_VIDEO_VIMC option. It is a tristate driver. What that means is that it can be:

    enabled as a built-in
    enabled as a module 
    disabled.

It depends on CONFIG_VIDEO_DEV, CONFIG_VIDEO_V4L2, and CONFIG_VIDEO_V4L2_SUBDEV_API to be enabled. It will also autoselect CONFIG_VIDEOBUF2_VMALLOC and CONFIG_VIDEO_V4L2_TPG.

    Enable as a module: CONFIG_VIDEO_VIMC=m
    Enable as built-in: CONFIG_VIDEO_VIMC=y
    Disable: CONFIG_VIDEO_VIMC=n or #CONFIG_VIDEO_VIMC

Some options are boolean. That means these modules or options can be enabled or disabled. It might take a couple of attempts to enable all the dependencies. We recommend using make menuconfig to enable drivers and other configuration options.

 

Kernel Configuration - make menuconfig

 

Vimc resides under the Device Drivers option. Using the down arrow, you can navigate to the Device Drivers option and take a look at what there is in there. You can use the "/" option to search. We are showing the long road to give you more details on the configuration hierarchy.

 

menuconfig Device Drivers

 

Now navigate down until you see Multimedia support and then follow the Media test drivers option. You will finally see vimc there.

 

menuconfig_vimc

 

In our configuration, we have it enabled as a module. If you would like to change it, scroll down and this will highlight the M, at which point you can change it by just pressing Enter, which will toggle through all three options for this driver. That’s enough fun with menuconfig for now. We will leave it to you to play with other options.



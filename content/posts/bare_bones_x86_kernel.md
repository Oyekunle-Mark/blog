---
title: "Writing a Bare Bones x86 Kernel"
date: 2024-04-27
description: "Writing a Bare Bones x86 Kernel"
summary: "In this tutorial we will write a simple kernel for 32-bit x86 and boot it."
tags: ["osdev", "C"]
draft: true
---

My interest was piqued by operating systems recently and I have been spending more and more time learning how they work and how they are built. After working my way through most of the xv6 labs[^1], I decided to invest time reading and trying out the tutorials on [osdev wiki](https://wiki.osdev.org/Main_Page) because I wanted to find my own way without the guard rails provided by the xv6 course. This article is the result of my trying out the [Bare Bones tutorial](https://wiki.osdev.org/Bare_Bones) on the wiki.

## Building your Cross-Compiler

You can not use the C compiler on your host operating system to compile the code here. It will build for your host and not for our target architecture. You will have to build a GCC cross-compiler for the **i686-elf** target. [This tutorial](https://wiki.osdev.org/GCC_Cross-Compiler) will help you do that if you don't have one installed on your machine already.

## The Code

For the minimal kernel we will be writing, we will end up with these files at the end of this article:

```bash
.
├── boot.s
├── kernel.c
└── linker.ld
```

**boot.s**: x86 assembly to start up the kernel and setup the stack
**kernel.c**: Main kernel code in C that uses VGA text mode[^2] to write to the screen
**linker.ld**: Linker script for setting up the final ELF[^3] file and placing the Multiboot[^4] header in place in the final kernel image.

All the code that will be shared will be heavily commented to make them self-explanatory. Additional explanation will be provided under each code block to provide link to specifications that explains key concepts.

### boot.s

```assembly
// boot.s file gets inserted here
```

The [Multiboot Specification](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html) describes the mutltiboot headers and how to place them. I recommend you read that document.

### kernel.c

```c
// kernel.c file gets inserted here
```

We don't have access to the C standard library since we will be compiling our code in *freestanding*. We do have access to a few headers for fixed-width integers, which allows us to use the two includes above. 
The [VGA text mode wikipeadia page](https://en.wikipedia.org/wiki/VGA_text_mode) is a useful read.

### linker.ld

```text
/* place linker script here */
```

The link scripts allows us to explicitly define how the final kernel executable should be built. We can specify alignment, address offset and sections of the output file. The [GNU Linker](https://ftp.gnu.org/old-gnu/Manuals/ld-2.9.1/html_chapter/ld_3.html) documentation on the ld command language is a recommended read for understanding link scripts.

## Compiling and Linking

How you invoke your cross-compiler might be different based on how you install it. So modify the commands in this section to use the right cross-compiler invocation.

We start by assembling the *boot.s* file with:

```bash
$HOME/opt/cross/bin/i686-elf-as boot.s -o boot.o
```

Next, compile the *kernel.c* file using:

```bash
$HOME/opt/cross/bin/i686-elf-gcc -std=gnu99 -ffreestanding -O2 -Wall -Wextra -c kernel.c -o kernel.o
```

Now, we will link the executables into a final kernel image using the linker script with:

```bash
$HOME/opt/cross/bin/i686-elf-gcc -ffreestanding -nostdlib -T linker.ld boot.o kernel.o -o my_kernel.elf -lgcc
```

*my_kernel.elf* is our final kernel image.

### Verifying Multiboot

If you have GRUB[^5] installed, you can check whether your *my_kernel.elf* has a valid Multiboot header with:

```bash
grub2-file --is-x86-multiboot my_kernel.elf
```

That command returns a *0* exit code on success and *1* on failure. You can view exit code of the last shell command using:

```bash
echo $?
```

## Running the Kernel

We will be using QEMU[^6] for this. The *-kernel* option to QEMU allows us to specify an ELF executable(like our *my_kernel.elf* file) that is multiboot compliant and will boot from it. So, boot your new-fangled kernel with:

```bash
qemu-system-i386 -kernel my_kernel.elf
```

You should see something like this:

![screen shot of the kernel printing the welcome message]()

Congratulations!!!

[^1]: point to xv6's source
[^2]: vga text mode
[^3]: elf
[^4]: multiboot spec
[^5]: grub
[^6]: qemu

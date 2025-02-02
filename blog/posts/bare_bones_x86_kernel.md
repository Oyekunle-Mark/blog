---
title: "Writing a Bare Bones x86 Kernel"
date: 2024-04-27
description: "Writing a Bare Bones x86 Kernel"
summary: "In this tutorial, we will write a simple kernel for 32-bit x86 and boot it."
tags: ["osdev"]
draft: false
---

My interest was piqued by operating systems recently and I have been spending more and more time learning how they work and how they are built. After working my way through most of the [xv6 labs](https://pdos.csail.mit.edu/6.828/2023/xv6.html), I decided to invest time reading and trying out the tutorials on [osdev wiki](https://wiki.osdev.org/Main_Page) because I wanted to find my way without the guard rails provided by the xv6 course. This article is the result of my trying out the [Bare Bones tutorial](https://wiki.osdev.org/Bare_Bones) on the wiki.

## Building your Cross-Compiler

You can not use the C compiler on your host operating system to compile the code here. It will be built for your host and not for our target architecture. You will have to build a GCC cross-compiler for the **i686-elf** target. [This tutorial](https://wiki.osdev.org/GCC_Cross-Compiler) will help you do that if you don't have one installed on your machine already.

## The Code

For the minimal kernel we will be writing, we will end up with these files at the end of this article:

```bash
.
├── boot.s
├── kernel.c
└── linker.ld
```

**boot.s**: x86 assembly to start the kernel and set up the stack.

**kernel.c**: Main kernel code in C that uses [VGA Text Mode](https://en.wikipedia.org/wiki/VGA_text_mode) to write to the screen.

**linker.ld**: Linker script for setting up the final [ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) file and placing the [Multiboot](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html) header in the final kernel image.

All the code that will be shared will be heavily commented on to make them self-explanatory. Additional explanations will be provided under each code block to provide links to specifications that explain key concepts.

### boot.s

```asm
/*
An OS image must contain an additional header called Multiboot header, besides the headers of the format used by the OS image.
The Multiboot header must be contained completely within the first 8192 bytes of the OS image, and must be longword (32-bit) aligned.
In general, it should come as early as possible, and may be embedded in the beginning of the text segment after the real executable header.
*/
.set MULTIBOOT_MAGIC, 		0x1BADB002 // The field ‘magic’ is the magic number identifying the header, which must be the hexadecimal value 0x1BADB002.
.set MULTIBOOT_ALIGN, 		1 << 0
.set MULTIBOOT_MEMINFO, 	1 << 1
.set MULTIBOOT_FLAGS,		MULTIBOOT_ALIGN | MULTIBOOT_MEMINFO // The field ‘flags’ specifies features that the OS image requests or requires of an boot loader
.set MULTIBOOT_CHECKSUM,	(0 -(MULTIBOOT_MAGIC + MULTIBOOT_FLAGS)) // The field ‘checksum’ is a 32-bit unsigned value which, when added to the other magic fields (i.e. ‘magic’ and ‘flags’), must have a 32-bit unsigned sum of zero.

// section for the magic fields of Multiboot header
.section .multiboot
.align 4
.long MULTIBOOT_MAGIC
.long MULTIBOOT_FLAGS
.long MULTIBOOT_CHECKSUM

.section .bss
.align 16 // x86 required a 16-bytes aligned stack
stack_bottom:
	.skip 4096 // reserve 4kb for the stack
stack_top:

.section .text
.global start
// starting point of our kernel
start:
	/*
	We must first setup the stack. To do that, we set a value for *%esp* register, the stack pointer
	On x86, the stack grows downward.
	*/
	mov $stack_top, %esp

	// call the *kernel_main* function we will write later in *kernel.c*.
	call kernel_main

// we shouldn't return from *kernel_main*, if we do, we will hang up the CPU
loop:
	cli // disables CPU interrupts
	hlt // halt
	jmp loop // if we do end up here, loop back
```

The [Multiboot Specification](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html) describes the multiboot headers and how to place them. I recommend you read that document.

### kernel.c

```c
#include <stddef.h>
#include <stdint.h>

/* Check if the compiler thinks you are targeting the wrong operating system. */
#if defined(__linux__)
	#error "This program is not being compiled with a cross-compiler"
#endif

/* This tutorial will only work for the 32-bit ix86 targets. */
#if !defined(__i386__)
	#error "This program is meant to target ix86"
#endif

// VGA text mode console is 80 columns by 25 rows
const size_t VGA_ROWS = 25;
const size_t VGA_COLS = 80;

// The VGA text buffer is located at physical memory address 0xB8000
uint16_t* vga_buffer = (uint16_t*)0xB8000;

size_t row_index = 0;
size_t col_index = 0;

// uint8_t VGA_COLOR_BLACK = 0;
// uint8_t VGA_COLOR_WHITE = 15;
// we are shifting the backgroud color left by 4 and bit ORing with the foregroud color
uint8_t terminal_color = 0 << 4 | 15;

/**
 * terminal_initialize clears the entire screen
 * by writing blank, the space character
 */
void terminal_initialize()
{
	for(size_t col = 0; col < VGA_COLS; col++)
	{
		for(size_t row = 0; row < VGA_ROWS; row++)
		{
			const size_t index = (VGA_COLS * row) + col;
			// shift terminal color to it's place and set the character code point to blank
			vga_buffer[index] = ((uint16_t)terminal_color << 8) | ' ';
		}
	}
}

/**
 * terminal_write_char writes a single character to the terminal.
 * Accounts for newlines
 */
void terminal_write_char(char c)
{
	switch(c)
	{
		case '\n':
		{
			col_index = 0;
			row_index++;
			break;
		}
		default:
		{
			const size_t index = (VGA_COLS * row_index) + col_index;
			vga_buffer[index] = ((uint16_t)terminal_color << 8) | c;
			col_index++;
			break;
		}
	}

	if (col_index == VGA_COLS)
	{
		col_index = 0;
		row_index++;
	}

	if (row_index == VGA_ROWS)
	{
		row_index = 0;
		col_index = 0;
	}
}

/**
 * terminal_write_string writes each character in the
 * string to the terminal.
 */
void terminal_write_string(const char* str)
{
	for(size_t i = 0; str[i] != '\0'; i++)
		terminal_write_char(str[i]);
}

void kernel_main()
{
	terminal_initialize();

	terminal_write_string("Hello, world!\n");
	terminal_write_string("This is my first kernel. :)\n");
}
```

We don't have access to the C standard library since we will compile our code in *freestanding*. We have access to a few headers for fixed-width integers, which allows us to use the two includes above. 
The [VGA text mode Wikipedia page](https://en.wikipedia.org/wiki/VGA_text_mode) is a recommended read.

### linker.ld

```ld
/* Our designated starting point. The symbol created in *boot.s*. The bootloader will begin execution here*/
ENTRY(start)

SECTIONS
{
	/* start placing sections at 1 MB */
	. = 1M;

	/* all sections are 4 kb aligned to accomodate paging later on */
	/* place multiboot header first followed by read only data */
	.rodata BLOCK(4K) : ALIGN(4K)
	{
		*(.multiboot)
		*(.rodata)
	}

	/* executable code */
	.text BLOCK(4K) : ALIGN(4K)
	{
		*(.text)
	}

	/* initialized data */
	.data BLOCK(4K) : ALIGN(4K)
	{
		*(.data)
	}

	/* uninitialzed data and stack */
	.bss BLOCK(4K) : ALIGN(4K)
	{
		*(COMMON)
		*(.bss)
	}
}
```

The linker script allows us to explicitly define how the final kernel executable should be built. We can specify alignment, address offset and sections of the output file. The [GNU Linker](https://ftp.gnu.org/old-gnu/Manuals/ld-2.9.1/html_chapter/ld_3.html) documentation on the ld command language is a recommended read for understanding link scripts.

## Compiling and Linking

How you invoke your cross-compiler may differ based on how you installed it. So, update the commands in this section to use the appropriate cross-compiler invocation.

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

If you have [GRUB](https://www.gnu.org/software/grub/) installed, you can check whether your *my_kernel.elf* has a valid Multiboot header with:

```bash
grub2-file --is-x86-multiboot my_kernel.elf
```

That command returns a *0* exit code on success and *1* on failure. You can view the exit code of the last shell command using:

```bash
echo $?
```

## Running the Kernel

We will be using [QEMU](https://www.qemu.org/) for this. The *-kernel* option to QEMU allows us to specify an ELF executable(like our *my_kernel.elf* file) that is multiboot compliant and will boot from it. So, boot your new-fangled kernel with:

```bash
qemu-system-i386 -kernel my_kernel.elf
```

You should see something like this:

![screenshot of the kernel printing the welcome message](https://i.imgur.com/elD5Iz5.png)

Congratulations!!!

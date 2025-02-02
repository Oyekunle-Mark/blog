---
title: "Run a Command at Interval, Unintrusively"
date: 2024-02-20
description: "Run a Command at Interval, Unintrusively"
summary: "A not so uncommon usecase is needing to run a command repeatedly at fixed intervals, without losing control of your shell. Doing this in the Linux shell is particularly trivial."
draft: false
tags: ["terminal"]
---

A not so uncommon usecase is needing to run a command repeatedly at fixed intervals, without losing control of your shell.
Doing this in the Linux shell is particularly trivial.

I have two quick options for going about this operation:

1. Use job control to run the command in the background
2. Use tmux to view the stdout(and/or stderr) of the command by attaching to the session and detaching when you don't have a need to view the logs.

In these, two cases, I prefer the added option of writing to a log file. This allows me examine what the process has been up to.

Let us pretend we wish to run the `date` command every **10s**

## Job Control

We will pipe stdout and stderr to `/dev/null` so they don't get mixed up messages from foreground processes.

```sh
watch -n 10 'date | tee -a output.txt' &>/dev/null &
```
This runs the date command every ten seconds in the background while appending the output to `output.txt` and swallowing writes to stdout and stderr.

## tmux

If you prefer to view the output of the command interactively, you can use [tmux](https://en.wikipedia.org/wiki/Tmux).

This is my preferred option, as I can attach to the session whenever I want see how things are moving on and detach when done.
If you aren't familiar with tmux, theres at least a billion useful articles online about what it is and how to use it.

The command in this case will not redirect stdout and stderr to `/dev/null`.

```sh
watch -n 10 'date'
```

---
title: "Keeping config files in sync with git"
date: 2024-04-06
description: "Keeping config files in sync with git"
summary: "With my workflow favouring the terminal over GUI-based development tools, my config files for the common terminal utilities I use daily have been growing as I build proficiency in Vim and Tmux. In this article, I will show you how I use git to keep my config files in sync across machines."
draft: false
tags: ["config", "terminal"]
---

<mark>**NOTE:**</mark>This article, and the code in the shared GitHub repository, have been superseded by changes described in this [follow up article]({{< ref "/posts/multi-environment-configuration-files-management.md" >}}).

Until 2024, I didn't have a big need to customise terminal commands and utilities. I used Visual Studio Code heavily, its CLI interface was good enough for me when I needed to use the terminal. My choice to switch to a more terminal-native environment has led me to learn how to be comfortable with Vim and Tmux, and I use these tools both for work and personal use now.

With that decision has also come the need to customize them, via config files, to my taste. Sharing these config files between my work and personal computers(or any other machine for that matter) has led me to check them into git, and devise a git workflow for keeping them in sync across the machines I develop on.

## The config files

The config files are checked into git and pushed to a [GitHub repository](https://github.com/Oyekunle-Mark/dotfiles/tree/master). At the time of writing this article, I have config files for [vim](https://github.com/Oyekunle-Mark/dotfiles/blob/master/.vimrc), [tmux](https://github.com/Oyekunle-Mark/dotfiles/blob/master/.tmux.conf) and [zsh](https://github.com/Oyekunle-Mark/dotfiles/blob/master/.zshrc). The GitHub repository can be considered the single source of truth for every machine that pulls its config from that repository.

## Workflow

### On a new machine

Setting up config files on a new machine includes:

1. Cloning the repository into `$HOME/my_works`. I keep all my development projects in a `$HOME/my_works` folder as a matter of habit. You can choose to put this anywhere in your file system that suits you, you just have to account for the change in path if you will be copying commands from this article.

```sh
cd ~/my_works && git clone https://github.com/Oyekunle-Mark/dotfiles.git
```

2. Create symbolic links from the config files in my home directory to the files in the `dotfiles` folder cloned above. For example, to create a symbolic link for a vim config file, I use this command:

```sh
ln -nfs $HOME/my_works/dotfiles/.vimrc $HOME/.vimrc
```

Alternatively, I have a [setup_dotfiles.sh](https://github.com/Oyekunle-Mark/dotfiles/blob/master/setup_dotfiles.sh) in the repository to create all the links and perform other setup actions required. Executing this script saves me a few keystrokes.

### Keeping them in sync

To make it possible to pull the latest config from anywhere in the file path, I have this alias in my `.zshrc`:

```sh
alias dot_g='/usr/bin/git --git-dir=$HOME/my_works/dotfiles/.git --work-tree=$HOME/my_works/dotfiles'
```

#### Update on one machine

After making an update to a config file(s), I can use

```sh
dot_g commit -am "<commit message>"
dot_g push
```

#### On another machine

```sh
dot_g pull
```

From anywhere update the config files.

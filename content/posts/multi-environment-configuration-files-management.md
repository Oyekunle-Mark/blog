---
title: "An Even More Flexible Config File Management Technique"
date: 2024-05-18
description: "Manage configuration files across many machines easily."
summary: "Config files are often strongly coupled to the machine they reside on. This create a need to have the configuration setup vary from machine to machine. I will be writing about how I have revamped my config workflow to accomodate this specific need."
draft: true
tags: ["config", "terminal"]
---

I had a basic system of sharing config files across the machines I work on. I have written about how I use a [simple git workflow]({{< ref "/posts/keep-configs-in-sync.md" >}}) to share the same files on different machines along with a tiny scripts to make setting up new machines easy.

That system ran into a wall recently. The main pain points of the old method were:
1. There were utilities I use on one machine I do not use on the other. My ultra minimalist mindset wants to have the config for the utilities I use on each machine and nothing more
2. There are frequently cases where, configs vary on different machines. A common example is having some aliases for internal tools I use at my 9 to 5 but do not use anywhere else or some initialization script in my `.zshrc` for utilities that does not exist on another machine.
3. Sensitive information cannot be added because the config files are checked into git.

Those 3 limitations acted as the requirement that the new changes had to deliver. Along with not using any other specific tool, or programming language that doesn't come preinstalled on Unix and Unix-like computers. I want to keep the old simplicity of installing git, pulling the config repositories, executing a script, and being ready to go on any machine after a clean install.

With the requirements established, I will now describe the new system, its usage, and how it solve the problems with the old method. This [Github repository](https://github.com/Oyekunle-Mark/dotfiles) is where you will find the code being described in this article.

## Building config files with environment awareness

Adding a utility requires adding a new folder for the utility. To onboard a utility `xyz`, you have to do following:
1. Add a `xyz` folder
2. Add a `common` file to the new folder. The *common* file is where you add the configurations you want to be shared across every machine for this utility.
3. Add a `.private` file to the folder. This is the file you add the configurations that are sensitive, such as personal identyfying data. The file is git ignored, so it's content will only ever stay on this machine.
4. Register the utility in `setup_dotfiles.sh` to build the config for the utility.

You will end up with this structure:

```sh
oye@pc ~/my_works/blog % lt -a xyz
xyz
├── common
├── game_machine
└── .private

1 directory, 3 files
```

All the magic happen in `setup_dotfiles.sh`. Most utilities are registered by adding this line to the script:

```sh
build_file xyz $1 ~/.xyzrc
```

Where `xyz` is the folder the configs were added to in steps 1-3 above, and `~/.xyzrc` is the file we want as output.

`$1` in the snippet plays a different role. It is the environment where we are executing this script from. Let's imagine that we are on a machine we refer to as *game_machine*, we will initiaze all our configs with:

```sh
./setup_dotfiles.sh game_machine
```

`$1` will be *game_machine*.

If `xyz` has been registered as described above, and `setup_dotfiles.sh` is executed as described, it follows the following logic to build the config file for the utility:
1. Truncates `~/.xyzrc` if it exists, otherwise, creates a new empty one.
2. Checks if there is a `xyz/common` file. If there is, it merges it into `~/.xyzrc`. 
3. Checks for a `xyz/game_machine` file. If there is, it merges it into `~/.xyzrc`.
4. Checks if a `xyz/.private` file exists and merges it into `~/.xyzrc`.

What this means is that, for any utility I want configuration provided for, I can:
1. Provide a base configuration that should be present on every machine in `common`. This is used for those utilities that is a stable no matter the device I am using. Most of the time, this is the only file to add because the files do not change across machines.
2. This allows me add configuration that are specific to a machine, by using. Or if it is a utility I do not use on all my machines, I just provide a file matching the environment name I will be passing to `setup_dotfiles.sh`. This allows me vary the generated config file based on a machine, or even have a config file generated on a machine and not on another. As many environment specific file can be added as environment using this repository to build configs.
3. Have sensitive information in the config file, by using `.private`, which doesn't have to make it into git and is isolated to where the file is added.

All files are optional, which means you only create what you need, and `setup_dotfiles.sh` only build what your environment only needs.

## A demonstration

At the time of writing this, the content of the repository looks like this:

```sh
oye@pc ~/my_works/dotfiles % tree -a -I .git
.
├── .gitignore
├── README.md
├── setup_dotfiles.sh
├── tmux
│   └── common
├── vim
│   └── common
└── zsh
    ├── common
    ├── pc_linux
    └── work

4 directories, 8 files
```

On my PC, running Debian, I have dubbed the environment *pc_linux*. I setup my configs with:

```sh
oye@pc ~/my_works/dotfiles % ./setup_dotfiles.sh pc_linux

Building config files for the pc_linux environment...


Building /home/oye/.zshrc...

Merging ./zsh/common into /home/oye/.zshrc...
Merging ./zsh/pc_linux into /home/oye/.zshrc...
Could not find a .private file in ./zsh. Skipping...
/home/oye/.zshrc built successfully.


Building /home/oye/.tmux.conf...

Merging ./tmux/common into /home/oye/.tmux.conf...
Could not find the ./tmux/pc_linux environment specific file. Skipping...
Could not find a .private file in ./tmux. Skipping...
/home/oye/.tmux.conf built successfully.


Building /home/oye/.vimrc...

Merging ./vim/common into /home/oye/.vimrc...
Could not find the ./vim/pc_linux environment specific file. Skipping...
Could not find a .private file in ./vim. Skipping...
/home/oye/.vimrc built successfully.


All config files have been built for the pc_linux environment. Enjoy :)
```

You can see the tool reports what it uses, and ignores as it generates each utilities config file.

Updates are checked into *git* and kept in sync across machines by push and pulls to the remote repository.

## Conclusion

The current setup described satisfies my current usecases. It will be interesting to see how long that lasts until it becomes obsolete and how I evolve the repository while keeping to my principle of not using more complex tools than I need.

While there are a number of tools out there for managing config files, this bespoke solution allows me to scratch my own itch, and needs just a git installation(if it already did not exist) on any machine to get up and running.

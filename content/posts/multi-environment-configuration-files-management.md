---
title: "Multi Environment Config Files Management"
date: 2024-05-01
description: "Manage configuration files across many machines easily."
summary: "Maintaining the same configuration files across machines is against the reason for using different machines. Which is that, the different environments have their own perculiarities and scripts. I will be writing about how I have revamped my config workflow to accomodate this specific need."
draft: true
tags: ["config", "terminal"]
---

old capabilies:
1. use git as a source of truth
2. aliases for updating and the syncing the files on any machine
3. basic helper to setup the config files, which involves creating sym links to the actual files.

new usecase:
1. enter machine specific config entries that doesn't pollute the config files on other machines.
2. have the same git driven worklow
3. accomodate adding new configuration files without making a code change

structure:

.config_setup.sh # file, git ignored, provides value for
env: env1
utilities: util1,util2 # list of all the config files to be built for this environment 

util1/  # for each terminal utility requiring config files
    common # will be present in all environments
    env1 # will be present  on machine where env is set to 'env1' in the .config_setup file
    .private # not checked into git, will contain sensitive information we want on our local machine alone
    setup # script to setup the config file for the utility. like creating the folders in the right path and sym linking
util2/ # same as above
    ...
    ...
build.sh # build the config files for this environment.
init.sh # first time setup of aliases required to add path to git dir. Can use realpath "$0". Should call build.sh to finish setup

Does:
1. reads and parses .config_setup
2. optionally builds the config files for all utilities this environment needs by:
    a. reading common
    b. reading a file with the same env name and merging with common
    c. reading the .private file, if one exist, and merging with the result from [b] above.
    d. executes setup script for each utility
3. [init.sh] adds the aliases to make syncing the config files and building them easy from any location
4. prints descriptive messages before, during and after setup

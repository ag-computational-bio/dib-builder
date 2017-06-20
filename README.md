# dib-builder

The dib-builder is a collection of scripts that build and deploy cloud images based on a configuration file.

## Proposed structure of a image source repository

* config.yml 

~~~~yaml
# The name of the cloud image will be created from the name and the version.
name: docker
version: 1.0.0
maintainers: [Lukas Jelonek - lukas.jelonek@computational.bio.uni-giessen.de]

# The description will be used for generated websites
description: An ubuntu image that contains a ready to use docker daemon
# A list of installed tools worth mentioning.
# Will be used as documentation, e.g. on a homepage
tools: [docker]

# A list of tags to classify images.
tags: [server, docker]

# Information needed for the execution of diskimage-builder
dib:
    # architecture of the image
    architecture: amd64
    # list of elements to include in the image
    elements: [ubuntu, vm, latest-docker]
    # package names that should be installed, -p in dib
    packages: []

# Information needed for image deployment
deploy:
    # RAM requirements in MB
    min_ram: 512
    # Disk requirements in GB
    min_hd: 4
~~~~

* elements - git subrepository to dib elements source
* dib-builder - git subrepository to this Project
* .gitignore

~~~~
target/
~~~~

* .gitlab-ci.yml 

~~~~yaml
before_script:
    - git submodule sync --recursive
    - git submodule update --init --recursive

stages:
    - build

build:
    stage: build
    tags:
        - dib
        - cloud
    script:
        - ./build.py
~~~~

* README.md - A technical documentation of the image

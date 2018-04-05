dib-builder
===========

The dib-builder is an abstraction on top of the diskimage builder. It adds a
simple config file for image definition, including additional metadata like
maintainers, versioning and so on. It comes with two commands:

* dibt-build - builds the image
* dibt-deploy - uploads the build image to an openstack project


Installation
------------

Installation, including all dependencies works via pip::

    git clone git@git.computational.bio.uni-giessen.de:deNBI-Cloud/dib-builder.git
    cd dib-builder
    pip3 install .


Usage
-----

To build an image, go to the directory containing the config.yaml file and
execute::

  dibt-build

The resulting image will be stored in the `target/` subdirectory.

To deploy an image, load the openrc file for your cloud project, go to the
directory containing the config.yaml, build it and then execute::

  dibt-build

The image will be uploaded and several properties will be set, based on the
contents of the config.yaml file.


Structure an image definition
-----------------------------

* elements directory containing all additional elements to include into the
  diskimage builder build
* config.yaml::

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

Proposed CI process for gitlab
-------------------

Create .gitlab-ci.yml 

::
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
            - dibt-build
            - dibt-deploy

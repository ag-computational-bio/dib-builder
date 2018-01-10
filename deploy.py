#!/usr/bin/env python3
import argparse
import os
import yaml
import sys
from subprocess import call

## deploys an image with the openstack client
## the openstack cloudrc must be run outside of this script

# parse arguments
parser = argparse.ArgumentParser(description='Deploy a build image')
parser.add_argument('-c', '--config', default='config.yaml')
args = parser.parse_args()
output_directory='target'

# read yaml
stream = open(args.config, 'r')
config = yaml.load(stream)

# check mandatory fields
mandatory_fields = ['name', 'version', ['deploy','min_ram'], ['deploy', 'min_hd'], 'maintainers']
for field in mandatory_fields:
    if isinstance(field, list):
        if not config[field[0]][field[1]]:
            raise Exception("Mandatory field '"+field[0] +"."+field[1]+"' not specified in config file")
    else:
        if not config[field]:
            raise Exception("Mandatory field '"+field+"' not specified in config file")

# build commandline
image_name = config['name'] + '-' + config['version']
image_file = 'target/' + image_name + '.qcow2'
ram = config['deploy']['min_ram']
hdd = config['deploy']['min_hd']
maintainers = config['maintainers']

cli = 'openstack image create --disk-format qcow2 --file ' + image_file
if ram:
    cli += ' --min-ram ' + str(ram)
if hdd:
    cli += ' --min-disk ' + str(hdd)
if maintainers:
    cli += ' --property maintainers="' + str.join(',',maintainers) + '"'

cli += ' ' + image_name

sys.stderr.write("Executing: " + cli + "\n")
sys.exit(os.system(cli))

#!/usr/bin/env python3
import argparse
import os
import yaml
import sys
from subprocess import call

sys.stderr.write("Starting build...\n")

# parse arguments
parser = argparse.ArgumentParser(description='Build image from configuration yaml file')
parser.add_argument('-c', '--config', default='config.yaml')
args = parser.parse_args()
output_directory='target'

sys.stderr.write("reading file...\n")
# read yaml
stream = open(args.config, 'r')
config = yaml.load(stream)

# check mandatory fields
mandatory_fields = ['name', 'version', ['dib','architecture'], ['dib', 'elements']]
for field in mandatory_fields:
    if isinstance(field, list):
        if not config[field[0]][field[1]]:
            raise Exception("Mandatory field '"+field[0] +"."+field[1]+"' not specified in config file")
    else:
        if not config[field]:
            raise Exception("Mandatory field '"+field+"' not specified in config file")

sys.stderr.write("building command...\n")
# build commandline
image_name = config['name'] + '-' + config['version'] + '.qcow2'
architecture = config['dib']['architecture']
elements = config['dib']['elements']
packages = config['dib']['packages']

cli = 'disk-image-create'
if architecture:
    cli += ' -a ' + architecture

cli += ' -o ' + output_directory + '/' + image_name
if packages:
    cli += ' -p '
    cli += ','.join(packages)

#import elements
call(["git", "submodule","init"])
call(["git", "submodule","update"])

if elements:
    for e in elements:
        cli += ' ' + e


sys.stderr.write("setting environment variable...\n")
# Execute diskimage builder
if 'ELEMENTS_PATH' in os.environ:
    os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements:' + os.environ['ELEMENTS_PATH']
else:
    os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements'
    
os.environ["LANG"] = "en_US.UTF-8"

sys.stderr.write("Executing: " + cli + "\n")
sys.exit(os.system(cli))

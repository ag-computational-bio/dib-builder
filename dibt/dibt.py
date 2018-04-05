#!/usr/bin/env python3
import argparse
import os
import yaml
import sys
from subprocess import call
import datetime

def readconfig(file):
  if os.path.exists(file):
    sys.stderr.write("reading file...\n")
    # read yaml
    with open(file, 'r') as stream:
      config = yaml.load(stream)
      return config
  else:
    raise Exception("Config file not found\n")

def check_mandatory_fields(config, fields):
  for field in fields:
    if isinstance(field, list):
        if not config[field[0]][field[1]]:
            raise Exception("Mandatory field '"+field[0] +"."+field[1]+"' not specified in config file")
    else:
        if not config[field]:
            raise Exception("Mandatory field '"+field+"' not specified in config file")

def create_build_commandline(config, target):
  sys.stderr.write("building command...\n")
  # build commandline
  image_name = config['name'] + '-' + config['version'] + '.qcow2'
  architecture = config['dib']['architecture']
  elements = config['dib']['elements']
  packages = config['dib']['packages']

  cli = 'disk-image-create'
  if architecture:
      cli += ' -a ' + architecture

  cli += ' -o ' + target + '/' + image_name
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
  if os.path.isdir(os.getcwd() + '/elements'):
    if 'ELEMENTS_PATH' in os.environ:
        os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements:' + os.environ['ELEMENTS_PATH']
    else:
        os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements'
      
  os.environ["LANG"] = "en_US.UTF-8"
  return cli

def create_deploy_commandline(config, target):
  # build commandline
  now = datetime.datetime.now()
  image_name = config['name'] + '-' + config['version']
  image_file = 'target/' + image_name + '.qcow2'
  ram = config['deploy']['min_ram']
  hdd = config['deploy']['min_hd']
  maintainers = config['maintainers']

  cli = 'openstack image create --disk-format qcow2 --file ' + image_file
  cli += ' --property version="' + config['version'] + '"'
  cli += ' --property image_name="' + config['name'] + '"'
  cli += ' --property upload_date="' + now.isoformat() + '"'
  if ram:
      cli += ' --min-ram ' + str(ram)
  if hdd:
      cli += ' --min-disk ' + str(hdd)
  if maintainers:
      cli += ' --property maintainers="' + str.join(',',maintainers) + '"'
  if 'OS_USERNAME' in os.environ:
      uploader = os.environ['OS_USERNAME']
      cli += ' --property uploader="' + uploader + '"'
  if 'description' in config:
      cli += ' --property description="'+ config['description'] +'"'
  if 'tags' in config:
      for tag in config['tags']:
          cli += ' --tag "' + tag + '"'

  cli += ' "' + image_name + ' (' + now.strftime("%Y-%m-%d") + ')"'
  return cli

def execute_command_line(cli):
  sys.stderr.write("Executing: " + cli + "\n")
  sys.exit(os.system(cli))

def _generate_default_parser():
  parser = argparse.ArgumentParser(description='Build image from configuration yaml file')
  parser.add_argument('-c', '--config', default='config.yaml')
  parser.add_argument('-o', '--output', default='target')
  return parser

def build():
  # parse arguments
  parser = _generate_default_parser()
  args = parser.parse_args()

  config = readconfig(args.config)
  check_mandatory_fields(config, ['name', 'version', ['dib','architecture'], ['dib', 'elements']])
  cli = create_build_commandline(config, args.output)
  execute_command_line(cli)

def deploy():
  # parse arguments
  parser = _generate_default_parser()
  args = parser.parse_args()

  config = readconfig(args.config)
  check_mandatory_fields(config, ['name', 'version', ['deploy','min_ram'], ['deploy', 'min_hd'], 'maintainers'])
  cli = create_deploy_commandline(config, args.output)
  execute_command_line(cli)

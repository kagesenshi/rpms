#!/usr/bin/python3

import argparse
import yaml
import os
import sys
import subprocess
import semver
import hashlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _c(color, t):
    c = getattr(bcolors, color.upper())
    return "%s%s%s" % (c, t, bcolors.ENDC)

parser = argparse.ArgumentParser()
parser.add_argument('-p','--push', default=False, action='store_true')
parser.add_argument('-c','--containerfile', default=None)
parser.add_argument('--cmd', required=False, default='docker')
parser.add_argument('directory')


args = parser.parse_args()

if args.containerfile is None:
    if os.path.exists('Containerfile'):
        containerfile = 'Containerfile'
    elif os.path.exists('Dockerfile'):
        containerfile = 'Dockerfile'
    else:
        raise AssertionError('Unable to locate Containerfile or Dockerfile')
else:
    containerfile = args.containerfile
    if not os.path.exists(containerfile):
        raise AssertionError('Unable to locate %s' % containerfile)

os.chdir(args.directory)

if not os.path.exists('repo.yml'):
    print(_c('fail', "repo.yml not found"))
    sys.exit(2)

with open('repo.yml', 'r') as f:
    conf = yaml.safe_load(f)

repo = conf['repo']
tag = conf['tag']
last_updated = conf.get('last_updated', None)

current_hash = str(hashlib.md5(open(containerfile,'rb').read()).hexdigest())

if not last_updated:
    current_hash = last_updated
    conf['last_updated'] = current_hash

stag = semver.VersionInfo.parse(tag)

if last_updated != current_hash:
    conf['last_updated'] = current_hash
    stag = stag.bump_patch()

patchtag = '%s:%s.%s.%s' % (repo, stag.major, stag.minor, stag.patch)
minortag = '%s:%s.%s' % (repo, stag.major, stag.minor)
majortag = '%s:%s' % (repo, stag.major)
latesttag = '%s:latest' % (repo)

print(_c('okblue', "+ Building %s" % repo))
cmd = [args.cmd, 'build', 
        '-t', latesttag, '-t', patchtag,  
        '-t', minortag, '-t', majortag, 
        '-f', containerfile, '.']

out = subprocess.Popen(cmd).wait()

if args.push:
    for t in [latesttag, patchtag, minortag, majortag]:
        print(_c('okblue', '+ Pushing %s' % t))
        cmd = [args.cmd, 'push', t]
        out = subprocess.Popen(cmd).wait()

conf['tag'] = str(stag)
with open('repo.yml', 'w') as f:
    yaml.safe_dump(conf, f)

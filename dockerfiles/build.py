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

class Tag(object):
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor 
        self.patch = patch
    
    @classmethod
    def parse(cls, tag):
        t = tag.split('.')
        if len(t) == 3:
            return cls(t[0],t[1],t[2])
        elif len(t) == 2:
            return cls(t[0],t[1],None)
        elif len(t) == 1:
            return cls(t[0],None,None)
        raise AssertionError('Unable to parse %s' % tag)

parser = argparse.ArgumentParser()
parser.add_argument('-p','--push', default=False, action='store_true')
parser.add_argument('-c','--containerfile', default=None)
parser.add_argument('-r','--release', default=False, action='store_true')
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
tag = str(conf['tag'])
conf.setdefault('build', 1)
build = conf['build']
last_updated = conf.get('last_updated', None)
current_hash = str(hashlib.md5(open(containerfile,'rb').read()).hexdigest())
if not last_updated:
    last_updated = current_hash
    conf['last_updated'] = last_updated

tags = []

stag = Tag.parse(tag)

if args.release:

    if last_updated != current_hash:
        conf['last_updated'] = current_hash
        build += 1
        conf['build'] = build

    tags.append('%s:latest' % repo)
    if stag.patch is not None:
        tags.append('%s:%s.%s.%s-%s' % (repo, stag.major, stag.minor, stag.patch, build))
        tags.append('%s:%s.%s.%s' % (repo, stag.major, stag.minor, stag.patch))
        tags.append('%s:%s.%s' % (repo, stag.major, stag.minor))
        tags.append('%s:%s' % (repo, stag.major))
    elif stag.minor is not None:
        tags.append('%s:%s.%s-%s' % (repo, stag.major, stag.minor, build))
        tags.append('%s:%s.%s' % (repo, stag.major, stag.minor))
        tags.append('%s:%s' % (repo, stag.major))
    else:
        tags.append('%s:%s-%s' % (repo, stag.major, build))
        tags.append('%s:%s' % (repo, stag.major))
else:
    tags.append('%s:development' % repo)

print(_c('okblue', "+ Building %s" % repo))
cmd = [args.cmd, 'build', '-f', containerfile]
for t in tags:
    cmd += ['-t', t]
cmd.append('.')

out = subprocess.Popen(cmd).wait()
if out != 0:
    raise ChildProcessError(' '.join(cmd))

if args.push:
    for t in tags:
        print(_c('okblue', '+ Pushing %s' % t))
        cmd = [args.cmd, 'push', t]
        out = subprocess.Popen(cmd).wait()
        if out != 0:
            raise ChildProcessError(' '.join(cmd))
    for t in tags:
        print(_c('okgreen', 'Pushed %s' % t))

with open('repo.yml', 'w') as f:
    yaml.safe_dump(conf, f)

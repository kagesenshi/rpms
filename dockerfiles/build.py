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
    def __init__(self, major, minor, patch, variant=None):
        self.major = major
        self.minor = minor 
        self.patch = patch
        self.variant = variant
    
    @classmethod
    def parse(cls, tag):
        comp = tag.split('-')
        version = comp[-1]
        variant = None
        if len(comp) > 1:
            variant = '-'.join(comp[:-1])
        t = version.split('.')
        if len(t) == 3:
            return cls(t[0],t[1],t[2], variant=variant)
        elif len(t) == 2:
            return cls(t[0],t[1],None, variant=variant)
        elif len(t) == 1:
            return cls(t[0],None,None, variant=variant)
        raise AssertionError('Unable to parse %s' % tag)

    def tags(self, build=None):
        parts = [self.major, self.minor, self.patch]
        tags = []
        tag = []
        for idx, pt in enumerate(parts):
            if pt is not None:
                tag.append(str(pt))
                if idx == 0:
                    continue
                if self.variant:
                    tags.append(self.variant + '-' + '.'.join(tag))
                    if idx == (len(parts) - 1):
                        if build is not None:
                            tags.append(self.variant + '-' + '.'.join(tag) + '-' + str(build))
                else:
                    tags.append('.'.join(tag))
                    if idx == (len(parts) - 1):
                        if build is not None:
                            tags.append('.'.join(tag) + '-' + str(build))
        return tags

parser = argparse.ArgumentParser()
parser.add_argument('-p','--push', default=False, action='store_true')
parser.add_argument('-c','--containerfile', default=None)
parser.add_argument('-r','--release', default=False, action='store_true')
parser.add_argument('-R','--force-release', default=False, action='store_true')
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


stag = Tag.parse(tag)

tags = []
if args.release or args.force_release:

    if (last_updated != current_hash) or args.force_release:
        conf['last_updated'] = current_hash
        build += 1
        conf['build'] = build

    for t in stag.tags(build):
        tags.append('%s:%s' % (repo, t))
    tags.append('%s:latest' % repo)

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

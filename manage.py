#!/usr/bin/env python
import argparse
import re
from pathlib import Path
from subprocess import call

import requests

root = Path(__file__).parent


def sh(cmd, **kwargs):
    print(cmd)
    code = call(cmd, shell=True, **kwargs)
    if code:
        raise SystemExit(code)
    return 0


def build_base():
    cwd = root / 'base'
    url = 'https://raw.githubusercontent.com/dotcloud/docker/master/contrib/'
    for name in ('mkimage-arch.sh', 'mkimage-arch-pacman.conf'):
        body = requests.get(url + name).text
        if name == 'mkimage-arch.sh':
            body = re.sub(
                r'(docker run.*)archlinux',
                r'\g<1>--rm archlinux',
                body
            )
            body += (
                '\ndocker tag -f archlinux:latest naspeh/base'
                '\ndocker rmi archlinux:latest'
            )
        with (cwd / name).open('bw') as f:
            f.write(body.encode())

    sh('sudo ./mkimage-arch.sh', cwd=str(cwd))


def main(argv=None):
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(help='commands')

    def cmd(name, **kw):
        p = cmds.add_parser(name, **kw)
        p.set_defaults(cmd=name)
        p.arg = lambda *a, **kw: p.add_argument(*a, **kw) and p
        p.exe = lambda f: p.set_defaults(exe=f) and p
        return p

    cmd('base').exe(lambda a: build_base())
    cmd('web').exe(lambda a: sh(
        'docker build -t naspeh/web .',
        cwd=str(root / 'web')
    ))
    cmd('dev').exe(lambda a: sh(
        'cat ~/.ssh/id_rsa.pub > authorized_keys'
        '&& cat /etc/pacman.d/mirrorlist > mirrorlist'
        '&& docker build -t dev .',
        cwd=str(root / 'dev')
    ))

    args = parser.parse_args(argv)
    if not hasattr(args, 'exe'):
        parser.print_usage()
    else:
        args.exe(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)

#!/usr/bin/env python
import argparse
import re
from pathlib import Path
from subprocess import call


root = Path(__file__).parent.absolute()
src = Path('/home/dockerfiles/')
host = 'root@localhost'
port = '2200'


def sh(cmd, **kwargs):
    print(cmd)
    code = call(cmd, shell=True, **kwargs)
    if code:
        raise SystemExit(code)
    return 0


def ssh(cmd, **kw):
    return sh('ssh {host} -p{port} "{cmd}"'.format(
        host=host, port=port, cmd=cmd.replace('"', '\\"')
    ), **kw)


def build_base():
    import requests

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


def init(name, image):
    sh(
        'docker stop {name}; docker rm {name};'
        'docker run -d --net=host --name=web {image} &&'
        'sleep 5 &&'
        'scp -P{port} -r ./ {host}:{src}/'
        .format(src=src, host=host, port=port, name=name, image=image),
        cwd=str(root)
    )


def commit(name):
    ssh(
        'rm -rf /var/cache/pacman/pkg/* &&'
        'rm -rf /root/.ssh/authorized_keys &&'
        'sed -i '
        '   -e "s/^#*\(PermitRootLogin\) .*/\\1 yes/"'
        '   -e "s/^#*\(PasswordAuthentication\\) .*/\\1 yes/"'
        '   -e "s/^#*\(PermitEmptyPasswords\) .*/\\1 yes/"'
        '   /etc/ssh/sshd_config'
    )
    sh(
        'docker commit {name} naspeh/{name} &&'
        'docker stop {name} && docker rm {name}'
        .format(name=name)
    )


def general(local=False, dot=False, keys=''):
    run = sh if local else ssh
    if keys:
        run(
            'rm ~/.ssh/* &&'
            'ssh-keygen -A &&'
            'ssh-keygen -q -t rsa -N "" -f /root/.ssh/id_rsa &&'
            'rsync -v {keys} /root/.ssh/authorized_keys &&'
            'cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys'
            .format(keys=keys)
        )

    if dot:
        run(
            'pacman --noconfirm -Sy python-requests &&'
            '([ -d {path} ] || mkdir {path}) &&'
            'cd {path} &&'
            '([ -d .git ] ||'
            '   git clone https://github.com/naspeh/dotfiles.git .'
            ') &&'
            'git pull && ./manage.py init --boot vim zsh bin'
            .format(path='/home/dotfiles')
        )

    run(
        '([ -f /root/.ssh/authorized_keys ] || ('
        '   echo "no authorized_keys" && exit 1'
        ')) &&'
        'sed -i '
        '   -e "s/^#*\(PermitRootLogin\) .*/\\1 yes/"'
        '   -e "s/^#*\(PasswordAuthentication\\) .*/\\1 no/"'
        '   -e "s/^#*\(PermitEmptyPasswords\) .*/\\1 no/"'
        '   -e "s/^#*\(UsePAM\) .*/\\1 no/"'
        '   /etc/ssh/sshd_config'
    )


def build_web():
    ssh(
        'cp {mnt}/mirrorlist /etc/pacman.d/ &&'
        'pacman --noconfirm -Sy'
        '   sudo zsh git rsync vim-python3 python'
        '   openssh nginx supervisor fcron logrotate'
        '&&'
        'rsync -v {mnt}/nginx.conf /etc/nginx/ &&'
        'rsync -v {mnt}/supervisord.conf /etc/ &&'
        'rsync -v {mnt}/logrotate.conf /etc/ &&'
        'rsync -v {mnt}/locale.conf /etc/ &&'
        '([ -d /etc/fcrontab ] || mkdir /etc/fcrontab) &&'
        'rsync -vr {mnt}/fcrontab /etc/fcrontab/00-default &&'
        'cat /etc/fcrontab/* | fcrontab - &&'
        'chsh -s /bin/zsh &&'
        .format(mnt=src / 'web')
    )


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
    cmd('sshd').exe(lambda a: sh(
        'docker build -t naspeh/sshd .',
        cwd=str(root / 'sshd')
    ))
    cmd('web')\
        .exe(lambda a: build_web())
    cmd('init')\
        .arg('-i', '--image', default='naspeh/sshd')\
        .arg('-n', '--name', default='web')\
        .exe(lambda a: init(a.name, a.image))
    cmd('commit')\
        .arg('-n', '--name', default='web')\
        .exe(lambda a: commit(a.name))
    cmd('general')\
        .arg('-d', '--dot', action='store_true')\
        .arg('-l', '--local', action='store_true')\
        .arg('-k', '--keys', help='path to authorized_keys')\
        .exe(lambda a: general(a.local, a.dot, a.keys))

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

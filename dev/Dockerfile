FROM naspeh/sshd
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ADD mirrorlist /etc/pacman.d/mirrorlist

RUN pacman-wrap -Syy python-virtualenv python-requests

RUN cd /home/ && git clone https://github.com/naspeh/dotfiles.git
RUN sudo /home/dotfiles/manage.py init --boot zsh bin vim dev

ADD authorized_keys /root/.ssh/
RUN chmod 600 /root/.ssh/authorized_keys

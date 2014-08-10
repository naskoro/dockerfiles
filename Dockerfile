FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

WORKDIR /root
ADD pacman /root/pacman
ADD pkgs /root/pkgs

RUN ./pacman -Sy
RUN ./pacman -S sudo zsh git python python2 python-virtualenv python-requests
RUN ./pacman -U ./pkgs/vim*

RUN cd /home/ && git clone https://github.com/naspeh/dotfiles.git
RUN sudo /home/dotfiles/manage.py init --boot zsh bin vim dev

RUN rm -rf ./pacman ./pkgs/*

CMD ["sudo", "/bin/zsh"]

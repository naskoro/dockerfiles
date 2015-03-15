FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ENV PACMAN pacman --noconfirm --noprogressbar

RUN $PACMAN -Sy sudo zsh git python python2 python-virtualenv python-requests

ADD pkgs /pkgs
RUN $PACMAN -U /pkgs/vim*

RUN rm -rf /pkgs /var/cache/pacman/pkg/*

RUN cd /home/ && git clone https://github.com/naspeh/dotfiles.git
RUN sudo /home/dotfiles/manage.py init --boot zsh bin vim dev

RUN chsh -s /bin/zsh
ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 TERM=xterm
RUN locale-gen $LC_ALL

CMD /bin/zsh

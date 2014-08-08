FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ADD pacman pacman
ADD pkgs pkgs

RUN /pacman -Sy
RUN /pacman -S zsh git python python2 python-virtualenv python-requests
RUN /pacman -U /pkgs/*

RUN cd /home/ && git clone https://github.com/naspeh/dotfiles.git
RUN sudo /home/dotfiles/manage.py init --boot zsh bin vim dev

RUN rm -rf /pacman ./pkg/*

CMD ["sudo", "/bin/zsh"]

FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ENV PACMAN pacman --noconfirm --noprogressbar
ADD mirrorlist /etc/pacman.d/mirrorlist

RUN $PACMAN -Syy \
    sudo zsh git openssh supervisor \
    python python2 python-virtualenv python-requests

ADD pkgs /pkgs
RUN $PACMAN -U /pkgs/vim*

RUN rm -rf /pkgs /var/cache/pacman/pkg/*

RUN cd /home/ && git clone https://github.com/naspeh/dotfiles.git
RUN sudo /home/dotfiles/manage.py init --boot zsh bin vim dev

RUN chsh -s /bin/zsh
ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 TERM=xterm
RUN locale-gen $LC_ALL

RUN ssh-keygen -A
RUN sed -i \
    -e 's/^#*\(PermitRootLogin\) .*/\1 yes/' \
    -e 's/^#*\(PasswordAuthentication\) .*/\1 no/' \
    -e 's/^#*\(PermitEmptyPasswords\) .*/\1 no/' \
    -e 's/^#*\(UsePAM\) .*/\1 no/' \
    -e 's/^#*\(X11Forwarding\) .*/\1 yes/' \
    -e 's/^#*\(Port\) .*/\1 2222/' \
    /etc/ssh/sshd_config
RUN ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa

ADD supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

ADD authorized_keys /root/.ssh/
RUN chmod 600 /root/.ssh/authorized_keys

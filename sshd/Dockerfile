FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ADD mirrorlist /etc/pacman.d/mirrorlist

RUN pacman --noconfirm -Syy openssh supervisor

ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 TERM=xterm
RUN locale-gen $LC_ALL

RUN ssh-keygen -A
RUN ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa
RUN sed -i \
    -e 's/^#*\(PermitRootLogin\) .*/\1 yes/' \
    -e 's/^#*\(PasswordAuthentication\) .*/\1 yes/' \
    -e 's/^#*\(PermitEmptyPasswords\) .*/\1 yes/' \
    -e 's/^#*\(UsePAM\) .*/\1 no/' \
    -e 's/^#*\(Port\) .*/\1 2200/' \
    /etc/ssh/sshd_config

ADD supervisord.conf /etc/
CMD ["supervisord", "-c", "/etc/supervisord.conf"]

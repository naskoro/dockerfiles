FROM naspeh/base
MAINTAINER Grisha Kostyuk "naspeh@gmail.com"

ADD pacman-wrap /usr/local/bin/
ADD mirrorlist /etc/pacman.d/mirrorlist

RUN pacman-wrap -Syy \
    sudo zsh git openssh nginx \
    supervisor python python2

ADD pkgs /pkgs
RUN pacman-wrap -U /pkgs/vim* && rm -rf /pkgs

RUN chsh -s /bin/zsh
ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 TERM=xterm
RUN locale-gen $LC_ALL

RUN ssh-keygen -A
RUN sed -i \
    -e 's/^#*\(PermitRootLogin\) .*/\1 yes/' \
    -e 's/^#*\(PasswordAuthentication\) .*/\1 no/' \
    -e 's/^#*\(PermitEmptyPasswords\) .*/\1 no/' \
    -e 's/^#*\(UsePAM\) .*/\1 no/' \
    -e 's/^#*\(Port\) .*/\1 2200/' \
    /etc/ssh/sshd_config
RUN ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa

ADD nginx.conf /etc/nginx/
ADD supervisord.conf /etc/
CMD ["supervisord", "-c", "/etc/supervisord.conf"]

# Docker images for various targets

## "Base" - clean archlinx image
Just clean archlinux image based [docker/contrib/mkimage-arch.sh][mkimage].

[mkimage]: https://github.com/docker/docker/blob/master/contrib/mkimage-arch.sh

Build command: `./manage.py base`


## "Sshd" - base image with sshd
Minimal image with `supervisor` and `sshd`.

Login over ssh with **root** user and **no password**.

Build command: `./manage.py sshd`

## "Web" - base image for web
### Installed & configured packages:
- supervisor
- sshd
- nginx
- fcron
- logrotate

**NB:** Required `authorized_keys` to login over ssh

Build command: `./manage.py web`

### Usage in Dockerfile
```dockerfile
FROM naspeh/web

ADD authorized_keys /root/.ssh/
RUN chmod 600 /root/.ssh/authorized_keys
```

### Usage if run image directly
```bash
docker run -d --net=host --name=web naspeh/web
docker exec -i web /bin/bash -c 'cat >> /root/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub
ssh root@localhost -p2200
```

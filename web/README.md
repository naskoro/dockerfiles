# Base image for web

### Installed & configured packages:
- supervisor
- sshd
- nginx
- fcron
- logrotate

**NB:** Required `authorized_keys` to login over ssh

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

# Image with sshd and supervisor

**NB:** Required `authorized_keys` to login over ssh

### Usage in Dockerfile
```dockerfile
FROM naspeh/sshd

ADD authorized_keys /root/.ssh/
RUN chmod 600 /root/.ssh/authorized_keys
```

### Usage if run directly
```bash
docker run -d --net=host --name=sshd naspeh/sshd
docker exec -i sshd /bin/bash -c 'cat >> /root/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub
ssh root@localhost -p2200
```

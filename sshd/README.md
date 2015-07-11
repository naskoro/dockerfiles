# Usage
```dockerfile
FROM naspeh/sshd

ADD authorized_keys /root/.ssh/
RUN chmod 600 /root/.ssh/authorized_keys
```

### Fill `authorized_keys` if you want to run this image directly
```bash
docker run -d --net=host --name=sshd naspeh/sshd
docker exec -i sshd /bin/bash -c 'cat >> /root/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub
```

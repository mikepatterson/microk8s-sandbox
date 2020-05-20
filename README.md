# Setup

<details><summary>Install MicroK8s</summary>

```bash
# ubuntu microk8s+docker
sudo apt install snapd docker.io
sudo snap install microk8s --classic

# centos microk8s+podman
sudo yum install snapd podman
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install microk8s --classic
```

```bash

microk8s.enable dns ingress

alias kubectl='microk8s.kubectl'

sudo usermod -aG docker ${USER}
su - ${USER}

# verfiy you can deploy a container
kubectl create ns test
kubectl -n test run my-shell --rm -i --tty --image ubuntu -- bash
kubectl delete ns test
```

</details>

<details><summary>Setup Private Registry Using Podman</summary>

Spin up registry container, mounting host's container storage

```bash
podman run --privileged -d \
  --name registry \
  -p 5000:5000 \
  -v $HOME/.local/share/containers/storage/:/var/lib/registry \
  --restart=always \
  registry:2
```

Edit MicroK8s registry configuration (2 files)

```toml
# FILE: /var/snap/microk8s/current/args/containerd-template.toml

# REDACTED
    [plugins.cri.registry]
      [plugins.cri.registry.mirrors]
        [plugins.cri.registry.mirrors."docker.io"]
          endpoint = ["https://registry-1.docker.io"]
         [plugins.cri.registry.mirrors."127.0.0.1:5000"] # PRIVATE REGISTRY DEFINITION
          endpoint = ["http://127.0.0.1:5000"]           # PRIVATE REGISTRY DEFINITION
```

```bash
# FILE: /etc/containers/registries.conf
[registries.insecure]
registries = ['127.0.0.1:5000']
```

Restart microk8s to load changes

```bash
microk8s stop && microk8s start
```

Verify private registry is online
```bash
$ podman ps
CONTAINER ID  IMAGE                         COMMAND               CREATED      STATUS          PORTS                   NAMES
12d392703c03  docker.io/library/registry:2  /etc/docker/regis...  2 hours ago  Up 2 hours ago  0.0.0.0:5000->5000/tcp  registry

$ curl http://127.0.0.1:5000/v2/_catalog
{"repositories":[]}
```
</details>

<details><summary>Import Docker Image into MicroK8s With No Registry</summary>

```bash
docker save retracker:v1 > retracker-v1.tar
microk8s.ctr -n k8s.io image import retracker-v1.tar
microk8s.ctr -n k8s.io images ls | grep retracker
```
</details>

# Build

<details><summary>Build Container Image</summary>

**Build with docker**

```bash
$ cd app/
$ docker build -t "retracker:v1" .
```
**Build with podman**

```bash
$ cd app/
$ podman  build -t "retracker:v1" .

$ podman images
REPOSITORY                 TAG   IMAGE ID       CREATED         SIZE
localhost/retracker        v1    53b1cfaeb1d1   3 minutes ago   970 MB

$ podman tag 53b1cfaeb1d1 127.0.0.1:5000/retracker:v1
$ podman images
REPOSITORY                 TAG   IMAGE ID       CREATED         SIZE
localhost/retracker        v1    53b1cfaeb1d1   4 minutes ago   970 MB
127.0.0.1:5000/retracker   v1    53b1cfaeb1d1   4 minutes ago   970 MB

```
</details>

# Deploy

```bash
cd k8s/
kubectl create -f deployment.yaml
kubectl create -f service.yaml
kubectl create -f ingress.yaml
```

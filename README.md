# MicroK8s

**Install Microk8s**

```bash
sudo apt install snapd docker.io
sudo snap install microk8s --classic

microk8s.enable dns ingress

alias kubectl='microk8s.kubectl'

sudo usermod -aG docker ${USER}
su - ${USER}

# verfiy you can deploy a container
kubectl create ns test
kubectl -n test run my-shell --rm -i --tty --image ubuntu -- bash
kubectl delete ns test
```

**Build Docker Image**

```bash
cd app/
docker build -t "retracker:v1" .
```

**MicroK8s 1.14 No Docker Workaround**

```bash
docker save retracker:v1 > retracker-v1.tar
microk8s.ctr -n k8s.io image import retracker-v1.tar
microk8s.ctr -n k8s.io images ls | grep retracker
```

**Deploy Test App**

```bash
cd k8s/
kubectl create -f deployment.yaml
kubectl create -f service.yaml
kubectl create -f ingress.yaml
```

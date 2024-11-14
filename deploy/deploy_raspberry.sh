# obsolete
sudo apt update
sudo apt install docker.io

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

curl -sSL https://get.docker.com | sh

sudo curl -L https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-`uname -s`-`uname -m` > docker-compose
sudo mv docker-compose /usr/bin/
sudo chown root: /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
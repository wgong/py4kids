Ubuntu Jammy 22.04 (LTS)

## [VS Code](https://phoenixnap.com/kb/install-vscode-ubuntu)
```
sudo snap install --classic code
code --version  # 1.85.1
```

## [Git](https://phoenixnap.com/kb/how-to-install-git-on-ubuntu)
How to Work With GitHub and Multiple Accounts: 
https://code.tutsplus.com/quick-tip-how-to-work-with-github-and-multiple-accounts--net-22574t

```
sudo apt update
sudo apt install git
git --version   # 2.34.1

ssh-keygen -t rsa -b 4096 -C "wg@email.com"    
ssh-keygen -t rsa -b 4096 -C "gw@email.com"


```
add .ssh/config
```
#Default GitHub 
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
Host github.com-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_work
```

add `-work` to git-clone-url
```
git clone git@github.com-work:gongwork/st_rag.git
```



## [Anaconda](https://www.hostinger.com/tutorials/how-to-install-anaconda-on-ubuntu/)
```
sudo apt-get update
wget  https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
bash Anaconda3-2023.09-0-Linux-x86_64.sh
python --version    # Python 3.11.5
```

## [Docker](https://docs.docker.com/engine/install/ubuntu/)

```
cd ~/tmp

## Install Docker Engine ## Install Docker Desktop
using the apt repository

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

## Install Docker Desktop

sudo apt-get update
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.26.1-amd64.deb
sudo apt-get install ./docker-desktop-4.26.1-amd64.deb

docker --version  # 24.0.7, build afdd53b

docker version

docker compose version

systemctl --user enable docker-desktop
systemctl --user stop docker-desktop
```

## [KeePass](https://linux.how2shout.com/install-keepass-password-manager-on-ubuntu-20-04-lts/)

```
sudo apt update
sudo apt install keepass2
```


## [Master PDF Editor 5](https://snapcraft.io/install/master-pdf-editor-5/ubuntu#install)

```bash
sudo apt update
sudo apt install snapd
sudo snap install master-pdf-editor-5

```

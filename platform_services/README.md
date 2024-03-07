## Install

Download and install [*docker*](https://docs.docker.com/engine/install/ubuntu/)

```shell
sudo apt install python3 python3-pip

python3 -m pip install -r scripts/requirements.txt
```

## Run

```shell
docker compose up
```

## Setup

```shell
export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./scripts/setup.py
```
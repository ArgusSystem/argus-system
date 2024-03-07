# Argus Web

## API Web Server

### Install

```shell
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-web-api-venv

source argus-web-api-venv/bin/activate

python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters are stored in [development.yml](development.yml).

- server: configuration of server deployment
  - host: IP to bind server to
  - port: port to deploy server to
- publisher_to_warden: configuration for rabbitmq publisher to *argus-warden*
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - exchange: exchange to publish messages
  - routing_key: key string to label the messages
  - ssl_ca: path of ssl certificate
- db: configuration of PostgreSQL database client
  - database: name of the database to connect to
  - host: IP of the PostgreSQL server
  - port: port of the PostgreSQL server
  - user: username of an authorized user of PostgreSQL server
  - password: password of the user
- video_storage: configuration of Minio storage client
  - host: IP of minio server
  - port: port of minio server
  - access_key: username of authorized user
  - secret_key: password of authorized user
- ssl: configuration for ssl 
  - certfile: location of certification file
  - keyfile: location of key file
- tracer: configuration of jaeger client
  - host: IP of jaeger server
  - port: port of jaeger server

### Run

```shell
source argus-web-api-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./server.py -c configuration_file.yml
```
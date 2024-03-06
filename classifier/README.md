# argus-classifier

The classifier application receives a face and performs face classification on it.
Results are then sent to the Web server for overlaying with the security cameras live feed.

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-classifier-venv

source argus-classifier-venv/bin/activate

python3 -m pip install -r requirements.txt
```

### Configuration

Before running, proper configuration should be considered.
Default parameters for development are stored in [development.yml](config/development.yml).

- consumer: configuration for rabbitmq consumer
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - queue: name of queue to consume messages
  - ssl_ca: path of ssl certificate
- face_embedder: configuration for face embeddings
  - type: possible types are tensorflow_facenet, pytorch_facenet and paddle_mobilefacenet
- face_classifier: configuration for face classifier
  - model: local path of the classifier model
  - minio: name of the classifier model file in minio
  - threshold: threshold to determine whether a face is a match or not
- publisher_web: configuration for rabbitmq publisher to argus-web
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - exchange: exchange to publish messages
  - routing_key: key string to label the messages
  - ssl_ca: path of ssl certificate
- publisher_warden: configuration for rabbitmq publisher to argus-warden
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
- storage: configuration of Minio storage client
  - host: IP of minio server
  - port: port of minio server
  - access_key: username of authorized user
  - secret_key: password of authorized user
- logging: level of logging, for example, DEBUG, INFO, WARNING or ERROR.
- tracer: configuration of jaeger client
  - host: IP of jaeger server
  - port: port of jaeger server

### Run

```bash
source argus-classifier-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```

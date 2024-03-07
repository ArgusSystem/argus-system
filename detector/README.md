# argus-detector

The detector application receives a frame and performs face detection on it.
Detected faces are then sent to the Classifier for further processing.

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-detector-venv

source argus-detector-venv/bin/activate

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
- face_detector: configuration for face detector
  - type: possible types are tensorflow_mtcnn, tensorflow_faceboxes, paddle_mtcnn and dlib_mmod
  - min_pixels: minimum number of pixels to be a valid face
- debug: allows image debug
- notifier: configuration of notification service
  - type: can be classification or web
  - publisher: configuration for rabbitmq publisher
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
source argus-detector-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```

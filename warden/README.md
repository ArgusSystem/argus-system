# Warden application

The warden is in charge of applying the restrictions configured by
the users to the faces analysed by *argus-classifier*. Broken restrictions are
sent to *argus-notifier*.


### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-warden-venv

source argus-warden-venv/bin/activate

python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in [development.yml](development.yml).

- consumer: configuration for rabbitmq consumer
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - queue: name of queue to consume messages
  - ssl_ca: path of ssl certificate
- publisher: configuration for rabbitmq publisher to *argus-notifier*
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
- logging: level of logging, for example, DEBUG, INFO, WARNING or ERROR.
- tracer: configuration of jaeger client
  - host: IP of jaeger server
  - port: port of jaeger server


### Run

```bash
source argus-sampler-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```
# Notifier application

- Send notifications to users
- Throttle notifications

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-notifier-venv

source argus-notifier-venv/bin/activate

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
- db: configuration of PostgreSQL database client
    - database: name of the database to connect to
    - host: IP of the PostgreSQL server
    - port: port of the PostgreSQL server
    - user: username of an authorized user of PostgreSQL server
    - password: password of the user
- tracer: configuration of jaeger client
  - host: IP of jaeger server
  - port: port of jaeger server

### Run

```bash
source argus-notifier-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```
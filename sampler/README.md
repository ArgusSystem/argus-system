# Sampler application
The Sampler application is in charge of accepting video chunks that need
processing. Once a new video chunk event is triggered, a sampler should
split the video into frames to send a processing event for the frame, 
change the video format to be compliant with the web video formats and
send an event to the web application with a new video chunk ready to
play.


### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv
sudo apt install ffmpeg

python3 -m venv argus-sampler-venv

source argus-sampler-venv/bin/activate

python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in [development.yml](development.yml).

- sampling_rate: number of frames to sample in a second
- consumer: configuration for rabbitmq consumer
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - queue: name of queue to consume messages
  - ssl_ca: path of ssl certificate
- video_chunk_publisher: configuration for rabbitmq publisher for processing video chunks events
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - exchange: exchange to publish messages
  - routing_key: key string to label the messages
  - ssl_ca: path of ssl certificate
- frame_publisher: configuration for rabbitmq publisher for frames-to-process events
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
source argus-sampler-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```
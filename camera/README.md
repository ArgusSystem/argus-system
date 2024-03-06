# argus-camera

The camera application records video from a video source and uploads it to the Argus system.
This application is meant to run on a Raspberry PI with a camera.

### Install

It is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip python3-venv

python3 -m venv argus-camera-venv

source argus-camera-venv/bin/activate

python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in [development.yml](development.yml).

- id: string with identifier of camera
- publisher: configuration for rabbitmq publisher
  - host: IP of rabbitmq server
  - username: username of authorized user of rabbitmq
  - password: password of user
  - exchange: exchange to publish messages
  - routing_key: key string to label the messages
  - ssl_ca: path of ssl certificate
- video_recorder: configuration for recording
  - resolution: width and height of the camera
  - recording_split: time in seconds to split the recording in fragments
  - framerate: frames per second of the camera
- storage: configuration of Minio storage client
  - host: IP of minio server
  - port: port of minio server
  - access_key: username of authorized user
  - secret_key: password of authorized user
- logging: level of logging, for example, DEBUG, INFO, WARNING or ERROR.
- tracer: configuration of jaeger server
  - host: IP of jaeger server
  - port: port of jaeger server

### Run

```bash
source argus-camera-venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```

### Development

The camera consists of two tasks that are running concurrently in separate threads:

```
+--------------+     +--------------------------------+
| Record video | --> | Upload video chunk             |
+--------------+     | Publish Video Processing Event |
                     +--------------------------------+
```

1) The first thread records a short video into a local file.
2) Second thread uploads the video chunk into a file storage (e.g. S3/Minio) and publish an event to start 
the video processing pipeline.
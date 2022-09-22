# Camera application

The camera application records video from a video source and uploads it to the Argus system.
This application is meant to run on a Raspberry PI with a camera, but it can also run on a computer with a webcam.

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in *development.yml*.

### Run

```bash
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
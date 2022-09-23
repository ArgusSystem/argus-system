# Detector application

The detector application receives a frame and performs face detection on it.
Detected faces are then sent to the Classifier for further processing.

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
export PYTHONPATH=$PYTHONPATH:/home/argus/argus-system
python3 -m pip install -r requirements.txt
```

### Configuration

Before running, proper configuration should be considered.
Default parameters for development are stored in *config/development.yml*.

### Run

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/argus-system
./run.py -c configuration_file.yml
```

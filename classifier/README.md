# Classifier application

The classifier application receives a face and performs face classification on it.
Results are then sent to the Web server for overlaying with the security cameras live feed.

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

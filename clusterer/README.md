# Clusterer application

The clusterer application receives unknown face and accumulates them.
Once enough have been received they are separated into clusters by similarity using HDBSCAN.

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

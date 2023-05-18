# Notifier application

- Send notifications to users
- Throttle notifications

### Install

Although it isn't necessary, it is recommended to run the application in a virtual environment.
To install all the dependencies, execute the following script: 

```bash
sudo apt install python3 python3-pip

python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in *development.yml*.

### Run

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/argus-system

./run.py -c configuration_file.yml
```
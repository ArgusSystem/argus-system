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
python3 -m pip install -r requirements.txt
```

### Configuration

Default parameters for development are stored in *development.yml*.

### Run

```bash
./run.py -c configuration_file.yml
```
# Application module

The *application* module is a basic frame to be used in all the applications in the Argus project.
This module concentrates common tasks that are needed in all the microservices, for example:
- Parsing arguments
- Loading configuration
- Starting (distributed) logging
- Handle Linux signals

## Usage

```python
from utils.application.src.application import run

# Do an expensive task
def work():
    return

with run('application_name') as application:
    while not application.is_stopped():
        work()
```
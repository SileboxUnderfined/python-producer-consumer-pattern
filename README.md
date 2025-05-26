# Python Producer Consumer Pattern Implementation

## Table of contents

1. [About project](#about-project)
2. [Architecture](#architecture)
   1. [Main Modules](#main-modules)
      1. [main.py](#mainpy)
      2. [server.py](#serverpy)
      3. [worker.py](#workerpy)
   2. [Logging Mechanism](#logging-mechanism)
   3. [Meta Modules](#meta-modules)
      1. [logger_setup.py](#logger_setuppy)
      2. [message_command.py](#message_commandpy)
      3. [message_worker.py](#message_workerpy)
      4. [multi_process_worker.py](#multi_process_workerpy)
3. [How to use this template](#how-to-use-this-template)
4. [Deployment](#deployment)

## About Project

The main goal of the project is to create a template
for writing fault-tolerant, easily extensible services.  

To achieve this goal, I used design pattern called **Producer/Consumer** 
or [Publish-Subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern).

## Architecture

There are two entities: **Server** and **Worker**.

**Server** is a **_Producer_** entity, which listens messages from web server and sends messages to **Worker**.

**Worker** is a **_Consumer_** entity, which listens messages from **Server** and do business logic.

Project's goal is to establish communication between these entities.

### Main Modules

There are required environment variables:

| Name          | Example Value | Description                                                     |
|---------------|---------------|-----------------------------------------------------------------|
| DEBUG         | 1             | Indicates which logging_levels and which server will be started |
| WAITRESS_HOST | 0.0.0.0       | IP-Address for deployment server                                |
| WAITRESS_PORT | 8000          | Port for deployment server                                      |

#### main.py

This module prepares processes to be run in multiprocess, environment variables, logging mechanism and grateful stop mechanism

You need to edit **start_worker** and **start_server** functions to suit your needs

**start_server** function checks environment variable **_DEBUG_**.
if it equals **"1"**, then starts werkzeug development server. Else - watress.

#### server.py

This module describes **Server** class. All server-side and web logic should be put there.

#### worker.py

This module describes **Worker** class. All business logic should be put there.

### Logging Mechanism

in **main.py** module initializes two handlers: **StreamHandler** and **QueueHandler**

**StreamHandler** used by logger in main process and it's just logs data to console

**QueueHandler** used by loggers in other processes. There is an Queue from multiprocessing module, and other
loggers log into this queue. **QueueListener** listens for data from **QueueHandlers** and redirects them into **StreamHandler**

### Meta Modules

#### logger_setup.py

In **logger_setup.py** there is an decorator called **logger_setup**

You need to use this decorator in class to automatic setup for logging

```python
from src.meta import logger_setup # or just from meta import logger_setup
from multiprocessing import Queue
from logging import Logger

@logger_setup
class A:
    def __init__(self, queue: Queue):
        self._logger: Logger | None = None
        
        # After that will be executed decorator's init function
```

It's needed to put log queue in arguments, because this variable will be used in decorator.

#### message_command.py

In **message_command.py** there is an dataclass **MessageCommand**.

It represents the messages that processes will exchange.

```python
from src.meta import MessageCommand # or just from meta import MessageCommand
from json import dumps

message = {"command":"hi_request","arguments":["hi!"]}
message_serialized_0 = dumps(message) # serializing dict into json string

message_obj = MessageCommand.from_json(message_serialized_0) # Deserializing message into MessageCommand object

print(message_obj.command) # Data fields accessible

message_serialized_1 = message_obj.to_json() # Serializing MessageCommand object into json string

assert message_serialized_0 == message_serialized_1 # they will be equal
```

#### message_worker.py

there is an interface **MessageWorker** which 
describes methods **receive_message** and **send_message**

```python
from src.meta import MessageWorker, MessageCommand  # or just from meta import MessageWorker
from multiprocessing.connection import Connection

class A(MessageWorker):
    def __init__(self, conn: Connection):
        self._connection = conn

    def receive_message(self):
        msg: str = self._connection.recv()
        cmd: MessageCommand = MessageCommand.from_json(msg)
        
        # logic to process messages

    def send_message(self, message: MessageCommand):
        data: str = message.to_json()
        self._connection.send(data)
```

#### multi_process_worker.py

there is an base class for **Worker** and **Server** classes
which called **MultiProcessWorker**.
This class initializes fields needed for both classes. 

If you need to add some fields,
you need to edit constructor of this class. 

If You need to add methods or logic, 
you need to add to this class **interfaces** or **decorators**.

## How to use this template

In most cases, you need to edit two modules: **worker.py** and **server.py**

In **Worker** you need to add your business logic

In **Server** you need to add your url_rules

If you need to add meta functionality for these classes, add meta modules in **meta** package directory

If you need to change mechanism of initializing application - edit **main.py** module

## Deployment

There is already a **Dockerfile** file that creates the most minimal image of the application.

If you want to change entrypoint command, or command arguments, or edit other container functionality, edit this file

To deploy application, you need to install [Docker](https://docs.docker.com/engine/install/) 

```bash
git clone <YOUR_REPO>
cd <YOUR_REPO_DIRECTORY>
docker build -t <IMAGE_NAME> .
docker run -d -p <HOST_PORT>:<CONTAINER_PORT> -t <CONTAINER_NAME> <IMAGE_NAME>
```
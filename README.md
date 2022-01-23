

# flask-vue-project-seed

> SPA quick start using Python, Flask, and Vue.js. Containerized with Docker.


## Requirements

- docker
- docker-compose
- make (optional)


## What is this repo and how do I use it?

This repository is meant to be a full-stack web application starting point. It
contains these basic parts and features:

### General:
- Containerized with Docker and Docker Compose
- Backend and Frontend code built with Webpack
- Example full-stack 'wall message' web application

### Backend:
- Python3 and Flask
- MySQL database container and driver
- Redis cache container and driver
- Architecture:
  * API (interface endpoints, call into service layer, format response)
  * Services (operate on data objects, business logic)
  * Data Objects (stateful models, represent deserialized records, implements CRUD)
  * Data Store Drivers (intermediary interface between application and datastore)

### Frontend:
- Vue.js
- vue-router
- Architecture:
  * Services (handle state and business logic, injectable into views and components)
  * Views (top level web page wrappers)
  * Components (UI building blocks, reusable, nestable)


## More Information:

`make up` runs both a Flask backend server and a webpack frontend server
simultaneously. The webpack frontend server proxies the Flask backend. The app
directory is a Docker mounted volume, and changes to backend and client files
will be automatically reflected.


## Getting started with the full-stack app example:

First, spin-up the dev environment:
```sh
make up
```

Then, connect to the app server container:
```sh
make app-shell
```

Once connected, run the table creation python script:
```sh
cd /app/server/scripts/ && python3 create-wall-message-table.py
```

Lastly, navigate to the 'wall messages' dev web page and create some messages:
```sh
http://localhost:4000/wall-messages
```


### Other convenience make commands

Connect to app server container:
```sh
make app-shell
```

Connect to MySQL container:
```sh
make mysql-shell
```

Connect to Redis container:
```sh
make redis-shell
```


## Tech Stack:

OS/Containerization:
- Docker
- Docker Compose
- Alpine

Languages:
- Python3
- Node.js
- Javascript ES6

Datastores:
- MySQL
- Redis

Backend:
- Flask
- Supervisor

Frontend:
- Vue.js
- Scss

Tools:
- npm
- pip3
- Adminer
- Webpack


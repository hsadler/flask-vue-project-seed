

# flask-vue-project-seed

> SPA quick start using Python Flask and Vue.js. Containerized with Docker.


## Requirements

- docker
- docker-compose


## Notes:

***** This is a work in progress, but... *****

Both the dev and prod mode Docker containers are working.

Prod mode serves exclusively from the Flask backend (app index.html, static
assets, and JSON API).

Dev mode runs both a Flask backend server and a webpack frontend server
simultaneously. The webpack frontend server proxies the Flask backend. The app
directory is a Docker mounted volume, and saves to backend and client files will
be automatically reflected in the container's server responses.

I imagine this could be used to develope both locally or on a remote dev host.
Just fire-up '. dev.sh' and rsync files upon update. Even webpack's hot-reload
works from the container!

Included in this project is a homebrewed database driver, cache driver and data
object architecture to provide a starting point for new projects.

Here's an outline of the multitier architecture so far:
- api (client endpoints, call into model layer, format response)
- service (operate on data objects, business logic)
- data object (stateful models, represent deserialized records, implements CRUD)
- data store driver (intermediary interface between application and datastore)


## Usage

### Dev Mode

Start dev mode server in Docker container:
```sh
source dev.sh
```

Navigate to dev localhost URL:
```sh
http://localhost:4000
```

### Prod Mode

Start prod mode server in Docker container:
```sh
source prod.sh
```

Navigate to prod localhost URL:
```sh
http://localhost
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
- Nginx
- uWSGI
- Supervisor
- Flask

Frontend:
- Vue.js
- Scss

Tools:
- npm
- pip3
- Adminer
- Webpack


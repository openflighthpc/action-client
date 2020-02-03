# Run a command on a node or over a group

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run action_app cli application

$ action_app --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Configuration

Refer to [reference config](config/action_app.yaml.example) on how to configure the application.

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Action Client`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it action_app --help
```

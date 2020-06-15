![Python application](https://github.com/christopherpryer/cvrp-app/workflows/Python%20application/badge.svg)
![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

# cvrp-app
Development project for solving the vehicle routing problem via containerized microservices & a restful API implementation. **Note that the first few iterations will be monolithic.** The goal is to identify and abstract services for meaningful improvements.

# objectives

- redevelop the [cvrp-app](https://github.com/christopherpryer/cvrp-app) for production-grade requirements
- learn to utilize [Vagrant](https://www.vagrantup.com/) for standard linux development environments
- learn to utilize [docker](https://www.docker.com/)
- build a deployable prototype in python to get going
- refator and optimize using c++ and typescript for learning purposes (some features will remain in python).
  - service balancers and product optimzations: c++
  - solution optimizations: c++
  - web client: typescript, vue.js?, electron.js? css framework?
- lean on and learn to contribute to [or-tools](https://github.com/google/or-tools)
- dive deeper into numpy utilization and custom optimizations
- deploy to [DO](https://www.digitalocean.com/)
- complete as modular service for future projects

# development

Initial development will be monolithic type until services can be abstracted. Current process:

1. Setup vagrant environment (not needed but some of the commands below might change)
2. Setup database for environment
3. Test environment
4. Launch app

# demo

recommended: setup vagrant development environment
```
vagrant up
vagrant ssh
cd /vagrant
pip3 install -r requirements.txt
```

add instance/app.db & create database (if it doesn't exist)
```
mkdir instance
touch instance/app.db
python3 manage.py db create_all
```

add .env file or set environment variables yourself
```.env
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1 # not needed
```

:rocket: launch
```
python3 manage.py runserver --host=0.0.0.0
```

register & sign in

upload test data 

```cvrp-app/tests/vrp_testing_data.csv```

![](https://github.com/christopherpryer/cvrp-app/blob/master/docs/img/v0.0.2_upload.PNG?raw=true)

pull cvrp service ```/cvrp```

![](https://github.com/christopherpryer/cvrp-app/blob/master/docs/img/v0.0.8.PNG?raw=true)

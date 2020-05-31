![Python package](https://github.com/christopherpryer/cvrp-app/workflows/Python%20package/badge.svg)
[![codebeat badge](https://codebeat.co/badges/10637c50-1887-4bd1-ae4e-1f970d2302de)](https://codebeat.co/projects/github-com-christopherpryer-cvrp-app-master)

# cvrp-app
Development projcet for solving the cvrp problem via containerized microservices & a restful API implementation.

# objectives

- redevelop the [cvrp-app](https://github.com/christopherpryer/cvrp-app) for production-grade requirements
- learn to utilize [Vagrant](https://www.vagrantup.com/) for standard linux development environments
- learn to utilize [docker](https://www.docker.com/)
- build a deployable prototype in python to get going
- refator and optimize using c++
- lean on and learn to contribute to [or-tools](https://github.com/google/or-tools)
- dive deeper into numpy utilization & custom optimizations
- deploy to [DO](https://www.digitalocean.com/)
- complete as modular service for future projects

# development

Initial development will be monolithic type until services can be abstracted. For the meantime use the following process:

1. Test with instance/app.db
2. use init.sh for initial database migrations

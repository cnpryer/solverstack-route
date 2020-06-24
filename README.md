![Python application](https://github.com/andromia/cvrp-app/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

# cvrp-app
Development project for solving the vehicle routing problem via containerized microservices & a restful API implementation. **Note that the first few iterations will be monolithic.** The goal is to identify and abstract services for meaningful improvements.

# CVRP
Stands for **c**apacitated **v**ehicle **r**outing **p**roblem which is a kind of subset of [vrp](https://en.wikipedia.org/wiki/Vehicle_routing_problem). 

## /paintpicture

Using the testing ```.csv``` file as a reference, maybe you are a business that owns multiple stores in the middle of the USA. These stores are spread across several different states (can be 50, 100, 200 miles apart from eachother). It's the beginning of the week and you need to make sure that you fill up those stores with enough inventory for the re-opening of different segments of the country after a pandemic lockdown (economic freeze). Your goal is to come up with a cost-effective way to get all the product from your distribution center and to each store during their business hours or specified loading times (the time window component is technically VRPTW). You have a limited number of trucks and limited budget for driver hours. What do?

# objectives

- redevelop the [cvrp-app](https://github.com/andromia/cvrp-app) for production-grade requirements
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

# demo cvrp-poc
this is how to demo the [proof of concept flask app](https://github.com/pybrgr/cvrp-poc) for this api.

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

![](https://github.com/andromia/cvrp-app/blob/master/docs/img/v0.0.2_upload.PNG?raw=true)

pull cvrp service ```/cvrp```

![](https://github.com/andromia/cvrp-app/blob/master/docs/img/v0.0.8.PNG?raw=true)


# planned cvrp-app backend API v0.1

TODO: server logging for capturing run data.
TODO: abstraction for ```/api/<version>/cvrp``` one-stop endpoint.

# Tables
##  Model

```Model```s are instances of solution designs containing:

  - model_id
  - data_chassis_id

## DataChassis
```DataChassis``` ties together models with their available data.

  - data_chassis_id
  - origin_id
  - demand_id
  - asset_class_id

## Scenarios
```Scenario```s are snapshots of models with different configurations.
TODO: expand on reasoning for this abstraction.

  - scenario_id
  - model_id
  - scenario_name

## Units
```Unit```s are different *unit of measures* used (pallets, weight, miles).
NOTE: haversine vs pcmiler should be abstracted (clustering methods too?).
  - unit_name: 'pallets', 'weight', 'miles'
  - unit_id

## Demand
```Demand``` is each node with capacity to route:

  - demand_id
  - latitude
  - longitude
  - units
  - unit_id 
  - model_id

### manage demand
**endpoint:** /cvrp/demand
**methods:** ```GET```, ```POST```
**```GET``` data expected:**

```json
{ 'model_id': '', 'demand': [ {'demand_id': '', 'latitude': '', 'longitude': '', 'units': '', 'unit_name': ''}, ... ] }
```

**```POST``` data required:**

```json
{
  'latitude': [],
  'longitude': [],
  'units': [],
  'unit_of_measure': ''
}
```

## AssetClass
```AssetClass``` groups vehicles (and other potential assets) together to form a pool of assets available to models.

  - asset_class_id

## Vehicles
```Vehicle```s are resources describing vehicle capacity and number of vehicles:
TODO: expand on how this will scale with additional modeling configurables.

  - vehicle_id
  - max_capacity
  - unit_id
  - asset_class_id

### manage vehicles
**endpoint:** /cvrp/vehicles
**methods:** ```GET```, ```POST```, ```CREATE?```

**```GET``` data expected:**

```json
{ 'vehicles': [ {'vehicle_id': '', 'max_capacity': '', 'unit_name': '', 'asset_class_id': ''}, ... ] }
```

**```POST``` data required:**

```
vehicles = [26, 26, ...] # start with a minimum requirement of having **at least** the same number of vehicles as unique demand points (also lets force the capacities to be the same early on too -- this can change).
```

**```CREATE```**
this creates a default set of vehicles for the model to use.

## Stops
Target output data for cvrp routing (one join with demand at the least).
```Stop```s are output data points that contain:

  - scenario_id
  - vehicle_id
  - stop_num
  - stop_distance
  - unit_id
  - demand_id

### manage stops
this is what the end goal of the service is for our client.
**endpoint:** /cvrp/vehicles/stops
**methods:** ```GET```

**```GET``` data expected:**

```json
{ 'scenario_id': '', 'stops': [ {'vehicle_id': '', 'stop_num': '', 'stop_distance': '', 'unit_name': '', 'demand_id': ''}, ... ] }
```

## Origins
```Origin```s are the node users want to generate routes from (routes are sequences of stops):

  - origin_id
  - latitude
  - latitude

### manage origin
**endpoint:** /cvrp/origin
**methods:** ```GET```, ```POST```
**```GET``` data expected:**

```json
{ 'origin_id': '', 'latitude': '', 'longitude': ''}
```

**```POST``` data required:**

```json
{
  'latitude': '',
  'longitude': ''
}
```
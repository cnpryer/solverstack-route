![Python application](https://github.com/andromia/cvrp-app/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

# cvrp-app
[Under Development] Flask CVRP Backend Web Service API. [Under Development] Flask CVRP Backend Service API. See the [proof of concept flask app](https://github.com/pybrgr/cvrp-poc) for more context.

# MVP
root: ```/api/<version>/```

#  Model

NOTE: how should we abstract run logging?

```Model```s are instances of solution designs containing:

  - ```id```: integer
  - ```name```: string

# Scenario
```Scenario```s are snapshots of models with different configurations.
Models consist of scenarios. Scenarios are projections of the different uses of the resources.

  - ```id```: integer
  - ```model_id```: integer
  - ```name```: string

# Unit
```Unit```s are different *unit of measures* used (pallets, weight, miles).

NOTE: haversine vs pcmiler should be abstracted (clustering methods too?).

  - ```id```: integer
  - ```name```: string ('pallets', 'weight', 'miles')

# Origin
```Origin```s are the node users want to generate routes from (routes are sequences of stops):

  - ```id```: integer
  - ```latitude```: float
  - ```latitude```: float

## Manage Origins
  - **endpoint:** /origin
  - **methods:** ```GET```, ```POST```
  - **```GET``` data expected:**

```json
{
  "id": 0,
   "latitude": 0.,
  "latitude": 0.
}
```

  - **```POST``` data required:**

```json
{
  "latitude": 0.,
  "longitude": 0.
}
```

# Demand
```Demand``` is each node with capacity to route:

  - ```id```: integer
  - ```latitude```: float
  - ```longitude```: float
  - ```units```: float
  - ```unit_id```: integer
  - ```cluster_id```: integer
  - ```model_id```: integer

## Manage Demand
  - **endpoint:** /demand
  - **methods:** ```GET```, ```POST```
  - **```GET``` data expected:**

```json
{
  "id": [],
  "latitude": [],
  "longitude": [],
  "[uom name]": [],
  "cluster_id": [],
  "model_name": ''
}

```
**```POST``` data required:**
```json
{
  "latitude": [],
  "longitude": [],
  "[uom name]": [],
  "cluster_id": [],
  "uom": ''
}
```

## AssetClass
```AssetClass``` groups vehicles (and other potential assets) together to form a pool of assets available to models.

  - ```id```: integer

## Vehicle
```Vehicle```s are resources describing vehicle capacity and number of vehicles:

TODO: expand on how this will scale with additional modeling configurables.

  - ```id```: integer
  - ```max_capacity_units```: integer # could change
  - ```unit_id```: integer
  - ```asset_class_id```: integer

## Manage Vehicles
  - **endpoint:** /vehicles
  - **methods:** ```GET```, ```POST```, ```CREATE```

  - **```GET``` data expected:**

```json
{
  "max_capacity_units": [],
  "[uom name]": []
}
```

  - **```POST``` data required:**

```json
{
  "max_capacity_units": [],
  "uom": ""
}
```

  - **```CREATE```**
This creates a default set of vehicles for the model to use.

## Stop
Target output data for cvrp routing (one join with demand at the least).
```Stop```s are output data points that contain:

  - ```id```: integer
  - ```scenario_id```: integer
  - ```vehicle_id```: integer
  - ```stop_num```: integer
  - ```stop_distance```: float
  - ```unit_id```: integer
  - ```demand_id```: integer

## Manage Stops
This is what the end goal of the service is for our client.
  - **endpoint:** /cvrp/vehicles/stops?
  - **methods:** ```GET```

  - **```GET``` data expected:**

```json
{
  "scenario_name": "",
  "vehicle_id": [],
  "stop_num": [],
  "stop_distance": [],
  "[uom name]": []
}
```

TODO: RPC for results combo or define resource ```Solution```.
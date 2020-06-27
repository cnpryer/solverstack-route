![Python application](https://github.com/andromia/cvrp-app/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

# cvrp-app
[Under Development] Flask CVRP Backend Web Service API. [Under Development] Flask CVRP Backend Service API. See the [proof of concept flask app](https://github.com/pybrgr/cvrp-poc) for more context.

# MVP
root: ```/api/<version>/```

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
  "id": "",
  "latitude": "",
  "latitude": ""
}
```

  - **```POST``` data required:**

```json
{
  "latitude": "",
  "longitude": ""
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
  "model_name": ""
}

```
**```POST``` data required:**
```json
{
  "latitude": [],
  "longitude": [],
  "[uom name]": [],
  "cluster_id": [],
  "uom": ""
}
```

## Vehicle
```Vehicle```s are resources describing vehicle capacity and number of vehicles:

TODO: expand on how this will scale with additional modeling configurables.

  - ```id```: integer
  - ```max_capacity_units```: integer # could change
  - ```unit_id```: integer
  - ```scenario_id```: integer

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

## Solution
```Solution```s define inputs and their outputs via cvrp rpc calls.

  - ```id```: integer
  - ```demand_id```: integer
  - ```origin_id```: integer
  - ```vehicle_id```: float
  - ```stop_num```: integer
  - ```stop_distance_units```: float
  - ```unit_id```: integer

## Manage Solutions
This is what the end goal of the service is for our client.
  - **endpoint:** /solution
  - **methods:** ```GET```

  - **```GET``` data expected:**

```json
{
  "demand_id": [],
  "origin_id": [],
  "vehicle_id": [],
  "stop_num": [],
  "[uom name]": []
}
```
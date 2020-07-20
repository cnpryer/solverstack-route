# solverstack-vrp-rpc

![vrp-rpc](https://github.com/andromia/solverstack-vrp-rpc/workflows/vrp-rpc/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

[**Under Development**] **NOTE**: API is not finalized and **will** change.

**TODO**: add current and future specs/features.

RPC API for logistics optimization web services.

## MVP

```/api/<version>/```

## Main Procedure

- **endpoint**: ```/procedure```
- **methods**: ```GET```, ```POST```
- **input data**:

```json
{
    "origin_latitude": "",
    "origin_longitude": "",
    "unit": "",
    "demand": [ {"latitude": "", "longitude": "", "[unit]": ""} ],
    "vehicle_max_capacity_quantity": "",
    "vehicles_definitions": []
}
```
*[unit]* is defined by *unit* (should be the same value).

```json
"unit": "weight",
"demand": [ {"latitude": "", "longitude": "", "weight": ""} ]
```

*vehicle_max_capacity_quantity* should be the same unit of measure as *unit*.

*vehicles_definitions* (optional) represent both the number of vehicles and their max capacities.

```json
"vehicles_definitions": [26, 26, 26, 26]
```

- **output data**:

```json
{
    "origin_latitude": "",
    "origin_longitude": "",
    "unit": "",
    "demand": [ {"latitude": "", "longitude": "", "[unit]*": "", "cluster_id": "", "vehicle_id": "", "stop_num": ""} ],
    "vehicle_max_capacity_quantity": "",
    "vehicles_definitions": []
}
```

## Usage

- Clone the repository using git clone or download it as a _.zip_ and extract it.
- `cd solverstack-vrp-rpc` or open a terminal in the _solverstack-vrp-rpc_ directory.
- **OPTIONAL** Create a virtual environment using python [venv](https://docs.python.org/3/tutorial/venv.html). This is **preferred** to keep the packages for this project separate.
- Install required packages using `python -m pip install -r requirements.txt`
- Run the flask server using `python manage.py runserver`
- Voila!

### Testing

- You can run the tests using the `pytest` module
- Install dependencies using `python -m pip install -r requirements-dev.txt`
- Run `python -m pytest`

#### (Optional) Using Docker container for testing

You can use a Docker container for running the tests by using the provided _Dockerfile.test_

- Build the Docker image using `docker build -f Dockerfile.test . -t andromia:solverstack-vrp-rpc-test`.
- Run the image using `docker run andromia:solverstack-vrp-rpc-test`

## TODO
- replace ```dict```[key][key]... with ```pandas``` wrappers.

## Other
See [cvrp-poc](https://github.com/fingafrog/cvrp-poc) for demo application.

![](https://github.com/fingafrog/cvrp-poc/blob/master/docs/img/v0.0.8.PNG?raw=true)

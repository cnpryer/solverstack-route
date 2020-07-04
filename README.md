# mds-cvrp-rpc

![Python application](https://github.com/andromia/mds-cvrp-rpc/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

[**Under Development**]

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
    "demand": {
        "demand_id": [],
        "latitude": [],
        "longitude": [],
        "unit": "",
        "quantity": [],
        "cluster": []
    },
    "max_vehicle_capacity_units": "",
    "vehicles": []
}
```

- **output data**:

```json
{
    "origin_latitude": "",
    "origin_longitude": "",
    "demand": {
        "demand_id": [],
        "latitude": [],
        "longitude": [],
        "unit": "",
        "quantity": [],
        "cluster": [],
        "vehicle_id": [],
        "stop_num": []
    },
    "max_vehicle_capacity_units": "",
    "vehicles": []
}
```

## Usage

- Clone the repository using git clone or download it as a _.zip_ and extract it.
- `cd mds-cvrp-rpc` or open a terminal in the _mds-cvrp-rpc_ directory.
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

- Build the Docker image using `docker build -f Dockerfile.test . -t andromia:mds-cvrp-rpc-test`.
- Run the image using `docker run andromia:mds-cvrp-rpc-test`

## TODO
- replace ```dict```[key][key]... with ```pandas``` wrappers.
# solverstack-route

![route](https://github.com/cnpryer/solverstack-route/workflows/route/badge.svg)

[**Under Development**] **NOTE**: API is not finalized and **will** change.

**TODO**: add current and future specs/features.

Service for route module.

## MVP

`/api/<version>/`

## Main Procedure
_NOTE_: `origin` initially will just be a single dictionary. Eventually lists will be accepted.

- **Endpoint**: `/route`
- **Methods**: `POST`
- **Request Syntax**:

```json
{
  "stack_id": <int>,
  "origin": {
    "id": <int>,
    "latitude": <float>,
    "longitude": <float>
  },
  "demand": [
    {
      "id": <int>,
      "latitude": <float>,
      "longitude": <float>,
      "quantity": <int>
    }
  ],
  "unit": <str>,
  "vehicle_max_capacity_units": <int>,

  // **OPTIONAL**
  "vehicle_definitions": [
    <int>
  ]
}
```

*vehicle_max_capacity_units* should be the same unit of measure as *unit*.

*vehicle_definitions* (optional) represent both the number of vehicles and their max capacities.

```json
"vehicle_definitions": [26, 26, 26, 26]
```

- **output data**:

```json
{
  "stack_id": <int>,
  "origin": [{
    "id": <int>,
    "latitude": <float>,
    "longitude": <float>
  }],
  "demand": [{
    "id": <int>,
    "latitude": <float>,
    "longitude": <float>,
    "quantity": <int>
  }],
  "routes": [{
      "id": <int>,
      "cluster_id": <int>,
      "vehicle_id": <int>,
      "stop_num": <int>
  }],
  "unit": <str>,
  "vehicle_max_capacity_units": <int>
}
```

## Usage

- Clone the repository using git clone or download it as a _.zip_ and extract it.
- `cd solverstack-route` or open a terminal in the _solverstack-route_ directory.
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

- Build the Docker image using `docker build -f Dockerfile.test . -t andromia:solverstack-route-test`.
- Run the image using `docker run andromia:solverstack-route-test`

## TODO

- replace `dict`[key][key]... with `pandas` wrappers.

## Other

See [cvrp-poc](https://github.com/cnpryer/cvrp-poc) for demo application.

![Demo Image](https://github.com/cnpryer/cvrp-poc/blob/master/docs/img/v0.0.8.PNG?raw=true)

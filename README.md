![Python application](https://github.com/andromia/cvrp-app-rpc/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

# cvrp-app-rpc
[Under Development] 

RPC API for logistics optimization web service API.

# MVP
```/api/<version>/``` 

# Main Procedure
  - **endpoint**: ```/procedure```
  - **methods**: ```GET```, ```POST```

  - **data**:

```json
{
    "origin_latitude": "",
    "origin_longitude": "",
    "demand": {
        "latitude": [],
        "longitude": [],
        "units": [], // this will change with future iterations
        "unit_name": "",
        "cluster": []
    },
    "vehicles": [] // optional
}
```
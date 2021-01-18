# EODD

## Initial setup

### Bounds

In the bounds folder you will need:

- inner_extent.geojson
- outer_extent.geojson
- DTM.tif

### Plugins

### settings

#### EODataDownBaseConfig.json


#### Sensor config files

Need to edit 

```
        "googleinfo":
        {
            "projectname":"<project name>",
            "googlejsonkey":"<path to json key>"
        },
```

Need to edit

```
        "download":
        {
            "granules":[
                "30UVD"

            ],
            "cloudcover":10,
            "startdate":"2020-09-01"
        },
```
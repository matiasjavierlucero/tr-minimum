# plant-management
 Bio energy plant management system


## Docker 

### Build 

To build the image, execute the next commands:

```bash
make build
```

Result: image with tag: `tecno-red/plant-management:1.0` and `tecno-red/plant-management:latest .`


### Use docker image

```bash
make run
```

Or 

```bash
docker run -d -p 8000:8000 --name plant-management tecno-red/plant-management:1.0
```

## Other commands

- Kill: to delete the current image

> `make kill`

- logs: to see the log

> `make logs`

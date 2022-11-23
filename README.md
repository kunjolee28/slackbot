# Survey Service

### Overview
> Project overview goes here

### Architecture
> Project architecture goes here

### Run Locally
> Go into the `surveyservice` directory in the `cloudrun` directory `/cloudrun/surveyservice`
```sh
cd /cloudrun/surveyservice
```

> Build Docker image and run container

```sh
docker-compose up --build
```

> Visit `http://0.0.0.0:8080/<ENDPOINT>` to view route. E.g. `http://0.0.0.0:8080/version` displays a message showing the version of the application that is live

> Tear down container and remove docker networks when done
```sh
docker-compose down
```

> Note: to remove all images (regardless) which service (in `docker-compose.yaml`) uses it, do the following instead:
```sh
docker-compose down --rmi all
```
# Docker and containers

This folder contains two Docker files, one for the application only and one for a container with Grafana and the application.

* [`Dockerfile`](/code/docker/Dockerfile)
* [`Dockerfile_custom_grafana`](/code/docker/Dockerfile_custom_grafana)

## 1. The `Dockerfile` defines the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** the container
The `Dockerfile` only configures the start of the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** application on port `8081`.

## 2. The `Dockerfile_custom_grafana` defines the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** and `custom  Grafana configuration` in one container

The `Dockerfile_custom_grafana` configures the start of the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** on port `8081` and the `Grafana` application on port `3000`.

Therefore, it uses the `superviord.conf`.

Verification of the running **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** inside the container:

```sh
curl -u ${APP_USER}:${APP_APIKEY} http://0.0.0.0:8081/
cd /var/log/grafana/
```

## 3. Additional information

### 3.1 Reset Podman machine

```sh
podman machine rm podman-machine-default
podman machine init
podman machine start
podman info
```

```sh
brew update
brew upgrade
brew install --cask podman-desktop
```



# Docker and containers

This folder contains two Docker files, one for the application only and one for a container with Grafana and the application.

* [`Dockerfile`](/code/docker/Dockerfile)
* [`Dockerfile_custom_grafana`](/code/docker/Dockerfile_custom_grafana)

## 1. The `Dockerfile` defines the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** the container
The `Dockerfile` only configures the start of the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** application on port `8081`.

## 2. The `Dockerfile_custom_grafana` defines the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** and `custom  Grafana configuration` in one container

The `Dockerfile_custom_grafana` configures the start of the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** on port `8081` and the `Grafana` application on port `3000`.

Therefore, it uses the `superviord.conf`.

Verification of the running **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** inside the container:

```sh
curl -u ${APP_USER}:${APP_APIKEY} http://0.0.0.0:8081/
cd /var/log/grafana/
```

## 3. Additional information

### 3.1 Reset Podman machine

```sh
podman machine rm podman-machine-default
podman machine init
podman machine start
podman info
```

```sh
brew update
brew upgrade
brew install --cask podman-desktop
```




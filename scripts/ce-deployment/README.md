# Automation of the IBM Cloud Code Engine deployment

The automation does:

1. Verify the Container runtime is running
2. Log in to IBM Cloud
3. Build and push the container image to IBM Cloud Container Image Registry (_the container tag is the last GitHub commit id_)
4. Create a new Code Engine project
5. Create an IBM Cloud Container Image Registry access for the Code Engine project
6. Deploys the **`Shelly 3EM`-`Cloudant`-`Grafana`-connection-server** to Code Engine
7. Shows the plain `kubectl` information for the containers in the project
8. Shows the plain `kubectl` log information for the first container
9. Verifies the deployment
10. Set global environment variable for later usage
11. Saves the deployment configurations in the `deployment-log` folders `all` and `last`

## 0. Prerequisites

* IBM Cloud CLI
* IBM Cloud Code Engine Plugin
* IBM Cloud Container Registry Plugin
* [`kubectl` command line](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
* GitHub CLI

```sh
ibmcloud update
ibmcloud plugin list
ibmcloud plugin update container-registry
ibmcloud plugin update container-service
ibmcloud plugin update code-engine
ibmcloud plugin update cloudant
```

## 1. Setup

### 1.1. Clone the project

```sh
git clone https://github.com/thomassuedbroecker/shelly-cloudant-grafana.git
cd shelly-cloudant-grafana
```

### 1.2. Create the needed `.env` files

* Set the `Code Engine` and `IBM Cloud` environment variables

```sh
cat ./scripts/ce-deployment/.env_template >  ./scripts/ce-deploment/.env
```

* Set the environment variables

```sh
cat ./code/.env_template >  ./.env
```

## 2. Run the automation

### 2.1. Run the automation

```sh
cd scripts/ce-deployment
sh deploy-to-code-engine.sh
```

### 2.2. Open your `Code Engine` project in the `IBM Cloud Console`

### 2.3. Open your `configmap` defined for your Code Engine application

### 2.4. Remove the `''` entries in your `configmap` and save the changes

### 2.5. Create a new application configuration, reflect the reason for the change in the name, and save the change

### 2.6. Wait until the application instance is restarted to apply the `configmap` changes

## 3. Redeploy an application based on existing information

You can redeploy an application based on existing information by providing the following information as parameters.


* Repository URL
* Commit ID
* ".env" file with the working configuration 

```sh
export REUSE_COMMAND=reuse
export COMMIT_ID=XXXXXXX
export REPOSITORY_URL=https://github.com/thomassuedbroecker/shelly-cloudant-grafana.git
export ENVIORNMENT_FILENAME=my-restore.env
sh deploy-to-code-engine.sh $REUSE_COMMAND $COMMIT_ID $REPOSITORY_URL $ENVIORNMENT_FILENAME
```
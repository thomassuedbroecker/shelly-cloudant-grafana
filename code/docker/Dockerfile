###############################
# 1. Create a build image
# as BUILDER_IMAGE
FROM python:3.11.2-slim-buster

# Update packages
USER root
RUN apk upgrade libssl3 libcrypto3 libexpat libexpat

# Set directory
WORKDIR /app

# Install needed environment

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install "fastapi[all]"
RUN python3 -m pip install requests
RUN python3 -m pip install pydantic
RUN python3 -m pip install fastapi-utils
RUN python3 -m pip install schedule
RUN python3 -m pip install typing
RUN python3 -m pip install --upgrade "ibmcloudant>=0.0.27"

# Create modeles folder
RUN mkdir modules
RUN python3 -m pip freeze > requirements.txt 

COPY /../requirements.txt /app
COPY /../shelly-3em-cloudant-connector.py /app
COPY /../modules/apis_payload.py /app/modules
COPY /../modules/apis_response_format.py /app/modules
COPY /../modules/load_env.py /app/modules
COPY /../modules/requests_cloudant.py /app/modules
COPY /../modules/requests_ibmcloud_token.py /app/modules
COPY /../modules/requests_shelly_3em.py /app/modules
COPY /../modules/requests_json_grafana_datasource.py /app/modules
COPY /../docker/docker_entrypoint.sh /app
COPY /../docker/generate_env-config.sh /app

###############################
# 2. Create a runtime image
# FROM python:3.11.2

# Install needed environment
# RUN apt-get -y update; apt-get -y install curl

# Install needed environment
# RUN pip3 install --upgrade pip

# Set directory
# WORKDIR /app

RUN addgroup shelly_cloudant_group
RUN useradd shelly_cloudant_user
RUN adduser shelly_cloudant_user shelly_cloudant_group
RUN chown -R shelly_cloudant_user /app

USER shelly_cloudant_user
# Copy sources
# COPY --from=BUILDER_IMAGE /app /app/
RUN ls -a
# RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8081
CMD ["/bin/sh","docker_entrypoint.sh"]
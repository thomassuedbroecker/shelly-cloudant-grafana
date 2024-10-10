# Setup Python environment

1. Set the Python Virtual environment

```sh
python3 -m venv --upgrade-deps shelly-cloudant-grafana-env-3.12
source shelly-cloudant-grafana-env-3.12/bin/activate
```

2. Install Libraries

```sh
python3 -m pip install -r requirements.txt
python3 -m pip install schedule
python3 -m pip install pandas
python3 -m pip freeze > requirements.txt
```
#!/usr/bin/env bash

virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements-tests.txt
nosetests -v --with-cover --cover-erase --cover-package=clickhouse_config_in_zookeeper tests/*.py
#flake8 clickhouse_config_in_zookeeper.py
deactivate

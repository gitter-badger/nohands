#!/usr/bin/bash

PROJ="nohands"

HV="${HOME}/.virtualenvs/$PROJ"
HW="${HOME}/workspace/$PROJ"

export PYTHONPATH="${HW}"

$HV/bin/python3 $HW/bin/$PROJ

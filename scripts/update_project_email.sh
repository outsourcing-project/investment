#!/bin/bash

echo date
source /home/bddyq/envs/investment/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/bddyq/workspace/investment
python /home/bddyq/workspace/investment/scripts/update_project_email.py $@
echo date, 'done'

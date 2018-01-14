#!/bin/bash

echo investment
date
source /home/bddyq/envs/investment/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/bddyq/workspace/investment
python /home/bddyq/workspace/investment/scripts/export_backup_database.py
date
echo 'done'

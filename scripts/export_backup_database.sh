#!/bin/bash

echo investment
date
source /home/yijia/envs/investment/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/jinji/workspace/investment
python /home/yijia/workspace/investment/scripts/export_backup_database.py
date
echo 'done'

#!/bin/bash

echo date
source /home/yijia/envs/investment/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/yijia/workspace/investment
python /home/yijia/workspace/investment/scripts/update_attachment.py $@
echo date, 'done'
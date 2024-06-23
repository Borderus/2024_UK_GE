#!/bin/sh

polling_region='Great Britain'
region_code='gb'
region_list="England,Scotland,Wales,Northern Ireland"
partylist="Conservative,Labour,Liberal Democrats,Reform,UKIP,Green"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

#!/bin/sh

polling_region='Northern Ireland'
region_code='ni'
region_list="Northern Ireland"
partylist="Sinn Fein,DUP,Alliance,Ulster Unionist Party,SDLP"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

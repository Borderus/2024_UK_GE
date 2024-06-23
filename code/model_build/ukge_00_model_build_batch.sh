#!/bin/sh

polling_region='Great Britain'
region_code='gb'
region_list="England,Scotland,Wales,Northern Ireland"
partylist="Conservative,Labour,Liberal Democrats,Reform,UKIP,Green"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

polling_region='Scotland'
region_code='sco'
region_list="Scotland"
partylist="Conservative,Labour,Liberal Democrats,Reform,Green,SNP"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

polling_region='Wales'
region_code='wal'
region_list="Wales"
partylist="Conservative,Labour,Liberal Democrats,Reform,Green,Plaid"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

polling_region='Northern Ireland'
region_code='ni'
region_list="Northern Ireland"
partylist="Sinn Fein,DUP,Alliance,Ulster Unionist Party,SDLP"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_01_polling_averages.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_02_previous_elections.py "$polling_region" "$region_code" "$region_list" "$partylist"
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_03_apply_uniform_swing.py "$polling_region" "$region_code" "$region_list" "$partylist"

python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_04_combine_regions.py
python /home/ubuntu/Documents/2024_UK_GE/code/model_build/ukge_05_run_model.py

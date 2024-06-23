from pandas import DataFrame, Series
import pandas as pd
import numpy as np

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

# Loop through reading in inputs
# Set up some variables in advance
suffix_list = ['gb', 'ni', 'sco', 'wal']
projections = {}
deviations = {}
proj_cols = pd.Index([])
proj_ind = pd.Index([])
# Begin loop
for value in suffix_list:
  # Read in each regional dataframe into a dictionary to later concatenate  
  projections[value] = pd.read_pickle(f"{projectfolder}/datasets/projected_seat_state_{value}.pickle")

  # Read in each regional deviation into a dictionary to later concatenate
  deviations[value] = pd.read_pickle(f"{projectfolder}/datasets/historic_std_{value}.pickle")

  proj_cols = proj_cols.union(projections[value].columns)
  proj_ind = proj_ind.union(projections[value].index)

# Drop regional outcomes from gb
projections['gb'] = projections['gb'].drop(projections['sco'].index).drop(projections['wal'].index).drop(projections['ni'].index)

# Create table with all seat projections
projections = pd.concat(projections)

# Get the table key from the records, use as a region key
projections = projections.reset_index(level=0).rename(columns={'level_0': 'region'})
# print(projections)

# Create table with all deviations, drop table key
deviations = pd.concat(deviations).reset_index().drop(columns='level_1').rename(columns={'level_0': 'region'})
# print(deviations)

# Create table with deviations for each seat
seat_devs = projections.reset_index()[['Constituency','region']].merge(deviations, how='left', on='region').set_index('Constituency')
# print(seat_devs)

# Write out to Pickle
projections.to_pickle(f"{projectfolder}/datasets/latest/seat_projections.pickle")
deviations.to_pickle(f"{projectfolder}/datasets/latest/deviations_region.pickle")
seat_devs.to_pickle(f"{projectfolder}/datasets/latest/deviations_seat.pickle")

# Write out to csv
projections.to_csv(f"{projectfolder}/output/seat_projections.csv")
deviations.to_csv(f"{projectfolder}/output/deviations.csv")
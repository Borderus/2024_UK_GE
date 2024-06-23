from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import sys

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

# Set regional values
polling_region = sys.argv[1]
region_code = sys.argv[2]
region_list = sys.argv[3].split(',')
partylist=sys.argv[4].split(',')

# Read inputs
previous_result = pd.read_pickle(f"{projectfolder}/datasets/previous_result_{region_code}.pickle")
previous_result_headline = pd.read_pickle(f"{projectfolder}/datasets/prev_election_headline_{region_code}.pickle")
polling_averages = pd.read_pickle(f"{projectfolder}/datasets/polling_averages_{region_code}.pickle")

# Get most recent average
current_state = polling_averages[:1]

# Check for an empty state - this can happen with NI
statecheck = current_state.sum(axis=1)[0]

# From this and the most recent election result, get swing. If the current state is empty, we assume no swing
if statecheck != 0:
  swing = current_state - previous_result_headline.values
else:
  swing = current_state

# Then add this to the individual seats
projected_seat_state = previous_result + swing.values

projected_seat_state.to_pickle(f"{projectfolder}/datasets/projected_seat_state_{region_code}.pickle")
# print(projected_seat_state)

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
historic_results = pd.read_csv(f"{projectfolder}/input/Previous Elections/All Constituency General Election Results.csv")
modern_boundary_prev_result = pd.read_excel(f"{projectfolder}/input/Previous Elections/results_spreadsheet.ods", sheet_name="2__results")
geography = pd.read_pickle(f"{projectfolder}/datasets/geography.pickle")
current_geography = geography[geography['Election Year']==2024][['Constituency', 'Country']]
geography = geography[['Boundary Year', 'Constituency', 'Country']]

# Convert odd party names 
party_map = {'The Brexit Party': 'Reform', 'UK Independence Party (UKIP)': 'UKIP', 'Green Party': 'Green', 'Plaid Cymru': 'Plaid', 
             'Sinn Féin': 'Sinn Fein'}

def conv_party(x):
  result = party_map.get(x, x)
  return result

historic_results['Party'] = historic_results['Party'].map(conv_party)

# *** Get election headlines ***

# Restrict results on region
historic_results = historic_results.merge(geography, on=['Boundary Year', 'Constituency'], how='left')
historic_results = historic_results[historic_results['Country'].isin(region_list)]

# Aggregate seat-levels into national totals
historic_results_tot = historic_results.groupby(['Election Year', 'Party'])['Votes'].sum()
historic_votes_tot = historic_results.groupby(['Election Year'])['Votes'].sum()
historic_results_pct = 100*historic_results_tot.divide(historic_votes_tot)
results_to_date = historic_results_pct.unstack(level=1)

# *** Get 2019 totals ***
prev_election_headline = results_to_date[partylist][-1:]

# *** Get std dev of historic polls ***
# TODO: Check if this is really the deviation we're using
historic_std = results_to_date.std().fillna(2).to_frame().T[partylist]

# *** Format modern_boundary_prev_result to match other tables ***

# Create lookup to change column names and change them
correct_names = {'Conv': 'Conservative', 'Labv': 'Labour', 'LDv': 'Liberal Democrats', 'SNPv': 'SNP',
                 'PCv': 'Plaid', 'Brxv': 'Reform', 'UKIPv': 'UKIP', 'Grnv': 'Green', 'SFv': 'Sinn Fein',
                 'DUPv': 'DUP', 'APNIv': 'Alliance', 'UUPv': 'Ulster Unionist Party', 'SDLPv': 'SDLP'}
modern_boundary_prev_result = modern_boundary_prev_result.rename(columns=correct_names)

# Restrict records by region
modern_boundary_prev_result = modern_boundary_prev_result.rename(columns={'Boundary Comm name': 'Constituency'}).merge(current_geography, on=['Constituency'], how='left')
modern_boundary_prev_result = modern_boundary_prev_result[modern_boundary_prev_result['Country'].isin(region_list)]

# Set constituency name as an index
modern_boundary_prev_result = modern_boundary_prev_result.set_index('Constituency')

# Restrict columns to partylist
modern_boundary_prev_result = modern_boundary_prev_result[partylist]

# Get total number of votes between these
modern_boundary_totals = modern_boundary_prev_result.sum(axis=1)

# Get percentages
modern_boundary_prev_result_pct = 100*modern_boundary_prev_result.divide(modern_boundary_totals, axis=0)

# *** Write out ***
prev_election_headline.to_pickle(f"{projectfolder}/datasets/prev_election_headline_{region_code}.pickle")
historic_std.to_pickle(f"{projectfolder}/datasets/historic_std_{region_code}.pickle")
modern_boundary_prev_result_pct.to_pickle(f"{projectfolder}/datasets/previous_result_{region_code}.pickle")


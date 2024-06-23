from pandas import DataFrame, Series
import pandas as pd
import numpy as np

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

# Set no. of runs
runs = 10000

# Read inputs

projections = pd.read_pickle(f"{projectfolder}/datasets/latest/seat_projections.pickle").drop(columns='region')
seat_devs = pd.read_pickle(f"{projectfolder}/datasets/latest/deviations_seat.pickle").drop(columns='region')

# Define prerequisite functions

# Seatdev - Seat Deviation - a deviation with mean 0 and std equal to average deviation at past elections
def rand_seatdev(value):
  return np.random.normal(0, value)

# Winflag - Convert percentages to 1s and 0s
def get_winflag(row):
  return np.floor(abs(row.divide(row.max())))

# *** RUN MODEL ***

# Create dictionary to store results
outcome_dict = {}

# Begin loop
for i in range(runs):
  # Create dataframe for geographic deviation  
  geo_dev = DataFrame(np.random.normal(0,4,(seat_devs.index.size, seat_devs.columns.size)), index=seat_devs.index, columns=seat_devs.columns)
  # Derive random components from seat deviation and geographic  
  random_comp = seat_devs.apply(rand_seatdev) + geo_dev
  
  # Get vote outcome from applying this component to the calculated vote  
  vote_outcome_raw = projections + random_comp
  # Apply the get winflag function to convert tables to ones and zeros  
  vote_outcome_raw = vote_outcome_raw.apply(get_winflag, axis=1)
  # Add to outcome dictionary  
  outcome_dict[i] = vote_outcome_raw

# Concatenate results together
outcome_votes = pd.concat(outcome_dict).groupby('Constituency').mean()
# print(outcome_votes)

# *** BREAKDOWN OF RESULTS ***

# Get weight of win
# Rules are:
#   - Safe     >90%
#   - Likely   80-90%
#   - Lean     EITHER: 70-80%
#                  OR: 60-80% and 3 parties on at least 10% of vote
#   - Toss-up  Other

# Strategy is to resolve most with bins, then handle unusual toss-up strategy

# First type - Bins
bins = [0, 0.7, 0.8, 0.9, 1]
names = ['', 'Lean', 'Likely', 'Safe']

likelihood = DataFrame(pd.cut(outcome_votes.max(axis=1), bins, labels=names), columns=['check1'])

# Second type - 3 parties and 10%
def check_lean(row):
  partycount = row[row>= 0.1].size
  if partycount > 2:
    partyflag = 1
  else:
    partyflag=0
  leanflag = (row.max()>=0.6)*partyflag
  if leanflag:
    return 'Lean'
  else:
    return ''
  
likelihood['check2'] = outcome_votes.copy().apply(check_lean, axis=1)

# Then the default value:
likelihood['check3'] = 'Toss-up'

# Define a function to get preferred column
def get_likelihood(row):
  if row['check1']!='':
    return row['check1']
  elif row['check2']!='':
    return row['check2']
  else:
    return row['check3']
  
# And results column:
likelihood['Likelihood'] = likelihood.apply(get_likelihood, axis=1)

# Merge back into outcomes
outcome_votes = outcome_votes.join(likelihood['Likelihood'], how='left')

print(outcome_votes)
# print(vote_outcome_raw['Likelihood'].drop_duplicates())

# Keep raw outcomes, create copy for final output
outcome_headline = outcome_votes.copy()

# Get winning party
outcome_headline['Winner'] = outcome_votes.select_dtypes(include='number').idxmax(axis=1)
print(outcome_headline)
outcome_headline['Winner_Final'] = np.where(outcome_headline['Likelihood']=='Toss-up', '',outcome_votes.select_dtypes(include='number').idxmax(axis=1))

# Set the Speaker's Constituency
outcome_headline.loc['Chorley', 'Winner'] = 'Speaker'
outcome_headline.loc['Chorley', 'Likelihood'] = 'Safe'

# Print out summaries
print(outcome_headline.reset_index().groupby(['Winner'])['Constituency'].count())
print(outcome_headline.reset_index().groupby(['Winner', 'Likelihood'])['Constituency'].count())
print(outcome_headline.reset_index().groupby(['Winner_Final', 'Likelihood'])['Constituency'].count())

# Write out
outcome_headline.to_csv(f"{projectfolder}/output/results.csv")
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

polling = pd.read_csv(f"{projectfolder}/input/Polling/Voting Intention Polling.csv")
weighting = pd.read_csv(f"{projectfolder}/input/Polling/Pollster Ratings.csv")

# Convert End Date to datetime ahead of making it an index
polling['End Date'] = polling.loc[:, ['End Date']].apply(pd.to_datetime,format='%Y-%m-%d')

# Restrict records to area=United Kingdom
polling = polling[(polling['Area']=='Great Britain')]

# Add pollster score
polling = polling.merge(weighting, on='Pollster', how='left')

# Turn weighting into a percentage
polling['wt'] = polling['Score']/100

# Halve weighting for commissioned polls 
polling['wt'] = np.where(polling['Client'].isna(), polling['wt'], polling['wt']/2)

# Create weighted voting intention
polling['wt_int'] = (polling['Voting Intention']*polling['wt'])

# Convert odd party names 
party_map = {'Reform UK': 'Reform', 'UK Independence Party (UKIP)': 'UKIP', 'Green Party': 'Green', 'Plaid Cymru': 'Plaid'}

def conv_party(x):
  result = party_map.get(x, x)
  return result

polling['Party'] = polling['Party'].map(conv_party)
polling['Party'] = polling['Party'].rename({'End Date': 'Date'})

# Restrict columns in weight table and unstack to create party-level columns
poll_wt = polling[['Party', 'Start Date', 'End Date', 'Pollster', 'Client', 'wt']]
poll_wt = poll_wt.set_index(['Party', 'Start Date', 'Pollster', 'Client', 'End Date']).unstack(level=0)
poll_wt = poll_wt.reset_index(['Start Date', 'Pollster', 'Client'])
poll_wt.columns = poll_wt.columns.droplevel(0)
poll_wt = poll_wt.drop(columns=['']).sort_index(ascending=False)

# Restrict columns in weighted intention table and unstack to create party-level columns
poll_wt_int = polling[['Party', 'Start Date', 'End Date', 'Pollster', 'Client', 'wt_int']]
poll_wt_int = poll_wt_int.set_index(['Party', 'Start Date', 'Pollster', 'Client', 'End Date']).unstack(level=0)
poll_wt_int = poll_wt_int.reset_index(['Start Date', 'Pollster', 'Client'])
poll_wt_int.columns = poll_wt_int.columns.droplevel(0)
poll_wt_int = poll_wt_int.drop(columns=['']).sort_index(ascending=False)

# Calculate rolling averages
duration = "14D"
wt_int_sum = poll_wt_int[::-1].rolling(duration).sum()
wt_sum = poll_wt[::-1].rolling(duration).sum()
int_index = wt_int_sum.divide(wt_sum)

# Sort and dedupe table
polling_avg = int_index.sort_index(ascending=False)
polling_avg = polling_avg[polling_avg.index.duplicated()==False]

# Reduce columns in use
partylist=['Conservative', 'Labour', 'Liberal Democrats', 'SNP', 'Plaid', 'Reform', 'UKIP', 'Green']
polling_avg = polling_avg[partylist]

# Rename index
polling_avg = polling_avg.reset_index('End Date').rename(columns={'End Date': 'Date'}).set_index('Date')

# Write out
polling_avg.to_pickle(f"{projectfolder}/datasets/polling_averages.pickle")
# print(polling_avg)

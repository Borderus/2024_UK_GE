from pandas import DataFrame, Series
import pandas as pd
import numpy as np

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

# Read in raw data
const_to_county = pd.read_csv(f"{projectfolder}/input/Geography/Constituency to County Lookup.csv")
county_to_region = pd.read_csv(f"{projectfolder}/input/Geography/County to Region Lookup.csv")

# Create a country lookup
country_lookup = {}
for value in county_to_region['Government Office Region'].drop_duplicates():
    if value not in ['Scotland', 'Northern Ireland', 'Wales']:
        country_lookup[value] = 'England'
    else:
        country_lookup[value] = value

# Join tables
geography = const_to_county.merge(county_to_region, on='County', how='left')

# Tidy up region name
geography = geography.rename(columns={'Government Office Region': 'Region'}).drop(columns='County Type')

# Create country column
geography['Country'] = geography['Region'].map(country_lookup)

# Dedupe
geography = geography.drop_duplicates()

# Write out
geography.to_pickle(f"{projectfolder}/datasets/geography.pickle")
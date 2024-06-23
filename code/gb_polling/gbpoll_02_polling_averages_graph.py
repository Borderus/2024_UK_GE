from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

projectfolder = "/home/ubuntu/Documents/2024_UK_GE"

# Read in polling average data
polling_avg = pd.read_pickle(f"{projectfolder}/datasets/polling_averages.pickle")
# Stack the data into a columnar fashion
# TODO: We don't need to stack and unstack (when graphing)
polling_avg = polling_avg.stack().reset_index(level=[0,1]).rename(columns={0: 'voter_int'})
# Get a list of parties, from which to create lines
party_list = polling_avg['Party'].drop_duplicates()

# print(party_list)
# print(polling_avg)

# Create plot
plot = figure(title='Polling Averages', width=1800, x_axis_type='datetime')

# Assign party colours
colours = {'Conservative': '#0087DC',
           'Labour': '#D50000',
           'Liberal Democrats': '#FDBB30',
           'SNP': '#FFF95D',
           'Plaid': '#3F8428',
           'Reform': '#1ECBE1',
           'Green': '#008066',
           'UKIP': '#EFE600'}
 
#  Party list loop
for party in party_list:
    temp_frame = polling_avg[polling_avg['Party'] == party]
    source=ColumnDataSource(data=temp_frame)
    plot.line(x='Date', y='voter_int', line_color=colours[party], legend_label=party, line_width=2, source=source)

# Set legend location
plot.legend.location='center'
plot.add_layout(plot.legend[0], 'right')
# Set legend to hide values when clicked on
plot.legend.click_policy='hide'

# show(plot)

# Write out to final location
output_file(filename=f"{projectfolder}/output/graphs/polling_avg.html")
save(plot)
#! /usr/bin/env python3

"""
Reads the DMR data from the 'data' folder and generates box-plots for each quarter.
This process is repeated for each measured parameter, ie lead, pH, etc. and then
saved to the 'figures' folder.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/CLR DMR.csv")

# cast 'Date' column as dates
df['Date'] = pd.to_datetime(df['Date'])
# Get our seasons
# winter = df.loc[df['Date'].dt.month==2]
# spring = df.loc[df['Date'].dt.month==5]
# summer = df.loc[df['Date'].dt.month==8]
# fall = df.loc[df['Date'].dt.month==11]

# Make these new fields instead and work on main dataframe

# What does work:
# df.boxplot(column='Value',by='Location') -> ax.figure.savefig()

# What so far has not:
# fig,ax = plt.subplots() -> ax.boxplot(series) -> fig.savefig()

# Always call plt.cla() + plt.clf()

# solution for by-location:
# for param:
# df.boxplot(column='Value',by='Location',showfliers=False,)
# plt.cla() plt.clf()

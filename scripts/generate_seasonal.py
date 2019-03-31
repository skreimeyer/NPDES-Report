#! /usr/bin/env python3

"""
Reads the DMR data from the 'data' folder and generates box-plots for each quarter.
This process is repeated for each measured parameter, ie lead, pH, etc. and then
saved to the 'figures' folder.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/CLR DMR.csv")

params = df['Parameter'].unique()
# cast 'Date' column as dates
df['Date'] = pd.to_datetime(df['Date'])
#make a 'Seasons' column
seasonmap = {2:'Winter',5:'Spring',8:'Summer',11:'Fall'}
df['Season'] = df['Date'].dt.month # intermediate step
df['Season'] = df['Season'].apply(lambda x: seasonmap[x])

# Make these new fields instead and work on main dataframe
# Main loop
# for p in params:
#     localframe = df.loc[df['Parameter']==p]
#     unit = localframe.iloc[1]['Unit']
#     # make seasonal graph
#     ax = localframe.boxplot(column='Value',by='Season')
#     ax.figure.savefig(f'../figures/seasonal-{p}.png')
#     plt.cla()
#     plt.clf()
#     # make location graph
#     ax = localframe.boxplot(column='Value',by='Location')
#     ax.figure.savefig(f'../figures/seasonal-{p}.png')
#     plt.cla()
#     plt.clf()
# OK UP TO HERE ^^^
#     # Now the time-series
#     fig1,ax1 = plt.subplots(figsize=(6,4),dpi=300)
#     ax1.set_title(f'Time-Series Analysis of {p} Within MS4',size=24)
#     ax1.set_ylabel(f'{unit}')
#     ax1.set_xlabel('Date')
#     medians = localframe.groupby('Date').median()
#     smoothed_medians = signal.savgol_filter(medians,51,3)





# What does work:
# df.boxplot(column='Value',by='Location') -> ax.figure.savefig()

# What so far has not:
# fig,ax = plt.subplots() -> ax.boxplot(series) -> fig.savefig()

# Always call plt.cla() + plt.clf()

# solution for by-location:
# for param:
# df.boxplot(column='Value',by='Location',showfliers=False,)
# plt.cla() plt.clf()

#! /usr/bin/env python3

"""
Reads the DMR data from the 'data' folder and generates box-plots for each quarter.
This process is repeated for each measured parameter, ie lead, pH, etc. and then
saved to the 'figures' folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

import numpy as np

import pdb

df = pd.read_csv("../data/CLR DMR.csv")

params = df['Parameter'].unique()
# cast 'Date' column as dates
df['Date'] = pd.to_datetime(df['Date'])
#make a 'Seasons' column
seasonmap = {2:'Winter',5:'Spring',8:'Summer',11:'Fall'}
df['Season'] = df['Date'].dt.month # intermediate step
df['Season'] = df['Season'].apply(lambda x: seasonmap[x])

# Main loop
for p in params: # FIXME
# for p in params:
    localframe = df.loc[df['Parameter']==p]
    unit = localframe.iloc[1]['Unit']
    # make seasonal graph
    ax = localframe.boxplot(
    column='Value',
    by='Season',
    showfliers=False)
    ax.set_title(f'Seasonal Distribution for {p}')
    ax.set_ylabel(unit)
    plt.suptitle("") #  clear the automatic title
    ax.figure.savefig(f'../figures/seasonal-{p}.png')
    plt.cla()
    plt.clf()
    # make location graph
    ax = localframe.boxplot(
    column='Value',
    by='Location',
    showfliers=False)
    ax.set_title(f'Regional Distribution for {p}')
    ax.set_xticklabels(["01","02","03","06","05"]) # readable labels
    ax.set_ylabel(unit)
    plt.suptitle("") # clear the automatic title
    ax.figure.savefig(f'../figures/regional-{p}.png')
    plt.cla()
    plt.clf()
    # Now the time-series
    fig1,ax1 = plt.subplots(figsize=(6,4),dpi=300)
    ax1.set_title(f'Time-Series Analysis of {p} Within MS4',size=14)
    ax1.set_ylim(localframe['Value'].quantile(0.05),localframe['Value'].quantile(0.95)) # upper limit
    ax1.set_ylabel(f'{unit}')
    ax1.set_xlabel('Date')
    locations = localframe['Location'].unique()
    medians = localframe.groupby('Date').median()
    smoothed_medians = signal.savgol_filter(medians['Value'],31,5)
    x_vals = localframe['Date'].unique() # order preserved. Groupby instead?
    ax1.plot(x_vals,smoothed_medians,color="yellow",alpha=0.75,lw=1,zorder=1.0)
    ax1.plot(x_vals,smoothed_medians,color="black",linestyle="--",alpha=0.75,label="Median",lw=1,zorder=1.1)
    for l in locations:
        y_vals = localframe.loc[localframe['Location']==l]['Value']
        ax1.scatter(x_vals,y_vals,marker="+",label=l)
    plt.legend(loc=2,fontsize=5)
    fig1.savefig(f'../figures/time-series-{p}.png')

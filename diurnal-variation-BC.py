import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/slcp_2019-2021_raw.csv', index_col=0, parse_dates=True)
# Change column name of BC to BC1h
df.rename(columns={'BC': 'BC1h'}, inplace=True)
# Load 10 min BC data
bc10m = pd.read_csv('data/BC10m2.csv', index_col=0, parse_dates=True)
bc10m = bc10m[['BC']]
bc10m = bc10m.resample('H').mean()

# Concatenate 10 min BC data to df
df = pd.concat([df, bc10m], axis=1)

# Filter data
year = 2019
df = df.loc[df.index.year == year]
species = 'BC'
# species = 'PM2.5'

# Calculate daily BC mean
df['daily'] = df.groupby(df.index.date)[species].transform('mean')
df['hourly/dailymean'] = df[species] / df['daily']

# Create a 2D array of Monthly average of each local time BC, x axis is month, y axis is hour
bc_mean = df.groupby([df.index.hour, df.index.month])['hourly/dailymean'].mean().unstack()

# Plot
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
im = ax.imshow(bc_mean, cmap='jet', vmin=0, vmax=1.5, aspect='auto')
ax.set_xticks(range(0,12, 1))
ax.set_xticklabels(range(1, 13, 1))
ax.set_yticks(bc_mean.index[::2])
ax.set_yticklabels(bc_mean.index[::2])
ax.set_xlabel('Month')
ax.set_ylabel('Local time (Hour)')
ax.set_title('Diurnal variations of '+ species + ' in ' + str(year))

# Add a colorbar
cbar = ax.figure.colorbar(im, ax=ax, label='Local time conc. per diurnal average')
cbar.ax.tick_params(labelsize=10)

plt.tight_layout()
plt.show()
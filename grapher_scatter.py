import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from color_line import colored_line
from matplotlib.collections import LineCollection

# Import data from CSV
stock_data = pd.read_csv("stock_data/all_data.csv", index_col=0, parse_dates=True)
stock_data = stock_data.rename_axis('Date').reset_index()

# Get data
data_wanted = 'Close'
data = stock_data[data_wanted]

# Assign colormap
cmap = clr.LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#2FFF00-FF0600
    (0.000, (0.184, 1.000, 0.000)),
    (1.000, (1.000, 0.024, 0.000))))


# Track whether price is going up or down and assign a 0 or 1 depending on price direction
tracker = [1]
for i in range(1, len(data)):
    curr = data[i]
    prev = data[i-1]

    if curr > prev:
        tracker.append(0)
    else:
        tracker.append(1)


# Count how many times the price went either way for each spike/dip
bundles = []
count = 1
for i in range(1, len(tracker)):
    if tracker[i] == tracker[i-1]:
        count += 1
    else:
        bundles.append((tracker[i-1], count))
        count = 1
bundles.append((tracker[-1], count))    # Append last bundle


# Calculate a fading color from 0 'green to 1 'red' dependent on the size of the number in bundles
cm = []
total = 0
for trend, length in bundles:
    if trend == 0:
        if length == 1:
            color_range = [0]
        else:
            color_range = np.linspace(0.5, 0, length)
    else:
        if length == 1:
            color_range = [1]
        else:
            color_range = np.linspace(0.5, 1, length)

    cm.extend(color_range)


# Plot as a scatterplot (Mainly used early stage to implement colormap on graph
plt.scatter(stock_data['Date'], data, cmap=cmap, c=cm)
plt.plot(stock_data['Date'], data)

# Display the plots to user
plt.show()

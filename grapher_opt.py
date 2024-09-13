import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.collections import LineCollection
import math
import time

time_start = time.time()

stock_data = pd.read_csv("stock_data/all_data.csv", index_col=0, parse_dates=True)
stock_data = stock_data.rename_axis('Date').reset_index()

# Get data
data_wanted = 'Close'
data = stock_data[data_wanted].to_numpy()


n = 5

# Assign colormap
cmap = clr.LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#10:2FFF00-25:7BF75E-75:EE504D-90:FF0600
    (0.000, (0.184, 1.000, 0.000)),
    (0.100, (0.184, 1.000, 0.000)),
    (0.250, (0.482, 0.969, 0.369)),
    (0.750, (0.933, 0.314, 0.302)),
    (0.900, (1.000, 0.024, 0.000)),
    (1.000, (1.000, 0.024, 0.000))))

"""
# Non-permanent fix to display x-axis on subplot
nl = []
for i in range(len(stock_data[data_wanted])):
    nl.append(i)

# Create a figure and plot the line on it

lines = colored_line(nl, stock_data[data_wanted], cm, ax1, linewidth=1, cmap=cmap)
"""

fig1, ax1 = plt.subplots()


# Compute trends using numpy
tracker = np.where(data[1:] > data[:-1], 0, 1).tolist()  # 0 for up, 1 for down

changes = np.diff(tracker, prepend=tracker[0])

print(tracker)
print(changes.tolist())

bundles1 = np.split(tracker, )

# Count how many times the price went either way for each spike/dip
bundles = []
count = 1
for i in range(1, len(tracker)):
    if tracker[i] == tracker[i-1]:
        count += 1
    else:
        bundles.append([tracker[i-1], count])
        count = 1
bundles.append([tracker[-1], count])    # Append last bundle

for i in range(len(bundles)):
    bundles[i][1] = bundles[i][1] * n

# Calculate a fading color from 0 'green to 1 'red' dependent on the size of the number in bundles
cm = []
total = 0
for trend, length in bundles:
    length1 = math.floor(int(length) * 1 / 10)
    length2 = math.ceil(int(length) * 9 / 10)
    if trend == 0:
        if length == 1:
            color_range = [0]
        else:
            color_range1 = np.linspace(1, 0.5, length1)
            color_range2 = np.linspace(0.5, 0, length2)
    else:
        if length == 1:
            color_range = [1]
        else:
            color_range1 = np.linspace(0, 0.5, length1)
            color_range2 = np.linspace(0.5, 1, length2)

    cm.extend(color_range1)
    cm.extend(color_range2)

def interpolate(data_list, n):
    datax = []
    datay = []
    for i in range(len(data_list)-1):
        x = np.linspace(i, i+1, n).tolist()
        y = np.linspace(data_list[i], data_list[i+1], n).tolist()

        datax = datax + x
        datay = datay + y
    return datax, datay

datax, datay = interpolate(data, n)


segments = []
for i in range(len(datax)-1):
    curr = (datax[i], datay[i])
    next = (datax[i+1], datay[i+1])

    segments.append([curr, next])

segments = np.array(segments)

lc = LineCollection(segments, linewidths=2, array=cm, cmap=cmap)
ax1.add_collection(lc)

# Set axis limits of line plot
ax1.set_xlim(0, len(data))
ax1.set_ylim(0, 225)

time_end = time.time()
time_diff = time_end - time_start
print("Code elapsed in:", time_diff)

# Display the plots to user
plt.show()






import pandas as pd     # Used to handle data gotten from yfinance
import numpy as np      # Used to handle data - Works well with matplotlib
import math             # Primarily used to round numbers
import glob             # Glob
import os               # File handling


# Function to convert the wanted data from CSV to a nested array
def all_csv_tolist(directory="stock_data", data_wanted="Close"):
    csv_files = glob.glob(directory + "/*.csv")     # Get all CSV file names in directory

    data = []   # Empty list to store all wanted data
    # Get the wanted data from each file and save it to data
    for i in range(len(csv_files)):
        curr_data = csv_files[i]    # Get name for current stock

        # Read the file CSV file
        stock_data = pd.read_csv(curr_data, index_col=0, parse_dates=True)
        stock_data = stock_data.rename_axis('Date').reset_index()   # Leftover code from when dates was on graphs

        # Get data from DataFrame and save it to the data list
        data.append(np.array(stock_data[data_wanted]))

    return data


# Function to delete CSV files after the code has been used to "weed out" errors from old files
def delete_old_csv(directory="stock_data"):
    csv_files = glob.glob(directory + "/*.csv")  # Get all files in directory

    # Delete all files
    for f in csv_files:
        os.remove(f)


# Function to get the x and y interval to be displayed on a graph
def axis_definer(graph_data):
    # x-axis
    x_lim = [0, len(graph_data)]

    # Get max and min of data
    data_max = np.max(graph_data)
    data_min = np.min(graph_data)

    # Threshold of +- 10 unless the graph would end up displaying less than 0 on y-axis
    y_lim = [0 if data_min-10 < 0 else data_min-10, data_max+10]

    return x_lim, y_lim


# Function to interpolate a line segment into multiple line segments to apply gradient
# Could probably be done more efficient with np.interpolate
def interpolate(data_list, n):
    # empty lists to store data
    data_x = []
    data_y = []

    # Interpolate data with np.linspace() function
    for i in range(len(data_list)-1):
        x = np.linspace(i, i+1, n).tolist()
        y = np.linspace(data_list[i], data_list[i+1], n).tolist()

        # Add the interpolated data to the lists
        data_x = data_x + x
        data_y = data_y + y
    return data_x, data_y


# Function that calculates a list of numbers to use to plot a colormap on each line segment to add a gradient
def color_fade_calculator(data, n=5):
    # Track which way the trend is going and add it to a list
    tracker = []
    for i in range(1, len(data)):
        curr = data[i]
        prev = data[i-1]

        if curr > prev:
            tracker.append(0)
        else:
            tracker.append(1)

    # Count how many times the price went either trend direction
    bundles = []
    count = 1
    for i in range(1, len(tracker)):
        if tracker[i] == tracker[i-1]:
            count += 1
        else:
            bundles.append([tracker[i-1], count])
            count = 1
    bundles.append([tracker[-1], count])    # Append last bundle

    # Multiply with amount of times the graph should be interpolated in each line segment
    for i in range(len(bundles)):
        bundles[i][1] = bundles[i][1] * n

    # Calculate a fading color from 0 'green to 1 'red' dependent on the size of the number in bundles
    cm = []
    for trend, length in bundles:
        # This is a workaround to make the graph be the opposite colour in the beginning to give a smooth transition
        length1 = math.floor(int(length) * 1 / 10)
        length2 = math.ceil(int(length) * 9 / 10)
        if trend == 0:
            color_range1 = np.linspace(1, 0.5, length1)
            color_range2 = np.linspace(0.5, 0, length2)
        else:
            color_range1 = np.linspace(0, 0.5, length1)
            color_range2 = np.linspace(0.5, 1, length2)

        cm.extend(color_range1)
        cm.extend(color_range2)

    return cm


# Function to calculate line segments to be added to a line-collection in matplotlib
def segment_calculator(data, n=5):
    data_x, data_y = interpolate(data, n)   # Interpolate all data

    segments = []   # Empty list to store line segments
    # Create line segments as nested lists defining two points for each line
    for i in range(len(data_x) - 1):
        curr = (data_x[i], data_y[i])   # Starting point
        next_one = (data_x[i + 1], data_y[i + 1])   # Ending point (next is build in)

        # Create the line segments
        segments.append([curr, next_one])

    return np.array(segments)


# Function to calculate a dynamical grid layout depending on the amount of data
# Function will try to make a ratio where the width is never bigger than the height + 2
def grid_layout(data):
    data_amount = len(data)     # Get the amount that needs to be plotted
    height = 1      # Minimum starting height
    while True:
        max_width = height - 1      # Width to height ratio
        width = math.floor(data_amount/height)  # Try width for this height
        if data_amount % height != 0:
            width += 1  # Add one to width if all graphs aren't plotted
        if width > max_width:
            height += 1     # Add one to height if all graphs aren't plotted
        else:
            break   # Break the loop if all conditions are satisfied

    return width, height

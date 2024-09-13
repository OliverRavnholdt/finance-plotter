import pandas as pd
import numpy as np
import math
import glob
import os


def all_csv_tolist(directory="stock_data", data_wanted="Close"):
    csv_files = glob.glob(directory + "/*.csv")

    data = []
    for i in range(len(csv_files)):
        curr_data = csv_files[i]
        curr_data_name = csv_files[i].split("\\")[1].split(".")[0]

        stock_data = pd.read_csv(curr_data, index_col=0, parse_dates=True)
        stock_data = stock_data.rename_axis('Date').reset_index()

        # Get data
        data.append(np.array(stock_data[data_wanted]))

    return data

def delete_old_csv(directory="stock_data"):
    csv_files = glob.glob(directory + "/*.csv")
    for f in csv_files:
        os.remove(f)

def axis_definer(graph_data):
    xlim = [0, len(graph_data)]

    data_max = np.max(graph_data)
    data_min = np.min(graph_data)

    ylim = [0 if data_min-10 < 0 else data_min-10, data_max+10]

    return xlim, ylim


def interpolate(data_list, n):
    data_x = []
    data_y = []
    for i in range(len(data_list)-1):
        x = np.linspace(i, i+1, n).tolist()
        y = np.linspace(data_list[i], data_list[i+1], n).tolist()

        data_x = data_x + x
        data_y = data_y + y
    return data_x, data_y


def color_fade_calculator(data, n=5):
    tracker = []
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
            bundles.append([tracker[i-1], count])
            count = 1
    bundles.append([tracker[-1], count])    # Append last bundle

    for i in range(len(bundles)):
        bundles[i][1] = bundles[i][1] * n

    # Calculate a fading color from 0 'green to 1 'red' dependent on the size of the number in bundles
    cm = []
    for trend, length in bundles:
        color_range1, color_range2 = [], []
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
        # noinspection Name
        cm.extend(color_range1)
        cm.extend(color_range2)

    return cm


def segment_calculator(data, n=5):
    data_x, data_y = interpolate(data, n)
    segments = []
    for i in range(len(data_x) - 1):
        curr = (data_x[i], data_y[i])
        next_one = (data_x[i + 1], data_y[i + 1])

        segments.append([curr, next_one])

    return np.array(segments)


def grid_layout(data):
    data_amount = len(data)
    height = 1
    while True:
        max_width = height - 1
        width = math.floor(data_amount/height)
        if data_amount % height != 0:
            width += 1
        if width > max_width:
            height += 1
        else: break

    return width, height

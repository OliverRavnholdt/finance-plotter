import matplotlib.pyplot as plt     # Used to plot data on graphs
import matplotlib.colors as clr     # Used to specify custom colormap
from matplotlib.collections import LineCollection       # Used to plot multiple lines in a plot with gradients
from data_getter import data_getter     # Function to pull stock data using yfinance
import graphing_functions as gf     # Various helper functions for data handling

# Assign colormap
cmap = clr.LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#10:2FFF00-25:7BF75E-75:EE504D-90:FF0600
    (0.000, (0.184, 1.000, 0.000)),
    (0.100, (0.184, 1.000, 0.000)),
    (0.250, (0.482, 0.969, 0.369)),
    (0.750, (0.933, 0.314, 0.302)),
    (0.900, (1.000, 0.024, 0.000)),
    (1.000, (1.000, 0.024, 0.000))))

n = 10  # Determines amount of "lines" between each value. Higher n = better gradient

# Saves stock data as CSV files in folder stock_data and returns list of names in alphabetical order
stock_names = data_getter(interval='1m')

# Pulls the data from the CSV files and saves them as a nested list
data = gf.all_csv_tolist()

# Get the layout of subplots depending on length of data_list
w, h = gf.grid_layout(data)

# Create the subplots with funny title
figs, axs = plt.subplots(h, w, num="Stock portfolio graphs for you my friend :)")


# Attempt to maximize the window using 'TkAgg'
mng = plt.get_current_fig_manager()
try:
    mng.window.state('zoomed')  # Type: Ignore
    # This works only with TkAgg backend
except AttributeError:
    print("Full-screen toggle not supported for this backend.")

# Adjust margins for nice layout
plt.subplots_adjust(left=0.05,
                    bottom=0.07,
                    right=0.95,
                    top=0.93,
                    wspace=0.15,
                    hspace=0.6)
# plt.subplot_tool() # Tool for margins

# This nested loop will plot the data
k = 0   # Used for indexing
for i in range(h):
    # Fix to plot data if stock list is 3 or less as "axs" is no longer nested
    if len(data) <= 3:
        curr_data = data[i]     # Define data to currently be plotted

        cm = gf.color_fade_calculator(curr_data, n)     # Get array to apply to colormap
        segments = gf.segment_calculator(curr_data, n)      # Define each line segment

        # Get and set the x and y limits
        x_lim, y_lim = gf.axis_definer(curr_data)
        axs[i].set_xlim(x_lim)
        axs[i].set_ylim(y_lim)

        # Create line-collection of segments with gradient and add them to plot
        lc = LineCollection(segments, linewidths=2, array=cm, cmap=cmap)
        axs[i].add_collection(lc)

        # Set title of current graph
        axs[i].title.set_text(stock_names[i])

    # Will run if the stock list is bigger than 3.
    else:
        for j in range(w):
            curr_data = data[k]     # Define data to currently be plotted

            cm = gf.color_fade_calculator(curr_data, n)  # Get array to apply to colormap
            segments = gf.segment_calculator(curr_data, n)  # Define each line segment

            # Get and set the x and y limits
            x_lim, y_lim = gf.axis_definer(curr_data)
            axs[i, j].set_xlim(x_lim)
            axs[i, j].set_ylim(y_lim)

            # Create line-collection of segments with gradient and add them to plot
            lc = LineCollection(segments, linewidths=2, array=cm, cmap=cmap)
            axs[i, j].add_collection(lc)

            # Set title of current graph
            axs[i, j].title.set_text(stock_names[k])

            k += 1      # Increment k for indexing

gf.delete_old_csv()     # Delete all files from stock folder (Comment to keep files)

# Plot graph using matplotlib pyplot
plt.show()

import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.collections import LineCollection
from data_getter import data_getter
import graphing_functions as gf

# Assign colormap
cmap = clr.LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#10:2FFF00-25:7BF75E-75:EE504D-90:FF0600
    (0.000, (0.184, 1.000, 0.000)),
    (0.100, (0.184, 1.000, 0.000)),
    (0.250, (0.482, 0.969, 0.369)),
    (0.750, (0.933, 0.314, 0.302)),
    (0.900, (1.000, 0.024, 0.000)),
    (1.000, (1.000, 0.024, 0.000))))

n = 10

stock_names = data_getter(interval='1m')
data = gf.all_csv_tolist()

w, h, err = gf.grid_layout(data)
figs, axs = plt.subplots(h, w, num="Stock portfolio graphs for you my friend :)")

mng = plt.get_current_fig_manager()
# Attempt to maximize the window using 'TkAgg'
try:
    mng.window.state('zoomed')  # type: ignore # This works only with TkAgg backend
except AttributeError:
    print("Full-screen toggle not supported for this backend.")

plt.subplots_adjust(left=0.05,
                    bottom=0.07,
                    right=0.95,
                    top=0.93,
                    wspace=0.15,
                    hspace=0.6)
# plt.subplot_tool() # Tool for margins

k = 0
for i in range(h):
    if len(data) <= 3:
        h = len(data)
        curr_data = data[i]

        cm = gf.color_fade_calculator(curr_data, n)
        segments = gf.segment_calculator(curr_data, n)

        x_lim, y_lim = gf.axis_definer(curr_data)

        lc = LineCollection(segments, linewidths=2, array=cm, cmap=cmap)
        axs[i].add_collection(lc)

        axs[i].set_xlim(x_lim)
        axs[i].set_ylim(y_lim)
        axs[i].title.set_text(stock_names[i])
    else:
        for j in range(w):
            print(i, j, k)
            curr_data = data[k]

            cm = gf.color_fade_calculator(curr_data, n)
            segments = gf.segment_calculator(curr_data, n)

            x_lim, y_lim = gf.axis_definer(curr_data)

            lc = LineCollection(segments, linewidths=2, array=cm, cmap=cmap)
            axs[i, j].add_collection(lc)

            axs[i, j].set_xlim(x_lim)
            axs[i, j].set_ylim(y_lim)
            axs[i, j].title.set_text(stock_names[k])
            k += 1
plt.show()

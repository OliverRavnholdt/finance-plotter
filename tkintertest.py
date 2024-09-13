import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
import math
from graphing_functions import grid_layout

tester = [[0] for i in range(10)]
w, h, remove = grid_layout(tester)
print(w, h)
print(len(tester))

figs, axs = plt.subplots(h, w)

segments1 = [0, 1, 2, 3, 4, 5]
segments2 = [0, 3, 1, 7, 10, 4]



segment1 = []
segment2 = []

mng = plt.get_current_fig_manager()
# Attempt to maximize the window using 'TkAgg'
try:
    mng.window.state('zoomed')  # type: ignore # This works only with TkAgg backend
except AttributeError:
    print("Full-screen toggle not supported for this backend.")

for i in range(len(segments1)-1):
    curr = [i, segments1[i]]
    next = [i+1, segments1[i+1]]

    segment1.append([curr, next])

    curr = [i, segments2[i]]
    next = [i+1, segments2[i+1]]

    (segment2.append([curr, next]))


plt.subplots_adjust(left=0.05,
                    bottom=0.07,
                    right=0.95,
                    top=0.93,
                    wspace=0.15,
                    hspace=0.6)
# plt.subplot_tool() # Tool for margins


lc = LineCollection(segment1, linewidths=2)
axs[0, 0].add_collection(lc)
axs[0, 0].title.set_text("hello")


lc = LineCollection(segment2, linewidths=2)
axs[1, 0].add_collection(lc)
axs[1, 0].title.set_text("hello1")


plt.show()

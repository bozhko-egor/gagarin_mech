import matplotlib.pyplot as plt
import matplotlib.patches as pt
from matplotlib.animation import FuncAnimation
import numpy as np
import pickle
import sys

x0, y0 = (0, 0)
x1, y1 = (23, 0)

fig = plt.figure()
ax = plt.axes(xlim=(0, 25), ylim=(0, 25))
ax.set_xticks(np.arange(-50, 30, 5))
ax.set_yticks(np.arange(-30, 25, 5))
plt.grid()
e1 = pt.Arc((0, 0), 49, 49, linewidth=1, theta1=179, theta2=315)

ax.add_patch(e1)
lines = []
for i in range(9):
    if i == 3:
        line_obj = plt.plot([], [], 'black', lw=2)[0]
        lines.append(line_obj)
        continue
    line_obj = plt.plot([], [], 'b', lw=2)[0]
    lines.append(line_obj)
with open('data', 'rb') as f:
    data = pickle.load(f)


def generator():
    for i, line in enumerate(data):
        yield line

data_gen = generator()
def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(i):

    (x3, y3), (x2, y2), (x9, y9), (x10, y10), (x8, y8), (x7, y7), (x6, y6), (x4, y4), (x5, y5), fi = next(data_gen)
    label = 'angle: {0}rad'.format(round(fi, 1))
    lines_ = [[(x1, x2), (y1, y2)],      # KB
              [(x2, x3), (y2, y3)],      # KD
              [(x9, x8), (y9, y8)],      # MF
              [(x0, x3), (y0, y3)],      # R
              [(x7, x8), (y7, y8)],      # GF
              [(x7, x6), (y7, y6)],      # GE
              [(x4, x3), (y4, y3)],      # SD
              [(x4, x5), (y4, y5)],      # SA
              [(x2, x5), (y2, y5)],      # AK
              ]
    for i, line1 in enumerate(lines):
        line1.set_data(*lines_[i])
    ax.set_xlabel(label)
    return tuple(lines) + (label,)

if __name__ == '__main__':
    anim = FuncAnimation(fig, update, frames=len(data), init_func=init, interval=50)
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('gagarin.gif', dpi=80, writer='imagemagick')
    else:
        plt.show()

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Initialize the figure and axis
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

# Set up the plot limits
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1, 1)

def init():
    """Initialize the background of the plot."""
    ln.set_data([], [])
    return ln,

def update(frame):
    """Update the data for each frame."""
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    return ln,

# Create the animation object
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                              init_func=init, blit=True, interval=50)

plt.show()
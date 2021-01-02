import matplotlib
import matplotlib.pylab as plt
from calculations import *

matplotlib.use('macosx')  # Used to create interactive plot


def plot_trajectory(distance, tank):
    """
    Plots the shell trajectory of a given tank firing at target at a given distance
    @param distance: float value that is the distance to the target
    @param tank: tank object from the file tank_info.py
    """
    # Initialize variables
    v = tank.muzzle_velocity
    g = 9.81
    angle_rad = math.radians(get_angle(distance, tank))
    times = np.linspace(0, get_time(distance, tank), num=1000)

    x_coordinates = []
    y_coordinates = []
    for time in times:
        # get positions for each time in times and append to lists
        x = ((v * time) * math.cos(angle_rad))
        y = ((v * time) * math.sin(angle_rad)) - ((0.5 * g) * (time ** 2)) + tank.gun_height
        x_coordinates.append(x)
        y_coordinates.append(y)

    # Remove any y values below the height of 0
    cleaned_y = []
    cleaned_x = []
    for val in y_coordinates:
        if val > 0:
            cleaned_y.append(val)
    for i in range(0, len(cleaned_y)):
        cleaned_x.append(x_coordinates[i])

    # plot each point and label axis
    plt.plot(cleaned_x, cleaned_y)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')

    # Label max height
    max_height_data = max_height(distance, tank)
    plt.annotate("Max height (" + str(max_height_data[1]) + " m)", (max_height_data[0], max_height_data[1]))

    plt.show()

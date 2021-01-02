import numpy as np
from tank_info import *
import math

# Initialize tanks objects
M1A1 = TankM1A1()
Challenger1 = TankChallenger1()
M4A1 = TankM4A1()
Churchill4 = TankChurchill4()

# With drag these resulting values would be very different, http://dynref.engr.illinois.edu/afp.html
# The max range would be roughly around 30% of what is currently be calculated to be


def max_range(tank):
    """
    Finds the maximum range a given tank can fire given a tanks muzzle_velocity and
        initial approximate gun firing height
    @param tank: tank object from the file tank_info.py
    @return max_distance: float value that is the calculated maximum distance a tank can hit
    """
    g = 9.81
    v = tank.muzzle_velocity
    time = 0
    height = tank.gun_height

    # For max range use max gun elevation
    angle_rad = math.radians(tank.max_gun_elevation)

    # solve for time
    coefficients = [-(1/2) * g, v * (math.sin(angle_rad)), height]
    roots = np.roots(coefficients)
    for val in roots:
        if np.iscomplex(val):
            continue
        if val < 0:
            continue
        time = val

    # Find max distance
    max_distance = (v * math.cos(angle_rad)) * time

    return max_distance


def min_range(tank):
    """
    Finds the minimum firing range a given tank can fire given a tanks muzzle_velocity and
        initial approximate gun firing height
    @param tank: tank object from the file tank_info.py
    @return min_distance: float value that is the calculated minimum distance the tank can hit
    """
    g = 9.81
    v = tank.muzzle_velocity
    time = 0
    height = tank.gun_height

    # For min range use max gun depression
    angle_rad = math.radians(-tank.max_gun_depression)

    # Solve for time
    coefficients = [-(1 / 2) * g, v * (math.sin(angle_rad)), height]
    roots = np.roots(coefficients)
    for val in roots:
        if np.iscomplex(val):
            continue
        if val < 0:
            continue
        time = val

    # Find min distance
    min_distance = (v * math.cos(angle_rad)) * time

    return min_distance


def get_angle(distance, tank):
    """
    Finds angle the tank needs to fire to hit a target at a given distance
    @param distance: float value that is the distance to the target
    @param tank: tank object from the file tank_info.py
    @return max_distance: float value that is the angle (in degrees) the tank needs to fire to hit a target at a
                          given distance
    """
    g = 9.81
    v = tank.muzzle_velocity
    distance_x = distance
    distance_y = tank.gun_height
    angle_deg = 0

    if distance > max_range(tank):
        print("Target out of range")
        return

    if distance < min_range(tank):
        print("Target too close")
        return

    # The formula below is derived by solving for time in the horizontal direction then substituting that into the
    # vertical direction. Then Use trig identities to obtain only tan functions and  simplify that to create a
    # quadratic function with x representing tan x. Solving this quadratic will yield the values for tan x. Then
    # solve for x (angle).

    term = -(g/2) * (distance_x ** 2 / v ** 2)
    coefficients = [term, distance_x, distance_y + term]
    roots = np.roots(coefficients)
    angles_deg = []

    # Convert tan x solution into degrees
    for i, val in enumerate(roots):
        temp = math.degrees(math.atan(val))
        temp = round(temp, 5)
        angles_deg.append(temp)

    # Find the angle that is actually in the range of the gun elevation and depression angles
    for val in angles_deg:
        if -tank.max_gun_depression <= val <= tank.max_gun_elevation:
            angle_deg = val

    return angle_deg


def get_time(distance, tank):
    """
    Finds the time the projectile is in the air
    @param distance: float value that is the distance to the target
    @param tank: tank object from the file tank_info.py
    @return time: float value that is the time that the projectile is in the air
    """
    v = tank.muzzle_velocity
    x = distance
    angle_rad = math.radians(get_angle(distance, tank))

    if distance > max_range(tank):
        print("Target out of range")
        return

    if distance < min_range(tank):
        print("Target too close")
        return

    time = x/(v*math.cos(angle_rad))

    return time


def max_height(distance, tank):
    """
    Finds the coordinates of the max height of the shell
    @param distance: float value that is the distance to the target
    @param tank: tank object from the file tank_info.py
    @return data: list that contains the coordinates of the max height of the shell, [x, y]
    """
    v = tank.muzzle_velocity
    g = 9.81
    angle_rad = math.radians(get_angle(distance, tank))
    time = 0

    # Find max height
    max_height = ((v*math.sin(angle_rad))**2)/(2*g)

    # Solve for time
    coefficients = [-(1/2) * g, v * angle_rad, -max_height]
    roots = np.roots(coefficients)
    for val in roots:
        if np.iscomplex(val):
            continue
        if val < 0:
            continue
        time = val

    # Find x coordinate and append the coordinates to the data list
    data = []
    x = ((v * time) * math.cos(angle_rad))
    data.append(x)
    data.append(max_height)

    return data

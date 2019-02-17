import numpy as np
import pandas as pd
import geopy.distance
from math import *
from scipy.spatial import KDTree
# i love this guy: https://stackoverflow.com/questions/43020919/scipy-how-to-convert-kd-tree-distance-from-query-to-kilometers-python-pandas

def location_to_xyz(user_location):
    return to_Cartesian(deg2rad(user_location['long']),deg2rad(user_location['lat']))

def mts_between_atms(coords_1,coords_2):
    return geopy.distance.vincenty(coords_1, coords_2).meters

def deg2rad(degree):
    rad = degree * 2*np.pi / 360
    return(rad)

def dist(x):
    R = 6367 # earth radius
    gamma = 2*np.arcsin(deg2rad(x/(2*R))) # compute the angle of the isosceles triangle
    dist = (2*R*sin(gamma/2)) # compute the side of the triangle
    return(dist)

def to_Cartesian(lat, lng):
    R = 6367 # radius of the Earth in kilometers

    x = R * cos(lat) * cos(lng)
    y = R * cos(lat) * sin(lng)
    z = R * sin(lat)
    return x, y, z

def map_df(atms_dict):

    keys_data = list(map(list,list(atms_dict.keys())))
    data = list(map(lambda each: {'long': each[0], 'lat': each[1], 'red': each[2]},keys_data))
    df = pd.DataFrame(data)
    df['x'],df['y'],df['z']=zip(*map(to_Cartesian,deg2rad(df['long']),deg2rad(df['lat'])))
    return df

def generate_kdtree(df):
    coordinates = list(zip(df['x'], df['y'], df['z']))
    return KDTree(coordinates)

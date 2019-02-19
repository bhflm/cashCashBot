import numpy as np
import pandas as pd
import geopy.distance
from consts import *
from math import *
from scipy.spatial import KDTree

def generate_reply(atms_info):
    message = "Here're nearby ATMS for you:\n\n"

    for atm in atms_info:
        bank = atm[1]
        dir = atm[2]
        additional_atm = 'Name: {}\nAddress: {}\n\n'.format(bank,dir)
        message += additional_atm

    return message

def filter_atm_by_distance(atm, user_location):
    return mts_between_atms((atm['lat'],atm['long']),(user_location['lat'],user_location['long'])) < MAX_DISTANCE

def mts_between_atms(coords_1,coords_2):
    return geopy.distance.vincenty(coords_1, coords_2).meters

def filter_possible_atms(all_near_atms,chosen_atm, user_location):
    code = map_atm_code(str(chosen_atm).upper())

    #JUST FOR TESTING
    #spoof_location = { 'long' : -58.5250309541001 , 'lat': -34.6137051686962 }
    #JUST FOR TESTING

    atms_with_code = list(filter(lambda atm: (atm['red'] == code), all_near_atms))
    atms_within_distance = list(filter(lambda atm: filter_atm_by_distance(atm,user_location), atms_with_code))

    return atms_within_distance

def is_valid_input(input):
    target = input.lower().capitalize()
    try:
        return { BANELCO : 'Banelco', LINK : 'Link'}[target]
    except KeyError:
        return False

def map_atm_code(atm):
    return CODE_DICT[atm]

def location_to_xyz(user_location):
    return to_Cartesian(deg2rad(user_location['long']),deg2rad(user_location['lat']))

def deg2rad(degree):
    rad = degree * 2*np.pi / 360
    return(rad)

def dist(x):
    gamma = 2*np.arcsin(deg2rad(x/(2*R))) # compute the angle of the isosceles triangle
    dist = (2*R*sin(gamma/2)) # compute the side of the triangle
    return(dist)

def to_Cartesian(lat, lng):
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

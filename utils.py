import numpy as np
import pandas as pd
import geopy.distance
from consts import *
from math import *
from scipy.spatial import KDTree


def probabilities_for_atms(atms):
    #chances of drawing from a atm acording to how many
    return { 1: 1, 2: [0.75, 0.25], 3: [0.7,0.2,0.1] }[atms]

def generate_reply(atms_info):
    message = "Here're nearby ATMS for you:\n\n"
    for atm in atms_info:
        print(atm)
        bank = atm[2]
        dir = atm[3]
        additional_atm = 'Name: {}\nAddress: {}\n\n'.format(bank,dir)
        message += additional_atm

    return message

def filter_atms_by_transactions(atms_data,atms_info):
    sorted_by_transactions = sorted(atms_data, key=lambda tup: tup[1])
    filter_if_exceeded_transactions = list(filter(lambda each: each[1] < MAX_TRANSACTIONS,sorted_by_transactions))
    id_candidates = list(map(lambda each: each[0],filter_if_exceeded_transactions[:3]))
    result = [x for x in atms_info if int(x[0]) in set(id_candidates)] #if x[0] in set(id_candidates)]

    return result

def filter_atm_by_distance(atm, user_location):
    return mts_between_atms((atm['lat'],atm['long']),(user_location['lat'],user_location['long'])) < MAX_DISTANCE

def mts_between_atms(coords_1,coords_2):
    return geopy.distance.vincenty(coords_1, coords_2).meters

def filter_possible_atms(all_near_atms,chosen_atm, user_location):
    code = map_atm_code(str(chosen_atm).upper())
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

def format_query(atms):
    query = ""
    for atm in atms:
        query += "({},0),".format(atm)
    return query[:-1]

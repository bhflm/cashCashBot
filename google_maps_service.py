import logging
import requests
from consts import MAPS_API_URL
from keys import MAPS_TOKEN


#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

def generate_map(user_location, atms_location):
    logging.info('Generating url for map')
    #ej:

    color = 'red'
    foo = 'markers=color:{}%'.format(color)

    #JUST FOR TESTING
    #spoof_location = { 'long' : -58.3652916646075 , 'lat': -34.6220423397099 }

    lat = float("{0:.6f}".format(user_location['lat']))
    long = float("{0:.6f}".format(user_location['long']))
    center = '{},{}'.format(lat,long)

    size = '800x800'
    zoom = '12'
    additional_markers = '&markers=color:{}|label:{}|{}'
    atms = ''

    static_maps_query = '{}center={}&zoom={}&size={}'.format(MAPS_API_URL,center,zoom,size)
    maps_api_key = '&key={}'.format(MAPS_TOKEN)

    for each_atm in atms_location:
        atm_lat = float("{0:.6f}".format(each_atm['lat']))
        atm_long = float("{0:.6f}".format(each_atm['long']))
        atm_coord = "{},{}".format(atm_lat,atm_long)
        atm_query = additional_markers.format(color,(atms_location.index(each_atm)+1),atm_coord)
        static_maps_query += atm_query

    result_url = static_maps_query + maps_api_key
    logging.info('Generated map: {}'.format(static_maps_query))
    return result_url

import logging
import telegram
import numpy as np
import pandas as pd
from utils import map_df, generate_kdtree, dist, mts_between_atms, location_to_xyz
from keys import TOKEN
from consts import BANELCO,LINK,FILE_PATH, INVALID_INPUT
from csv_reader import csvReader
from scipy.spatial import KDTree
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

class ATMSearcher():
    def __init__(self):
        self.updater = Updater(token=TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.atms_dict = {}
        self.read_csv(self.atms_dict)
        self.atms_df = map_df(self.atms_dict)
        self.atms_tree = generate_kdtree(self.atms_df)
        self.user_location = {}

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.get_user_location))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.get_valid_atm))

    def start(self, bot, update):
        logging.info('STARTED BOT')
        welcome_message = "Welcome to cashCash! in order to work properly, i'd need to ask you for your location."
        keyboard = telegram.KeyboardButton("Confirm", request_contact=None, request_location=True)
        reply_markup = telegram.ReplyKeyboardMarkup([[keyboard]])
        bot.send_message(chat_id=update.message.chat_id,
                         text=welcome_message,
                         reply_markup=reply_markup)

    def is_valid_input(self, input):
        target = input.lower().capitalize()
        try:
            return { BANELCO : 'Banelco', LINK : 'Link'}[target]
        except KeyError:
            return False

    def search_closest_atms(self,atm):
        logging.info("GETTING CLOSEST {} ATMs NEAR {}".format(atm,self.user_location))

        user_xyz = location_to_xyz(self.user_location)
        #con el arbol y la ubicacion le tiro la query al arbol para que me devuelva los n mas cercanos
        near_atms = self.atms_tree.query(user_xyz,10)
        print(near_atms)

        # print(self.atms_tree)
        # print(self.atms_df)

        # df = generate_df_for_kdtree(self.atms_dict)
        # coordinates = list(zip(df['x'], df['y'], df['z']))
        # print(coordinates[0])



        #una vez que tengo los ids de os mas cercanos (near_atms[1]) los busco en el df


        # foodist = list(map(dist,foo[0]))
        # print(coordinates[0])
        # possible_atms = list(foo[1])
        # print(possible_atms)
        # print(self.atms_dict.items())
        #print(df['lat'][0],df['long'][0])
        # -34.605812942035 -58.3709017854754
        #print(df['lat'][1],df['long'][1])
        # -34.6050839250446 -58.3709757833981
        #foobar = mts_between_atms((df['lat'][0],df['long'][0]),(df['lat'][1],df['long'][1]))


    def get_valid_atm(self, bot, update):
        atm_network = self.is_valid_input(update.message.text)
        if (atm_network):
            logging.info("REQUEST FOR RETRIEVING {} ATM'S ".format(atm_network))
            a = self.search_closest_atms(atm_network)

        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=INVALID_INPUT.format(update.message.text))


    def get_user_location(self, bot, update):
        logging.info('GETTING USER LOCATION')
        self.user_location = { 'lat' : update.message.location.latitude, 'long' : update.message.location.longitude }
        bot.send_message(chat_id=update.message.chat_id, text="Thanks, try searching for 'Banelco' or 'Link'!")

    def read_csv(self,atms_dict):
        logging.info('PROCESSING CSV')
        reader = csvReader(FILE_PATH, delimiter = '', quotechar = '|')
        reader.process_csv(atms_dict)


    def run(self):
        self.updater.start_polling()

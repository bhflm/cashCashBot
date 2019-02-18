import logging
import telegram
import numpy as np
import pandas as pd
from utils import *
from google_maps_service import generate_map
from keys import TOKEN
from consts import BANELCO,LINK,FILE_PATH, INVALID_INPUT, NO_AVAILABLE_ATMS_AROUND
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

    def search_closest_atms(self,atm):
        logging.info("GETTING CLOSEST {} ATMs NEAR {}".format(atm,self.user_location))

        user_xyz = location_to_xyz(self.user_location)
        kdtree_query = list(self.atms_tree.query(user_xyz,10)[1])

        all_near_atms = list(map(lambda each: {'long': self.atms_df['long'][each], 'lat': self.atms_df['lat'][each], 'red': self.atms_df['red'][each]},kdtree_query))
        return filter_possible_atms(all_near_atms, atm, self.user_location)


    def retrieve_atms_info(self, atms):
        dict_keys = list(map(lambda each: (each['long'],each['lat'],each['red']),atms))
        atms_info = list(map(lambda each: self.atms_dict[each],dict_keys))
        return atms_info

    def get_valid_atm(self, bot, update):
        atm_network = is_valid_input(update.message.text)
        if (atm_network):
            logging.info("REQUEST FOR RETRIEVING {} ATM'S ".format(atm_network))
            closest_atms = self.search_closest_atms(atm_network)

            atms_info_for_message = self.retrieve_atms_info(closest_atms)


            if not closest_atms:
                    logging.info('COULD NOT RETRIEVE ATMs WITHIN DISTANCE')
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=NO_AVAILABLE_ATMS_AROUND)

            bot.send_message(chat_id = update.message.chat_id, text = generate_reply(atms_info_for_message))
            bot.send_photo(chat_id = update.message.chat_id, photo = generate_map(self.user_location, closest_atms))

        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=INVALID_INPUT.format(update.message.text))

    def get_user_location(self, bot, update):
        logging.info('GETTING USER LOCATION')
        self.user_location = { 'lat' : update.message.location.latitude, 'long' : update.message.location.longitude }
        bot.send_message(chat_id=update.message.chat_id, text="Thanks!, now try searching for 'Banelco' or 'Link'!")

    def read_csv(self,atms_dict):
        logging.info('PROCESSING CSV')
        reader = csvReader(FILE_PATH, delimiter = '', quotechar = '|')
        reader.process_csv(atms_dict)


    def run(self):
        self.updater.start_polling()

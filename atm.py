import logging
import telegram
import numpy as np
import pandas as pd
import os
from utils import *
from db_service import DBTransactor
from last_refresh_service import generate_last_refresh_file, update_last_refresh_file, check_updated_today, service_healthcheck
from google_maps_service import generate_map
from keys import TOKEN
from consts import BANELCO,LINK,FILE_PATH, INVALID_INPUT, NO_AVAILABLE_ATMS_AROUND, MAX_TRANSACTIONS
from csv_reader import csvReader
from scipy.spatial import KDTree
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

class ATMSearcher():
    def __init__(self):
        self.db_transactions = DBTransactor()
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

    def calculate_possible_atms(self, closest_atms):
        logging.info("CALCULATING EXTRACTION PROBABILITIES FOR CLOSEST ATMS")
        atms_info = self.retrieve_atms_info(closest_atms)
        if (len(closest_atms) > 3):
            logging.info("CHECKING ATMS TRANSACTIONS")
            atms_ids = list(map(lambda each: each[0],atms_info))
            data = []
            for atm in atms_ids:
                data.append(self.db_transactions.get_atm_transactions(atm)[0])


            atms_info = filter_atms_by_transactions(data,atms_info)

        atms_p_ids = list(map(lambda each: each[0],atms_info))
        draw_probabilities = probabilities_for_atms(len(atms_p_ids))

        possibles = np.random.choice(atms_p_ids,len(atms_p_ids), p = draw_probabilities)

        self.db_transactions.add_transaction(possibles[0]) # not working query ?

        atms_coords = list(map(lambda each: (each[7],each[8]),atms_info)) # (long, lat) -> desprolijisimo germo



        return (atms_coords,atms_info)

    def get_valid_atm(self, bot, update):
        atm_network = is_valid_input(update.message.text)
        if (atm_network):
            logging.info("REQUEST FOR RETRIEVING {} ATM'S ".format(atm_network))
            closest_atms = self.search_closest_atms(atm_network)
            possible_atms = self.calculate_possible_atms(closest_atms)

            atms_info_for_message = self.retrieve_atms_info(closest_atms)

            if closest_atms:
                bot.send_message(chat_id = update.message.chat_id, text = generate_reply(possible_atms))
                bot.send_photo(chat_id = update.message.chat_id, photo = generate_map(self.user_location, closest_atms))
            else:
                logging.info('COULD NOT RETRIEVE ATMs WITHIN DISTANCE')
                bot.send_message(chat_id=update.message.chat_id,
                                 text=NO_AVAILABLE_ATMS_AROUND)
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

    def populate_db(self, atms_dict):
        atms_ids = list(map(lambda each: each[0],atms_dict.values()))
        self.db_transactions.add_all_atms(atms_ids)

    def run(self):
        logging.info('STARTED BOT')
        logging.info('CHECKING IF SERVICE WAS RUNNING TODAY')
        if not service_healthcheck():
            generate_last_refresh_file()
        if self.db_transactions.setup():
            self.populate_db(self.atms_dict)
        self.updater.start_polling()

import logging
import telegram
import numpy as np
import pandas as pd
from utils import *
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
        self.atms_tree = self.map_dict_to_kdtree(self.atms_dict)
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
        # pos = list(self.user_location.values())
        pos = [-58.37097270, -34.60459180]
        possible_atms = self.atms_tree.query_pairs(2000)
        # print(self.atms_tree.data)
        print(possible_atms)

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

    def map_dict_to_kdtree(self, atms_dict):
        mapped_data = list(map(list,list(atms_dict.keys())))
        # print(mapped_data)
        return KDTree(mapped_data, leafsize = 2)

    def run(self):
        self.updater.start_polling()

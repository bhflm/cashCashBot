import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import TOKEN
from consts import BANELCO,LINK,FILE_PATH
from csv_reader import csvReader
import numpy as np
import pandas as pd
from scipy.spatial import KDTree

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class ATMSearcher():
    def __init__(self):
        self.updater = Updater(token=TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.atms_dict = {}
        self.read_csv(self.atms_dict)
        self.atms_tree = self.map_dict_to_kdtree(self.atms_dict)

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

    def is_valid_atm(self, input):
        target = input.lower().capitalize()
        #filtrar cuando no es alguno de los 2
        return { BANELCO : 'Banelco', LINK : 'Link'}[target]

    def get_valid_atm(self, bot, update):
        atm_network = update.message.text
        print(self.is_valid_atm(atm_network))

    def get_user_location(self, bot, update):
        logging.info('GETTING USER LOCATION')
        user_coords = { 'lat' : update.message.location.latitude, 'long' : update.message.location.longitude }
        print(user_coords['lat'],user_coords['long'])

    def read_csv(self,atms_dict):
        logging.info('PROCESSING CSV')
        reader = csvReader(FILE_PATH, delimiter = '', quotechar = '|')
        reader.process_csv(atms_dict)

    def map_dict_to_kdtree(self, atms_dict):
        mapped_data = list(map(list,list(atms_dict.keys())))
        return KDTree(mapped_data, leafsize = 3)

    def run(self):
        self.updater.start_polling()

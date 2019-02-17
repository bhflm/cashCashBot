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
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.get_user_location))

        self.atms_dict = {}
        self.read_csv(self.atms_dict)
        self.atms_tree = self.map_dict_to_kdtree(self.atms_dict)



    def start(self, bot, update):
        logging.info('STARTED BOT')
        welcome_message = "Welcome to cashCash! in order to work properly, i'd need to ask you for your location."
        bot.send_message(chat_id=update.message.chat_id, text=welcome_message)

        keyboard = telegram.KeyboardButton("Confirm", request_contact=None, request_location=True)
        reply_markup = telegram.ReplyKeyboardMarkup([[keyboard]])
        bot.send_message(chat_id=update.message.chat_id,
                         text = "Would like to search for Link or Banelco closest ATMs?",
                         reply_markup=reply_markup)

    def get_user_location(self, bot, update):
        logging.info('GETTING USER LOCATION')
        user_coords = { 'lat' : update.message.location.latitude, 'long' : update.message.location.longitude }
        print(user_coords['lat'],user_coords['long'])

    def read_csv(self,atms_dict):
        logging.info('PROCESSING CSV')
        reader = csvReader(FILE_PATH, delimiter = '', quotechar = '|')
        reader.process_csv(atms_dict)

    def print_data(each):
        print('hola')
        print(each)

    def map_dict_to_kdtree(self, atms_dict):
        mapped_data = list(map(list,list(atms_dict.keys())))
        return KDTree(mapped_data, leafsize = 3)

    def is_a_valid_atm(self, id):
        pass



    def start(self):
        self.updater.start_polling()

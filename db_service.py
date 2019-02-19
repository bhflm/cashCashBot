import sqlite3
import logging

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

class DBTransactor:
    def __init__(self, dbname="transactions.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        logging.info('CREATING TABLE TRANSACTIONS')
        try:
            self.conn.execute('''CREATE TABLE TRANSACTIONS
             (ATM         INT    NOT NULL,
             EXTRACTIONS  INT     NOT NULL);''')
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: TABLE ALREADY EXISTS')

    def select_all(self):
        logging.info('SELECT ALL')
        try:
            cursor = self.conn.execute("SELECT * FROM TRANSACTIONS")
            for row in cursor:
                print(row)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT SELECT ALL')

    def add_transaction(self, atm = 0): # < cambiar atm
        logging.info('ADDING TRANSACTION TO ATM {}'.format(atm))

        try:
            query = "INSERT INTO TRANSACTIONS (ATM, EXTRACTIONS) VALUES ({}, 1).".format(atm)
            self.conn.execute(query) #args)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT ADD TRANSACTION FOR ATM {}'.format(atm))

    def refresh_all_atms(self):
        logging.info('REFRESHING ALL TRANSACTIONS FOR ATMS')
        try:
            query = "UPDATE TRANSACTIONS SET EXTRACTIONS = 0"
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT UPDATE ALL ATMS')

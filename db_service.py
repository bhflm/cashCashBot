import sqlite3
import logging
from utils import format_query
#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

class DBTransactor:
    def __init__(self, dbname="transactions.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        logging.info('CREATING TABLE TRANSACTIONS')
        try:
            self.conn.execute('''CREATE TABLE TRANSACTIONS
             (ATM         INT    NOT NULL,
             EXTRACTIONS  INT     NOT NULL);''')
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: TABLE ALREADY EXISTS')
            return False
    def add_atm(self,id):
        logging.info('ADDING ATM')
        try:
            query = "INSERT INTO TRANSACTIONS (ATM, EXTRACTIONS) VALUES ({}, 0).".format(id)
            self.conn.execute(query) #args)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT ADD TRANSACTION FOR ATM {}'.format(atm))

    def add_all_atms(self, atms):
        logging.info('POPULATING TABLE WITH ALL {} ATMS'.format(len(atms)))
        all_atms = format_query(atms)
        try:
            query = "INSERT INTO TRANSACTIONS (ATM, EXTRACTIONS) VALUES {}".format(all_atms)
            self.conn.execute(query)
            self.conn.commit()

        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR')

    def get_atm_transactions(self, atm):
        try :
            data = []
            query = "SELECT * FROM TRANSACTIONS WHERE ATM = {}".format(atm)
            # SELECT * FROM Student WHERE name IN (3, 2, 1)
            cursor = self.conn.execute(query)
            for row in cursor:
                data.append(row)

            self.conn.commit()
            return data
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT SELECT ALL')

    def add_transaction(self, atm_id): # < cambiar atm
        logging.info('ADDING TRANSACTION TO ATM {}'.format(atm_id))
        try: #tf is wrong with this query below
            query = "UPDATE TRANSACTIONS SET EXTRACTIONS = EXTRACTIONS + 1 WHERE ATM = {}".format(atm_id)
            query2 = "INSERT INTO TRANSACTIONS (EXTRACTIONS) VALUES (1) WHERE ATM = {}".format(atm_id)
            self.conn.execute(query) #args)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT ADD TRANSACTION FOR ATM {}'.format(atm_id))

    def refresh_all_atms(self):
        logging.info('REFRESHING ALL TRANSACTIONS FOR ATMS')
        try:
            query = "UPDATE TRANSACTIONS SET EXTRACTIONS = 0"
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT UPDATE ALL ATMS')


    def select_all(self):
        #this one is just for testing purposes
        #this one is just for testing purposes
        logging.info('SELECT ALL')
        try:
            cursor = self.conn.execute("SELECT * FROM TRANSACTIONS")
            for row in cursor:
                print('ROW')
                print(row)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info('DB SERVICE ERROR: COULD NOT SELECT ALL')

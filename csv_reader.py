from consts import *
import csv


class csvReader():

    def __init__(self, file, **parameters):
        self.file = file
        self.parameters = parameters

    def row_filter(self,row, columns=['long', 'lat', 'banco', 'red', 'ubicacion', 'terminales', 'calle', 'altura']):
        if row['localidad'] == 'CABA':
            return {col: row[col] for col in columns}

    def process_csv(self):
        with open(self.file, 'r') as csvfile:
            atms_data = csv.DictReader(csvfile)
            for row in atms_data:
                print(self.row_filter(row))
                

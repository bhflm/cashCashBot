from consts import *
import csv


class csvReader():

    def __init__(self, file, **parameters):
        self.file = file
        self.parameters = parameters

    def row_filter(self,row, columns=['long', 'lat', 'banco', 'red', 'ubicacion', 'terminales', 'calle', 'altura']):
        if row['localidad'] == 'CABA':
            return {col: row[col] for col in columns}

    def map_network(self,atm):
        get_type = {'BANELCO' : 0, 'LINK' : 1}
        return get_type[atm]

    def process_csv(self, data_dict):
        with open(self.file, 'r') as csvfile:
            atms_data = csv.DictReader(csvfile)
            for row in atms_data:
                transactions = 0
                key = (float(row['long']),float(row['lat']),self.map_network(row['red']))
                values = [row['banco'],row['ubicacion'],row['terminales'],row['calle'],row['altura'], transactions]
                data_dict[key] = values

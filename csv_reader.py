import csv


class csvReader():

    def __init__(self, file, **parameters):
        self.file = file
        self.parameters = parameters

    def read_csv(self):
        with open(self.file, 'r') as csvfile:
            atms_data = csv.reader(csvfile, self.parameters)
            for row in atms_data:
                print(row)

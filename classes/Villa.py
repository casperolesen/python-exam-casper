import csv

class Villa():
    def __init__(self, *data):
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def __getattr__(self, name):
        return 'attribute {name} not found'
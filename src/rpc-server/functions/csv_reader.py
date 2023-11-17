from csv import DictReader

class CSVReader:
    def __init__(self, filename, delimiter=';'):
        self._path = filename
        self._delimiter = delimiter

    def loop(self):
        with open(self._path, 'r') as file:
            for row in DictReader(file, delimiter=self._delimiter):
                yield row

    def read_entities(self, attr, builder, after_create=None):
        entities = {}
        for row in self.loop():
            if attr in row:
                e = row[attr]
                if e not in entities:
                    entities[e] = builder(row)
                    if after_create is not None:
                        after_create(entities[e], row)
        return entities

csv_reader = CSVReader(".data/data.csv")
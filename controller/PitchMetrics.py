import csv


class PitchMetrics:
    def __init__(self, file):
        self.metrics = []

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                self.metrics.append([row[1], row[2]])

    def get_note(self, rate):
        minm = False
        maxm = False
        for r in self.metrics:
            if float(rate) > float(r[1]):
                minm = True
            if float(rate) < float(r[1]):
                maxm = True
            if minm and maxm:
                return r[0]
        return False


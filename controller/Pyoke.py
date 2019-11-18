import magic
import os
import pygame

from pydub import AudioSegment

from controller.PitchMetrics import PitchMetrics
from controller.Pitcher import Pitcher


class Pyoke:
    def __init__(self):
        self.path = os.path.abspath('./music/music.mp3')
        self.file_recorded = os.path.abspath('./records/lauan.wav')

        mime = magic.from_file(self.path, mime=True)

        if mime != "audio/ogg":
            self.dst = str(self.path.split('.')[0]) + '.ogg'
            sound = AudioSegment.from_mp3(self.path)
            sound.export(self.dst, format="ogg")

        self.metrics = PitchMetrics(os.path.abspath("./metrics/pitch_metrics.csv"))

    @staticmethod
    def calc_average_rating(val1, val2):
        return (val2*100)/val1

    def get_average_rating(self):
        pitcher = Pitcher()
        data = pitcher.get_rate(self.dst)
        data2 = pitcher.get_rate(self.file_recorded)

        counter = 0
        rating = 0

        for i, d in data:
            note1 = self.metrics.get_note(d)
            if note1:
                note1 = note1.split(" ")[0]

            try:
                note2 = self.metrics.get_note(data2[i][1])
                if note2:
                    note2 = note2.split(" ")[0]
            except IndexError:
                break

            if note1 == note2:
                rating = rating + 1
            counter = counter + 1
        return self.calc_average_rating(counter, rating)


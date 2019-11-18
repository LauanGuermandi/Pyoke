from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from js2py.base import xrange

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
MAXIMUM = 16384


class Record:
    def __init__(self):
        self.wf = None
        self.end = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT, channels=1, rate=RATE,
                                  input=True, output=True,
                                  frames_per_buffer=CHUNK_SIZE)
        self.r = None
        self.sample_width = None

    @staticmethod
    def is_silent(snd_data):
        return max(snd_data) < THRESHOLD

    @staticmethod
    def normalize(snd_data):
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    @staticmethod
    def trim(snd_data):
        def _trim(_snd_data):
            snd_started = False
            r = array('h')

            for i in _snd_data:
                if not snd_started and abs(i) > THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        snd_data = _trim(snd_data)

        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        self.r = array('h', [0 for i in xrange(int(seconds * RATE))])
        self.r.extend(snd_data)
        self.r.extend([0 for i in xrange(int(seconds * RATE))])
        return self.r

    def record(self):
        num_silent = 0
        snd_started = False

        self.r = array('h')

        while 1:
            snd_data = array('h', self.stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            self.r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if self.end:
                print('end')
                break

    def record_to_file(self, path):
        self.record()
        data = pack('<' + ('h' * len(self.r)), *self.r)

        self.wf = wave.open(path, 'wb')
        self.wf.setnchannels(1)
        self.wf.setsampwidth(self.sample_width)
        self.wf.setframerate(RATE)
        self.wf.writeframes(data)
        self.wf.close()

    def end_record(self):
        self.end = True
        self.sample_width = self.p.get_sample_size(FORMAT)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.r = self.normalize(self.r)
        self.r = self.trim(self.r)
        self.r = self.add_silence(self.r, 0.5)

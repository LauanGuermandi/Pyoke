from aubio import source, pitch


class Pitcher:
    def __init__(self):
        self.downsample = 1
        self.samplerate = 44100 // self.downsample
        self.win_s = 4096//self.downsample
        self.hop_s = 512//self.downsample
        self.tolerance = 0.8

    def get_rate(self, file_path):
        file = source(file_path, self.samplerate, self.hop_s)
        self.samplerate = file.samplerate
        pitch_o = pitch("yin", self.win_s, self.hop_s, self.samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(self.tolerance)
        total_frames = 0
        history = []
        counter = 0

        while True:
            samples, read = file()
            audio_pitch = pitch_o(samples)[0]

            history.append([counter, audio_pitch])
            counter = counter+1

            total_frames += read
            if read < self.hop_s:
                break

        if not history:
            return False
        return history

    @staticmethod
    def save_rate(history, name):
        with open(name, 'w') as file_handle:
            for rate in history:
                file_handle.write('%s\n' % rate)


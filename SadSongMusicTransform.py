#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : SadSongMusicTransform.py
# @Author: MoonKuma
# @Date  : 2018/9/11
# @Desc  : Transform music from .wav into digital data


from util.Tools import is_legal_file,get_system_time
import wave
import pyaudio
import time
import pylab
import numpy as npy
from scipy.fftpack import fft



class SadSongMusicTransform:

    def __init__(self):
        self.music_data_map = dict()  # {id:{data_list:fft data list,type: is sad or not}
        self.wav_file = None # used only in playing songs

    def __pyaudio_callback(self, in_data, frame_count, time_info, status):
        data = self.wav_file.readframes(frame_count)
        return data, pyaudio.paContinue

    def play_single_song(self, file_name):
        if not is_legal_file(file_name):
            print 'File name is illegal:', file_name
            return 0
        p = pyaudio.PyAudio()
        self.wav_file = wave.open(file_name, 'rb')
        stream = p.open(format=p.get_format_from_width(self.wav_file.getsampwidth()),
                        channels=self.wav_file.getnchannels(), rate=self.wav_file.getframerate(), output=True,
                        stream_callback=self.__pyaudio_callback)
        stream.start_stream()
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.wav_file = None

    def wav_to_digital(self, file_name):
        if not is_legal_file(file_name):
            print 'File name is illegal:', file_name
            return 0
        wf = wave.open(file_name, 'rb')
        params = wf.getparams()
        n_channels, sample_width, frame_rate, n_frames = params[:4]
        str_data = wf.readframes(n_frames)
        wave_data = npy.fromstring(str_data, dtype=npy.short)
        if wf.getnchannels() == 2: # for music with two channels, 'LRLRLRLR'
            wave_data.shape = -1, 2
        wave_data = wave_data.T
        time_list = npy.arange(0, n_frames) * (1.0 / frame_rate)
        return [time_list, wave_data]

    def plot_wave_data(self, file_name):
        time_list, wave_data = self.wav_to_digital(file_name)
        pylab.subplot(211)
        pylab.plot(time, wave_data[0])
        pylab.subplot(212)
        pylab.plot(time, wave_data[1], c="g")
        pylab.xlabel("time (seconds)")
        pylab.show()

    def time_to_frequency(self, file_name):
        time_list, wave_data = self.wav_to_digital(file_name)
        for wave_line in wave_data:
            pass


    def test_execute(self):
        file_name = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/test01.wav'
        self.play_single_song(file_name)



# test
if __name__ == '__main__':
    pass
    SadSongMusicTransform().test_execute()











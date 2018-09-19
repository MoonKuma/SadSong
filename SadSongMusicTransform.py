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
        wf = wave.open(file_name, "rb")

    def test_execute(self):
        test_file = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/test01.wav'
        self.play_single_song(test_file)


# test
if __name__ == '__main__':
    pass
    SadSongMusicTransform().test_execute()











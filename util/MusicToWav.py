#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MusicToWav.py
# @Author: MoonKuma
# @Date  : 2018/9/11
# @Desc  : Change not-wav type music into *.wav

from pydub import AudioSegment
from Tools import get_file_list, get_system_time
import threading


class MusicThread(threading.Thread):

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)


class MusicToWav:

    def __init__(self):
        self.legal_file_type = ['mp3', 'flv', 'wav', 'ogg']
        return

    def trans_to_wav(self, file_name):
        file_name = file_name.strip()
        file_name_str = file_name[0:file_name.rfind('.')]
        file_type = file_name[file_name.rfind('.')+1:len(file_name)]
        file_save = file_name_str + '.wav'
        song = None
        if file_type not in self.legal_file_type:
            return
        elif file_type == 'wav':
            return
        elif file_type == 'mp3':
            song = AudioSegment.from_mp3(file_name)
        elif file_type == 'flv':
            song = AudioSegment.from_flv(file_name)
        elif file_type == 'ogg':
            song = AudioSegment.from_flv(file_name)
        if song is not None:
            song.export(file_save, format='wav')

    def trans_music_path(self, path_name):
        print 'Start transforming music from :', path_name, 'at ', get_system_time(1)
        time_start = get_system_time(0)
        file_list = get_file_list(path_name)
        for file_name in file_list:
            self.trans_to_wav(file_name)
        time_cost = get_system_time(0) - time_start
        print 'End transforming music from :', path_name, 'at ', get_system_time(1), ' with time_cost:', time_cost

    def trans_music_path_thread(self, path_name):
        # using threading to transform music
        print 'Start transforming music from :', path_name, 'at ', get_system_time(1)
        time_start = get_system_time(0)
        file_list = get_file_list(path_name)
        thread_list = list()
        for file_name in file_list:
            thread_list.append(MusicThread(self.trans_to_wav, (file_name,)))
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        time_cost = get_system_time(0) - time_start
        print 'End transforming music from :', path_name, 'at ', get_system_time(1), ' with time_cost:', time_cost


# test
if __name__ == '__main__':
    path_test = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/'
    MusicToWav().trans_music_path(path_test)
    MusicToWav().trans_music_path_thread(path_test)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Tools.py
# @Author: MoonKuma
# @Date  : 2018/9/10
# @Desc  : Some tools

import os
import pickle
import time


def is_legal_file(file_name):
    return os.path.exists(file_name)


def get_file_list(file_dir):
    file_list = list()
    if not is_legal_file(file_dir):
        print 'file dir:', file_dir, ' not exist'
        return file_list
    for file_name in os.listdir(file_dir):
        file_full_name = os.path.join(file_dir, file_name)
        file_list.append(file_full_name)
    return file_list


def get_system_time(return_type):
    if return_type == 0:
        return time.time()
    if return_type == 1:
        return time.ctime()


def load_object(file_name):
    if not is_legal_file(file_name):
        error_str = 'Error, there exists no file named:', file_name
        raise RuntimeError(error_str)
    f = open(file_name, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj


def dump_object(obj, file_name):
    if is_legal_file(file_name):
        warning_str = 'Warning, there already exists file named:', file_name, ', which will be overwritten automatically'
        print warning_str
    f = open(file_name, 'wb')
    pickle.dump(obj, f)
    f.close()


# test
if __name__ == '__main__':
    path_test = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/'
    get_file_list(path_test)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : SadSongTrainer.py
# @Author: MoonKuma
# @Date  : 2018/9/6
# @Desc  : This is the svm trainer class

import numpy as npy
from sklearn import svm
from sklearn.model_selection import train_test_split
from util.Tools import is_legal_file, dump_object


class SadSongTrainer:

    def __init__(self, data_file):
        self.data_file = data_file
        if not is_legal_file(data_file):
            error_str = 'No such file named:', self.data_file
            raise RuntimeError(error_str)
        self.c = 0.8
        self.gamma = 20
        self.svm_model = svm.SVC(self.c, kernel='rbf', gamma=self.gamma, decision_function_shape='ovr')
        self.data_list = list()  # [x,y]
        self.__load_data()
        self.data_reform_list = list()
        self.reform_factor_max = 20
        self.reform_factor_best = 1
        return

    def __load_data(self):
        data = npy.loadtxt(self.data_file, dtype=float, delimiter=',')
        if len(data) > 1:
            data_size = (len(data), len(data[0]))
            x, y = npy.split(data, (data_size[1]-1,), axis=1)
            result_list = [x, y]
            self.data_list = result_list
            return result_list
        else:
            error_str = 'len(data) is not acceptable:', len(data)
            raise RuntimeError(error_str)

    def __avg_list(self, data_list, avg_range):
        sum_data = 0.0
        count_data = 0
        for i in data_list[avg_range[0]:avg_range[1]]:
            sum_data += i
            count_data += 1
        return sum_data/count_data

    def set_svm_para(self, c, gamma):
        self.c = c
        self.gamma = gamma
        self.svm_model = svm.SVC(self.c, kernel='rbf', gamma=self.gamma, decision_function_shape='ovr')

    def reset_file(self, data_file):
        self.data_file = data_file
        self.__load_data()

    def show_accuracy(self, y_predict, y_real, *note):
        if len(y_predict) != len(y_real) or len(y_predict) == 0:
            print 'require equal and non-zero length from both list, while len(y_predict)', len(
                y_predict), ' and len(y_real)', len(y_real)
            return
        count_total = 0
        count_correct = 0
        for i in range(0, len(y_predict)):
            count_total += 1
            if y_predict[i] == y_real[i]:
                count_correct += 1
        if len(note) == 1:
            report = note[0] + ':' + str(count_correct * 100 / count_total) + '%'
            print report
        return count_correct * 100 / count_total

    # compute svm model based on reformed data list
    def compute_model(self):
        if len(self.data_reform_list) == 0:
            error_str = 'No data in data_reform_list,len(self.data_reform_list)', len(self.data_reform_list)
            raise RuntimeError(error_str)
        x = self.data_reform_list[0]
        y = self.data_reform_list[1]
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
        self.svm_model.fit(x_train, y_train.ravel())
        y_hat_train = self.svm_model.predict(x_train)
        y_hat_test = self.svm_model.predict(x_test)
        return [self.show_accuracy(y_hat_train, y_train), self.show_accuracy(y_hat_test, y_test)]

    # reform data with the average value of each n columns
    # ( this is special for fft data for the nearby frequency is in some way similar)
    def reform_data(self, reform_factor):
        x = self.data_list[0]
        y = self.data_list[1]
        if len(x[0]) < reform_factor:
            error_str = 'len(x[0]) is smaller than reform_factor as len(x[0]):', len(x[0]), ', while reform_factor:', reform_factor
            raise RuntimeError(error_str)
        data_length = len(x[0]) / reform_factor
        data_tail = len(x[0]) % reform_factor
        data_splitter = list()
        x_trans = npy.zeros((len(x), reform_factor))
        for i in range(0, reform_factor-1):
            data_splitter.append(data_length)
        data_splitter.append(data_length+data_tail)
        for x_index in range(0, len(x)):
            x_tmp = x[x_index]
            x_tans_tmp = list()
            for s in range(0, len(data_splitter)):
                avg_range = (s*data_length, s*data_length + data_splitter[s])
                avg_value = self.__avg_list(x_tmp, avg_range)
                x_tans_tmp.append(avg_value)
            x_trans[x_index] = x_tans_tmp
        self.data_reform_list = [x_trans, y]

    # try to identify the best ( with highest test accuracy) separating method based on certain data-sample
    # model_select_table is used to show the tendency, model_select_best give the `best` separator
    def model_select_table(self):
        if self.reform_factor_max > len(self.data_list[0][0]):
            self.reform_factor_max = len(self.data_list[0][0])
        for reform_factor in range(1, self.reform_factor_max+1):
            self.reform_data(reform_factor)
            [y_hat_train, y_hat_test] = self.compute_model()
            report = '[Show Each] reform_factor=' + str(reform_factor) + ' ,y_hat_train:' + str(y_hat_train) + ', y_hat_test:' + str(y_hat_test)
            print report

    def model_select_best(self):
        if self.reform_factor_max > len(self.data_list[0][0]):
            self.reform_factor_max = self.data_list[0][0]
        current_test_accuracy = 0
        for reform_factor in range(1, self.reform_factor_max+1):
            self.reform_data(reform_factor)
            [y_hat_train, y_hat_test] = self.compute_model()
            if y_hat_test > current_test_accuracy:
                current_test_accuracy = y_hat_test
            else:
                report = '[Best] reform_factor=' + str(reform_factor) + ' ,y_hat_train:' + str(y_hat_train) + ', y_hat_test:' + str(y_hat_test)
                print report
                self.reform_factor_best = reform_factor
                return

    def execute(self, save_name):
        self.model_select_table()
        self.model_select_best()
        result_list = [self.reform_factor_best, self.svm_model]
        dump_object(result_list, save_name)


if __name__ == '__main__':
    # test
    test_file = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/Iris_transed'
    save_file = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/test_model.pkl'
    test_obj = SadSongTrainer(test_file)
    test_obj.execute(save_file)
















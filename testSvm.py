#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : testSvm.py
# @Author: MoonKuma
# @Date  : 2018/9/7
# @Desc  : test Svm using an internet example

import numpy as npy
from sklearn import svm
from sklearn.model_selection import train_test_split


def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


def show_accuracy(y_predict, y_real, note):
    if len(y_predict) != len(y_real) or len(y_predict) == 0:
        print 'require equal and non-zero length from both list, while len(y_predict)', len(y_predict), ' and len(y_real)', len(y_real)
        return
    count_total = 0
    count_correct = 0
    for i in range(0, len(y_predict)):
        count_total += 1
        if y_predict[i] == y_real[i]:
            count_correct += 1
    report = note + ':' + str(count_correct*100/count_total) + '%'
    return report

file_name = 'C:/Users/7q/PycharmProjects/SadSong/sample_data/Iris'
data = npy.loadtxt(file_name, dtype=float, delimiter=',', converters={4: iris_type})
x, y = npy.split(data, (4,), axis=1)

x = x[:, :3] # as dimension increased, the accuracy for prediction (both train and test) adds up, which means adding dimension could still benefit the prediction
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
clf.fit(x_train, y_train.ravel())
y_hat = clf.predict(x_train)
show_accuracy(y_hat, y_train, 'train-predict')
y_hat = clf.predict(x_test)
show_accuracy(y_hat, y_test, 'test-predict')


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : testThreading.py
# @Author: MoonKuma
# @Date  : 2018/9/14
# @Desc  : a simple example about using threading to save time


import threading
import time


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        # print "Starting " + self.name
        # run something out of lock
        compute_fibonacci(self.name, self.counter)
        # then run something inside lock
        # threadLock.acquire()
        # print_time(self.name, self.counter, 3)
        # threadLock.release()


def print_time(thread_name, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        counter -= 1


def __fibonacci(n, time_window):
    if n < 1 or time.time() >= time_window:
        return 0
    if n == 1 or n == 2:
        return 1
    return __fibonacci(n-1, time_window) + __fibonacci(n-2, time_window)


def compute_fibonacci(thread_name, period):
    time_1 = int(time.time()) + period
    __fibonacci(99, time_1)
    # print "___%s: %s___" % (thread_name, str(time.time() - time_1 - period))


def test_thread(thread_num, counter):

    # 正常计算
    """
    print "Start ordinary computing at: ", time.ctime()
    time_0 = time.time()
    for i in range(0, thread_num):
        threads_name = "Cycle-" + str(i + 1)
        compute_fibonacci(threads_name, counter)
    time_1 = time.time() - time_0
    print "Exiting ordinary computing at: ", time.ctime(), ", total time cost:", time_1
    """
    # 线程计算
    # threadLock = threading.Lock()
    threads = list()
    # 创建新线程
    for i in range(0, thread_num):
        threads_name = "Thread-" + str(i+1)
        threads.append(MyThread(i+1, threads_name, counter))
    # 开启新线程
    time_0 = time.time()
    print "Start thread computing at: ", time.ctime()
    for t in threads:
        t.start()
    # 等待所有线程完成
    for t in threads:
        t.join()
    time_1 = time.time() - time_0
    print "Exiting all threads at: ", time.ctime(), ", total time cost:", time_1


# -*- coding: utf-8 -*-

def output():
    print('hello,这是')


def output1(data):
    print('hello,这是：{}'.format(data))


def susu(susu):
    print('susu:{}'.format(susu))


def print99():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print('{}x{}={}\t'.format(j, i, i * j), end='')
        print()
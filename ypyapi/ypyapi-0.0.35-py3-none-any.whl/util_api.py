#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/25 17:05
# @Author : yangpingyan@gmail.com
import sqlalchemy
import os
import numpy as np
import matplotlib.pyplot as plt


def append_to_csv(df, csv_file):
    # 当df没有数据或只有列名时， 不做任何操作
    if len(df) < 1:
        print("No data saved")
        return
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=False, header=False, mode='a', encoding='utf_8_sig')
    else:
        df.to_csv(csv_file, index=False, encoding='utf_8_sig')

def kelly_formula_stock():
    probability_win = 0.7
    probability_loss = 1 - probability_win
    ratio_win = 1.5
    ratio_loss = 0.8
    kelly = probability_win/ratio_loss - probability_loss/ratio_win



    print("Kelly is", kelly)
    players = 100
    times = 50
    winners = 0
    balance = 0.0
    for j in range(players):
        m = np.zeros(times)
        m[0] = 100.0
        for i in range(1, times):
            if np.random.randint(2):
                m[i] = m[i - 1] * ratio_win * kelly + m[i - 1] * (1 - kelly)
            else:
                m[i] = m[i - 1] * ratio_loss * kelly + m[i - 1] * (1 - kelly)

        if m[-1] > m[0]:
            winners += 1
        if m[-1] > balance:
            balance = m[-1]
        plt.semilogy(m)

    print('The number of winners is', winners)
    print(balance)
    plt.xlabel('Times')
    plt.ylabel('Balance')
    plt.show()

    return kelly


if __name__ == '__main__':
    print("Mission start!")
    kelly_formula_stock()
    print("Mission complete!")

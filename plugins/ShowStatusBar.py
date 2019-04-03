#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'P喵呜-phpoop'

import sys

# 显示百分比状态栏
class ShowStatusBar():
    # :param number:  '#'号的个数
    # :param symbol:  要显示的“符号”
    def __init__(self, number = 50, symbol = '█'):
        self.number = number
        self.symbol = symbol
        self.filler = 100/number #表示数量每增加多少时添加一个“符号”

    # :param now_number:  当前数量
    # :param total:       总数
    def run(self, now_number, total):
        # 计算当前百分比
        percentage = self._percentage(now_number, total)

        # 显示的符号数量
        show_filler_number = int(percentage / self.filler)

        # 进度条返回
        progress_bar_number = self._progress_bar(show_filler_number)

        # 进度条打印
        try:
            result = '\r%s%d%%-%d/%d\r' % (progress_bar_number, percentage, now_number, total)
            if percentage >= 100:
                result += '\n'
            sys.stdout.write(result)
            sys.stdout.flush()
        except KeyboardInterrupt:
            print('\r用户终止,当前执行进度: %s%%\n' % float(percentage))
            exit()

    # 计算当前百分比
    # :param now_number:  当前的数
    # :param total:       总数
    # :return:            现在所到达百分比
    def _percentage(self, now_number, total):
        return float(now_number / total * 100)

    # 进度条状态现时
    # :param number:  拼接的“符号”数量
    # :return:        返回的结果当前的进度条
    def _progress_bar(self, number):
        # 1. “符号”个数
        show_filler_number = self.symbol * number
 
        # 2. 空格的个数
        space_num = " " * (self.number - number)
 
        return '[%s%s]' % (show_filler_number, space_num)
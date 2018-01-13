# coding=utf-8
'''
Created on 2017年5月15日

@author: jianpinh
'''

import os


def Install():
    commands = (
                u'pip install bs4',
                u'pip install pyyaml',
                u'pip install tushare',
                u'pip install numpy',
                u'pip install pandas',
                u'pip install requests',
                u'pip install xlwt',
                u'pip install xlrd',
                )
    for x in commands:
        print(os.system(x))


if __name__ == '__main__':
    Install()

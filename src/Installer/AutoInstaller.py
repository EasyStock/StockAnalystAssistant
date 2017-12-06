# coding=utf-8
'''
Created on 2017年5月15日

@author: jianpinh
'''

import os


def Install():
    commands = (u'/usr/local/bin/easy_install pip',
                u'/usr/local/bin/pip install bs4',
                u'/usr/local/bin/pip install pyyaml',
                u'/usr/local/bin/pip install tushare',
                u'/usr/local/bin/pip install numpy',
                u'/usr/local/bin/pip install pandas',
                )
    for x in commands:
        print(os.system(x))


if __name__ == '__main__':
    Install()

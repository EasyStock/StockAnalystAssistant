# coding=utf-8
'''
Created on 2018/1/5 23:34
@author: jianpinh

'''


class CStockExamleItem(object):
    def __init__(self):
        self._id = None
        self._date = None
        self._price = None
        self._otherInfo = []

    def initWithList(self,_list):
        if not isinstance(_list,(tuple, list)):
            return

        if len(_list) < 3:
            return

        self._id = _list[0]
        self._date = _list[1]
        self._price = _list[2]

        if len(_list) >= 4:
            self._otherInfo = _list[3:]



    def formatToList(self):
        pass


if __name__ == '__main__':
    pass
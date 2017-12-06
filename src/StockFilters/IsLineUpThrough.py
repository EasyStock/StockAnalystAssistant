# coding=utf-8
'''
Created on 2017-11-23 23:24:23
@author: jianpinh

'''
from StockFilters.StockFilterBase import CStockFilterBase


class CIsLineUpThrough(CStockFilterBase):
    def __init__(self):
        '''
        主要用途: 判断均线是否向上穿过，例如5日均线向上穿过8日均线
        '''
        self._filterName = '向上穿透过滤器'

    def _checkParam(self, data=None, lParam=None, rParam=None):
        failedRes = False
        if data is None:
            return failedRes

        if lParam is None:
            return failedRes

        if not isinstance(data, (list, tuple)):
            return failedRes

        list1 = data[0]
        list2 = data[1]
        size1 = len(list1)
        size2 = len(list2)
        if size1 != size2:
            return failedRes

        rangeDay = int(lParam)
        if size1 < rangeDay:
            return failedRes

        return True

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        '''
        data 是一个list,里面包含了两个列表
        lParam 表明在多少时间内出现向上穿
        返回值:(True,发生向上穿的索引）
        '''
        if not self._checkParam(data, lParam, rParam):
            return (False,)

        list1 = data[0]
        list2 = data[1]

        rangeDay = int(lParam)
        # list1最后一天必须是 大于 list2 的最后一天
        if float(list1[-1]) <= float(list2[-1]):
            return (False,)

        if float(list1[-rangeDay]) >= float(list2[-rangeDay]):
            return (False,)

        lastPositive = 1
        findFlag = False
        for index in range(2, rangeDay+1):
            if float(list1[-index]) <= float(list2[-index]):
                findFlag = True
                break
            else:
                lastPositive = index

        if not findFlag or lastPositive >= rangeDay:
            return (False,)

        for index in range(lastPositive+1, rangeDay+1):
            if float(list1[-index]) >= float(list2[-index]):
                return (False,)

        return (True, lastPositive)


if __name__ == '__main__':
    pass

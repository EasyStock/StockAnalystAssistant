# coding=utf-8
'''
Created on 2017-11-26 08:32:00
@author: jianpinh

'''
from StockFilters.StockFilterBase import CStockFilterBase
from numpy import arctan, pi


class CIsLineDirectionHorizontal(CStockFilterBase):
    def __init__(self):
        '''
        主要用途: 判断均线是否水平的，即横盘，例如5日均线的倒数3天方向是横盘的，或者趋于水平的
        '''
        self._filterName = '线条水平过滤器'

    def _checkParam(self, data=None, lParam=None, rParam=None):
        failedRes = False
        if data is None:
            return failedRes

        if lParam is None:
            return failedRes

        if not isinstance(data, (list, tuple)):
            return failedRes

        size = len(data)
        rangeDay = int(lParam)
        if size < rangeDay:
            return failedRes

        return True

    def _CalcData(self, data):
        size = len(data)
        res = []
        for i in range(size):
            for j in range(i+1, size):
                r = 1.0*(float(data[j]) - float(data[i])) / (j - i)
                res.append(arctan(r))
        return res

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        '''
        data 是一个list,
        lParam 表示要计算倒数几天的
        rParam 表示概率，即概率大于多少表示上升的
        返回值是(true/false, 概率)
        '''
        if not self._checkParam(data, lParam, rParam):
            return (False, -1)

        lastN = lParam
        delta = float(rParam)

        size = len(data)
        res = []
        if lastN >= size:
            res = self._CalcData(data)
        else:
            res = self._CalcData(data[-lastN:])
        if len(res) == 0:
            return (False, -1)
        # 趋势水平应该是 角度在-3度和3度之间，即 -PI/60 < x < -PI/60
        m = [x for x in res if -pi/60.0 < x < pi/60.0]
        ret = 1.0*len(m)/len(res)
        return (ret >= delta, ret)


if __name__ == '__main__':
    pass

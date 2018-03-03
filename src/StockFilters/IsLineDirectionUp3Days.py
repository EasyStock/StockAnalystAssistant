# coding=utf-8
'''
Created on 2018-01-17 22:15:22
@author: jianpinh

'''
from StockFilters.StockFilterBase import CStockFilterBase


class CIsLineDirectionUp3Days(CStockFilterBase):
    '''
    判断均线是否连续3天向上:均线连续3天的增量大于等于0
    '''
    def __init__(self):
        self._filterName = '3日均线连续向上'

    def _checkParam(self, data=None, lParam=None, rParam=None):
        '''
        检查参数:
        1. data 必须是一个list 或者 tuple
        2. data 的长度必须大于60(因为要算55日均线)
        '''
        failedRes = False
        if data is None:
            return failedRes

        if lParam is None:
            return failedRes

        if not isinstance(data, (list, tuple)):
            return failedRes

        size = len(data)
        if size < 60:
            return failedRes

        return True

    def _cacl(self, data=None, lParam=None, rParam=None):
        '''
        计算均线，根据均线判断最后三日是否是向上的
        '''
        from StockMath.AverageLine import AverageLine as avgLine
        avg = avgLine.CAverageLine(int(lParam))
        avgLine = avg.GetLineAverageOfEveryDay(data, 0)
        return (avgLine[-3] <= avgLine[-2] <= avgLine[-1])

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        if not self._checkParam(data, lParam, rParam):
            return (False, -1)

        if self._cacl(data, lParam, rParam):
            return (True, 0)
        else:
            return (False, 0)


if __name__ == '__main__':
    pass
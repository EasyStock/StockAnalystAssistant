# coding=utf-8
'''
Created on 2017-11-20 22:34:55
@author: jianpinh

'''


class CStockQuota_AvgLines(object):
    '''
    均线指标
    '''
    def __init__(self):
        self._avgLines = {}

    def getAvgLine(self, data, param=None):
        if self._avgLines:
            return self._avgLines
        else:
            return self._calcAvgLine(data, param)

    def _calcAvgLine(self, data, param=None):
        '''
        根据均线参数，计算所有的均线，会先清空所有的均线，重新计算
        '''
        # 清空目前所有的均线
        self._avgLines = {}
        if data is None:
            return {}

        if param is None:
            param = (5, 8, 13, 21, 34, 55)

        if not isinstance(param, (list, tuple)):
            return {}

        from StockMath.AverageLine import AverageLine as avgLine
        for x in param:
            key = int(x)
            if key in self._avgLines:
                continue
            avg = avgLine.CAverageLine(key)
            self._avgLines[key] = avg.GetLineAverageOfEveryDay(data, 0)

        return self._avgLines


if __name__ == '__main__':
    pass

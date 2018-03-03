# coding=utf-8
'''
Created on 2018-01-17 22:51:14
@author: jianpinh

'''
from StockFilters.StockFilterBase import CStockFilterBase
from numpy import arctan


class CIsLineAtBottomAndUp(CStockFilterBase):
    '''
    主要功能: 判断34日均线或者55日均线等钝化后的曲线是否触底反弹
    判断依据:
    1. 前 N-3 天的曲线方向是一直向下的,最后三天的曲线开始触底反弹，拐头向上，趋势确立
    '''
    def __init__(self):
        self._filterName = '均线触底反弹过滤器'

    def _checkParam(self, data=None, lParam=None, rParam=None):
        failedRes = False
        if data is None:
            return failedRes

        if lParam is None:
            return failedRes

        if rParam is None:
            return failedRes

        if not isinstance(data, (list, tuple)):
            return failedRes

        size = len(data)
        if size < int(lParam)+10 or size < int(rParam):
            return failedRes

        return True

    def _isLineDown(self, lineData):
        '''
        判断曲线方向是否向下的
        1. 计算两两点之间的 arctan 值, 然后计算arctan 值 小于等于0 的占比
        对于钝化后的曲线来说，临时性的变动很小，所有当方向占比大于90% 以上，则认为是方向向下的
        '''
        size = len(lineData)
        res = []
        for i in range(size):
            for j in range(i+1, size):
                r = 1.0*(float(lineData[j]) - float(lineData[i])) / (j - i)
                res.append(arctan(r))
        m = [x for x in res if x < 0]
        ret = 1.0*len(m)/len(res)
        return (ret >= 0.9)

    def _cacl(self, data=None, lParam=None, rParam=None):
        '''
        1. 计算均线
        2. 计算均线前lParam-3天的方向
        3. 判断N-3 ~ N 这三天的方向
        '''
        from StockMath.AverageLine import AverageLine as avgLine
        avg = avgLine.CAverageLine(int(lParam))
        avgLine = avg.GetLineAverageOfEveryDay(data, 0)
        if not (avgLine[-3] <= avgLine[-2] <= avgLine[-1]):
            return False
        lastN = int(rParam)
        tmp = avgLine[-lastN: -3]
        if not self._isLineDown(tmp):
            return False
        return True

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        '''
        参数说明:
        1.data 是一个list，包含了所有的收盘价，长度必须大于lParam
        2.lParam 表明是几日均线的整数值
        3. rParam 表明要计算的倒数前N日的N
        '''
        if not self._checkParam(data, lParam, rParam):
            return (False, -1)

        if not self._cacl(data, lParam, rParam):
            return (False, 0)

        return (True, 0)


if __name__ == '__main__':
    pass

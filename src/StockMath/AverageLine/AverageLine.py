# coding=utf-8
'''
Created on 2016-11-26 22:40:22
@author: jianpinh

'''
import numpy as np


class CAverageLine(object):
    def __init__(self, param):
        self._K = int(param)

    def GetLineAverage(self, data):
        if data is None:
            return 0

        if len(data) == 0:
            return 0

        if self._K == -1:
            self._K = len(data)

        if len(data) <= self._K:
            return np.average(data)

        tmp = data[-self._K:]
        return np.average(tmp)

    def GetLineAverageOfEveryDay(self, data, fill=None):
        if data is None:
            return []
        res = []
        size = len(data)
        if fill is None:
            if len(data) < self._K:
                return []

        for x in range(self._K-1, len(data)):
            tmp = data[0:x+1]
            avg = self.GetLineAverage(tmp)
            res.append(avg)

        if fill is not None:
            delta = size - len(res)
            ret = [fill]*delta
            ret.extend(res)
            return ret
        else:
            return res


if __name__ == '__main__':
    data = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    t = CAverageLine(5)
    print(data)
    print(t.GetLineAverage(data))
    print(t.GetLineAverageOfEveryDay(data, 1))

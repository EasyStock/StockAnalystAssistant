# coding=utf-8
'''
Created on 2017-11-24 19:59:25
@author: jianpinh

'''
from StockAnalyzers.StockAnalysisBase import CStockAnalysisBase
from StockQuota import StockQuota_AvgLines as SQAL
from StockFilters.IsLineUpThrough import CIsLineUpThrough
import pandas as pd
from StockFilters.IsLineDirectionUp import CIsLineDirectionUp


class CAverageLineThroughAnalysis(CStockAnalysisBase):
    def __init__(self):
        self._analysisName = '均线上穿分析器'

    def _checkParam(self, dataFrame=None,
                    lParam=None, rParam=None):
        if not isinstance(dataFrame, pd.DataFrame):
            return False
        # 数据小于50行的不分析
        if dataFrame.shape[0] < 50:
            return False

        return True

    def _lineNThoughLineM(self, N, M, lineN, lineM, retRes,
                          param=None):
        lineUp = CIsLineUpThrough()
        r1 = lineUp.doFilterLastDay((lineN, lineM), param, None)
        # key1 = u'04_%02d->%02d' % (N, M)
        key2 = u'04_%02d->%02d点' % (N, M)
        if r1[0] is True:
            # retRes[key1] = True
            retRes[key2] = r1[1]
        else:
            # retRes[key1] = False
            retRes[key2] = u''
        return r1[0]

    def _IsLineDirectionUp(self, N, data, retRes, lastN, delta):
        isLineDirection = CIsLineDirectionUp()
        r1 = isLineDirection.doFilterLastDay(data, lastN, delta)
        if retRes is not None:
            # key1 = u'05_%02d日是否向上' % (N)
            key2 = u'05_%02d日向上概率' % (N)
            # retRes[key1] = True
            retRes[key2] = r1[1]
        return r1[0]

    def doManualAnalysis(self, stockId=None, dataFrame=None,
                         lParam=None, rParam=None):
        '''
        '''
        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        stockAvgLines = SQAL.CStockQuota_AvgLines()
        avgLineParam = (5, 8, 13, 21, 34, 55)
        avgLines = stockAvgLines.getAvgLine(closePrice, avgLineParam)
        size = len(dates)
        if lParam is None:
            start = 1
        else:
            start = size - int(lParam)

        ret = []
        for index in range(start, size):
            tmpAvgLine5 = avgLines[5][:index]
            tmpAvgLine8 = avgLines[8][:index]
            tmpAvgLine13 = avgLines[13][:index]
            tmpAvgLine21 = avgLines[21][:index]
            tmpAvgLine34 = avgLines[34][:index]
            tmpAvgLine55 = avgLines[55][:index]

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]

            self._IsLineDirectionUp(5, tmpAvgLine5, res, 5, 0.99)
            self._IsLineDirectionUp(8, tmpAvgLine8, res, 5, 0.85)
            self._IsLineDirectionUp(13, tmpAvgLine13, res, 3, 0.85)
            self._IsLineDirectionUp(21, tmpAvgLine21, res, 3, 0.85)
            if not self._isLine55DirectionUp(tmpAvgLine55):
                continue

            if not self._isLine34DirectionUp(tmpAvgLine34):
                continue

            self._lineNThoughLineM(5, 8, tmpAvgLine5, tmpAvgLine8, res, 10)

            self._lineNThoughLineM(8, 21, tmpAvgLine8, tmpAvgLine21, res, 10)
            self._lineNThoughLineM(13, 21, tmpAvgLine13, tmpAvgLine21, res, 10)

            self._lineNThoughLineM(8, 34, tmpAvgLine8, tmpAvgLine34, res, 10)
            self._lineNThoughLineM(13, 34, tmpAvgLine13, tmpAvgLine34, res, 10)
            self._lineNThoughLineM(21, 34, tmpAvgLine21, tmpAvgLine34, res, 10)

            self._lineNThoughLineM(13, 55, tmpAvgLine13, tmpAvgLine55, res, 10)
            self._lineNThoughLineM(21, 55, tmpAvgLine21, tmpAvgLine55, res, 10)
            self._lineNThoughLineM(34, 55, tmpAvgLine34, tmpAvgLine55, res, 10)
            ret.append(res)
        return ret

    def doAnalysisLastNDay(self, stockId=None, data=None,
                           lastN=1, lParam=None, rParam=None):
        if lastN is None:
            return self.doAnalysisEveryDay(stockId, data, lParam, rParam)
        else:
            if int(lastN) < 1:
                return []
            elif(lastN == 1):
                ret = self.doAnalysisLastDay(stockId, data, lParam, rParam)
                if ret is not None:
                    return [ret, ]
                else:
                    return []
            else:
                return self._doAnalysisLastNDay(stockId, data,
                                                lastN, lParam, rParam)

    def doAnalysisLastDay(self, stockId=None, dataFrame=None,
                          lParam=None, rParam=None):
        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        stockAvgLines = SQAL.CStockQuota_AvgLines()
        avgLineParam = (5, 8, 13, 21, 34, 55)
        avgLines = stockAvgLines.getAvgLine(closePrice, avgLineParam)
        line5 = avgLines[5]
        line8 = avgLines[8]
        line13 = avgLines[13]
        line21 = avgLines[21]
        line34 = avgLines[34]
        line55 = avgLines[55]

        res = {}
        res[u'01_股票代码'] = stockId
        res[u'02_日期'] = dates[-1]
        res[u'03_价格'] = closePrice[-1]
        r1 = self._lineNThoughLineM(8, 34, line8, line34, res, 10)
        r2 = self._lineNThoughLineM(13, 34, line13, line34, res, 10)
        r3 = self._lineNThoughLineM(21, 34, line21, line34, res, 10)
        if not r1 and not r2 and not r3:
            return None

        # 34日均线必须向上
        r34 = self._isLine34DirectionUp(line34)
        if not r34:
            return None

        # 55日均线必须向上
        r55 = self._isLine55DirectionUp(line55)
        if not r55:
           return None

        # 5日均线必须向上
        r4 = self._IsLineDirectionUp(5, line5, None, 5, 0.99)
        if not r4:
            return None

        # 8日均线必须向上
        r5 = self._IsLineDirectionUp(8, line8, None, 3, 0.9)
        if not r5:
            return None

        self._lineNThoughLineM(5, 8, line5, line8, res, 10)

        self._lineNThoughLineM(8, 21, line8, line21, res, 10)
        self._lineNThoughLineM(13, 21, line13, line21, res, 10)
        return res

    def _doAnalysisLastNDay(self, stockId=None, dataFrame=None,
                            lastN=1, lParam=None, rParam=None):

        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        stockAvgLines = SQAL.CStockQuota_AvgLines()
        avgLineParam = (5, 8, 13, 21, 34, 55)
        avgLines = stockAvgLines.getAvgLine(closePrice, avgLineParam)
        size = len(dates)

        ret = []
        for index in range(size-lastN, size):
            line5 = avgLines[5][:index]
            line8 = avgLines[8][:index]
            line13 = avgLines[13][:index]
            line21 = avgLines[21][:index]
            line34 = avgLines[34][:index]
            line55 = avgLines[55][:index]

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]
            r1 = self._lineNThoughLineM(8, 34, line8, line34, res, 10)
            r2 = self._lineNThoughLineM(13, 34, line13, line34, res, 10)
            r3 = self._lineNThoughLineM(21, 34, line21, line34, res, 10)
            if not r1 and not r2 and not r3:
                continue

            # 34日均线必须向上
            r34 = self._isLine34DirectionUp(line34)
            if not r34:
                continue

            # 55日均线必须向上
            r55 = self._isLine55DirectionUp(line55)
            if not r55:
                continue

            # 5日均线必须向上
            r4 = self._IsLineDirectionUp(5, line5, None, 5, 0.99)
            if not r4:
                continue

            # 8日均线必须向上
            r5 = self._IsLineDirectionUp(8, line8, None, 3, 0.9)
            if not r5:
                continue

            self._lineNThoughLineM(5, 8, line5, line8, res, 10)

            self._lineNThoughLineM(8, 21, line8, line21, res, 10)
            self._lineNThoughLineM(13, 21, line13, line21, res, 10)
            ret.append(res)
        return ret

    def doAnalysisEveryDay(self, stockId=None, dataFrame=None,
                           lParam=None, rParam=None):
        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        stockAvgLines = SQAL.CStockQuota_AvgLines()
        avgLineParam = (5, 8, 13, 21, 34, 55)
        avgLines = stockAvgLines.getAvgLine(closePrice, avgLineParam)
        size = len(dates)

        ret = []
        for index in range(1, size):
            line5 = avgLines[5][:index]
            line8 = avgLines[8][:index]
            line13 = avgLines[13][:index]
            line21 = avgLines[21][:index]
            line34 = avgLines[34][:index]
            line55 = avgLines[55][:index]

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]
            r1 = self._lineNThoughLineM(8, 34, line8, line34, res, 10)
            r2 = self._lineNThoughLineM(13, 34, line13, line34, res, 10)
            r3 = self._lineNThoughLineM(21, 34, line21, line34, res, 10)
            if not r1 and not r2 and not r3:
                continue

            # 34日均线必须向上
            r34 = self._isLine34DirectionUp(line34)
            if not r34:
                continue

            # 55日均线必须向上
            r55 = self._isLine55DirectionUp(line55)
            if not r55:
                continue

            # 5日均线必须向上
            r4 = self._IsLineDirectionUp(5, line5, None, 5, 0.99)
            if not r4:
                continue

            # 8日均线必须向上
            r5 = self._IsLineDirectionUp(8, line8, None, 3, 0.9)
            if not r5:
                continue

            self._lineNThoughLineM(5, 8, line5, line8, res, 10)

            self._lineNThoughLineM(8, 21, line8, line21, res, 10)
            self._lineNThoughLineM(13, 21, line13, line21, res, 10)
            ret.append(res)
        return ret

    def _isLine34DirectionUp(self, avgLine34, param = None):
        # 34日均线必须向上, 34日均线钝化严重，所以34日均线必须严格判断
        if len(avgLine34) <= 3:
            return False

        if avgLine34[-2] <= avgLine34[-2] <= avgLine34[-1]:
            return True
        return False

    def _isLine55DirectionUp(self, avgLine55, param = None):
        # 55日均线必须向上, 55日均线钝化严重，所以55日均线必须严格判断
        if len(avgLine55) <= 3:
            return False

        if avgLine55[-2] <= avgLine55[-2] <= avgLine55[-1]:
            return True
        return False

if __name__ == '__main__':
    pass

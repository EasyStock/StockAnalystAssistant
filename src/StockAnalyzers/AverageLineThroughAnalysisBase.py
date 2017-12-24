# coding=utf-8
'''
Created on 2017-11-24 19:59:25
@author: jianpinh

'''
import datetime
from StockAnalyzers.StockAnalysisBase import CStockAnalysisBase
from StockQuota import StockQuota_AvgLines as SQAL
from StockFilters.IsLineUpThrough import CIsLineUpThrough
import pandas as pd
from StockFilters.IsLineDirectionUp import CIsLineDirectionUp


class CAverageLineThroughAnalysisBase(CStockAnalysisBase):
    def __init__(self):
        self._analysisName = '均线上穿分析器基类'

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
        # N 日均线 上穿 M日均线
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
        return r1

    def _isLineDirectionUp(self, N, data, retRes, lastN, delta):
        isLineDirection = CIsLineDirectionUp()
        r1 = isLineDirection.doFilterLastDay(data, lastN, delta)
        if retRes is not None:
            # key1 = u'05_%02d日是否向上' % (N)
            key2 = u'05_%02d日向上概率' % (N)
            # retRes[key1] = True
            retRes[key2] = r1[1]
        return r1[0]

    def _isLine5DirectionUp(self, avgLine5, param = None):
        # 5日均线，从倒数5天到今日的均线必须向上的
        return self._isLineDirectionUp(5, avgLine5, None, 5, 0.99)

    def _isLine8DirectionUp(self, avgLine8, param = None):
        # 8日均线必须向上, 8日均线3天的方向必须向上的
        return self._isLineDirectionUp(8, avgLine8, None, 3, 0.9)

    def _isLine13DirectionUp(self, avgLine13, param = None):
        # 13日均线必须向上, 13日均线2天的方向必须向上的
        return self._isLineDirectionUp(13, avgLine13, None, 2, 0.9)

    def _isLine21DirectionUp(self, avgLine21, param = None):
        # 21日均线必须向上, 21日均线2天的方向必须向上的
        return self._isLineDirectionUp(21, avgLine21, None, 2, 0.9)

    def _isLine34DirectionUp(self, avgLine34, param = None):
        # 34日均线必须向上, 34日均线2天的方向必须向上的
        return self._isLineDirectionUp(34, avgLine34, None, 2, 0.9)

    def _isLine55DirectionUp(self, avgLine55, param = None):
        # 55日均线必须向上, 55日均线2天的方向必须向上的
        return self._isLineDirectionUp(55, avgLine55, None, 2, 0.9)

    def _isConditionMatch(self, avgLines, outRes, lParam=None, rParam=None):
        (line5, line8, line13, line21, line34) = avgLines

        if lParam is None:
            # 5日均线必须向上
            if not self._isLine5DirectionUp(line5):
                return  False
            # 8日均线必须向上
            if not self._isLine8DirectionUp(line8):
                return  False
            if not self._isLine13DirectionUp(line13):
                return  False

            # 一下条件必须满足其一：
            # 1. 8日均线上穿34日均线
            # 2. 13日均线上穿34日均线
            # 3. 21日均线上穿34日均线
            r1 = self._lineNThoughLineM(8, 34, line8, line34, outRes, 10)
            r2 = self._lineNThoughLineM(13, 34, line13, line34, outRes, 10)
            r3 = self._lineNThoughLineM(21, 34, line21, line34, outRes, 10)
            if not r1[0] and not r2[0] and not r3[0]:
                return False

            #添加一些附加信息
            #5日均线上传8，13，21，34
            self._lineNThoughLineM(5, 8, line5, line8, outRes, 10)
            self._lineNThoughLineM(5, 13, line5, line13, outRes, 10)
            self._lineNThoughLineM(5, 21, line5, line21, outRes, 10)
            self._lineNThoughLineM(5, 34, line5, line34, outRes, 10)

            # 8日均线上穿 13，21，34(r1)
            self._lineNThoughLineM(8, 13, line8, line13, outRes, 10)
            self._lineNThoughLineM(8, 21, line8, line21, outRes, 10)

            # 13 穿21，34(r2)
            self._lineNThoughLineM(13, 21, line13, line21, outRes, 10)

            # 21 穿 34(r3)
            return True
        else:
            self._isLine5DirectionUp(line5)
            self._isLine8DirectionUp(line8)

            self._lineNThoughLineM(5, 8, line5, line8, outRes, 10)
            self._lineNThoughLineM(5, 13, line5, line13, outRes, 10)
            self._lineNThoughLineM(5, 21, line5, line21, outRes, 10)
            self._lineNThoughLineM(5, 34, line5, line34, outRes, 10)

            self._lineNThoughLineM(8, 13, line8, line13, outRes, 10)
            self._lineNThoughLineM(8, 21, line8, line21, outRes, 10)
            self._lineNThoughLineM(8, 34, line8, line34, outRes, 10)

            self._lineNThoughLineM(13, 21, line13, line21, outRes, 10)
            self._lineNThoughLineM(13, 34, line13, line34, outRes, 10)

            self._lineNThoughLineM(21, 34, line21, line34, outRes, 10)
            return True



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
            line5 = avgLines[5][:index]
            line8 = avgLines[8][:index]
            line13 = avgLines[13][:index]
            line21 = avgLines[21][:index]
            line34 = avgLines[34][:index]

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]

            subAvgLine = (line5, line8, line13, line21, line34)
            # set the lparam is not None
            if self._isConditionMatch(subAvgLine, res, ()) is False:
                continue
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

    def _isSuspension(self,dates):
        if dates is None:
            return True

        if not isinstance(dates,(list, tuple)):
            return True

        #新股不做分析
        if len(dates) < 50:
            return True

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=-3)
        last3DayStr = tomorrow.strftime('%Y-%m-%d')
        if dates[-1]< last3DayStr:
            print dates[-1], last3DayStr
            return True
        return False
    
    def doAnalysisLastDay(self, stockId=None, dataFrame=None,
                          lParam=None, rParam=None):
        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        stockAvgLines = SQAL.CStockQuota_AvgLines()
        avgLineParam = (5, 8, 13, 21, 34, 55)
        avgLines_dict = stockAvgLines.getAvgLine(closePrice, avgLineParam)
        line5 = avgLines_dict[5]
        line8 = avgLines_dict[8]
        line13 = avgLines_dict[13]
        line21 = avgLines_dict[21]
        line34 = avgLines_dict[34]

        res = {}
        res[u'01_股票代码'] = stockId
        res[u'02_日期'] = dates[-1]
        res[u'03_价格'] = closePrice[-1]

        avgLine = (line5, line8, line13, line21, line34)
        if self._isConditionMatch(avgLine, res) is False:
            return None

        # 停盘的股票过滤掉
        if self._isSuspension(dates):
            return None

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

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]

            subAvgLine = (line5, line8, line13, line21, line34)
            if self._isConditionMatch(subAvgLine, res) is False:
                continue

            # 停盘的股票过滤掉
            if self._isSuspension(dates[:index+1]):
                continue
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

            res = {}
            res[u'01_股票代码'] = stockId
            res[u'02_日期'] = dates[index]
            res[u'03_价格'] = closePrice[index]

            subAvgLine = (line5, line8, line13, line21, line34)
            if self._isConditionMatch(subAvgLine, res) is False:
                continue

            # 停盘的股票过滤掉
            if self._isSuspension(dates[:index+1]):
                continue

            ret.append(res)
        return ret


if __name__ == '__main__':
    pass

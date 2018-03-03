# coding=utf-8
'''
Created on 2018-01-18 22:45:49
@author: jianpinh

'''
from StockAnalyzers.StockAnalysisBase import CStockAnalysisBase
import pandas as pd
from StockFilters.IsLineAtBottomAndUp import CIsLineAtBottomAndUp


class CAverageLineAtBottomAndUpAnalysis(CStockAnalysisBase):
    def __init__(self):
        '''
        均线触底反弹分析器：
        主要是34日均线或者55日均线这样钝化后的均线,触底反弹了，表示可以适量买入了
        '''
        self._analysisName = '均线触底反弹分析器'

    def _checkParam(self, stockId=None, dataFrame=None,
                    lParam=None, rParam=None):
        if not isinstance(dataFrame, pd.DataFrame):
            return False
        # 数据小于50行的不分析
        if dataFrame.shape[0] < 50:
            return False

        return True

    def doAnalysisEveryDay(self, stockId=None, dataFrame=None,
                           lParam=None, rParam=None):
        pass

    def doAnalysisLastDay(self, stockId=None, dataFrame=None,
                          lParam=None, rParam=None):
        if not self._checkParam(dataFrame, lParam, rParam):
            return None

        dates = dataFrame.ix[:, 0].tolist()  # 第0列为日期
        closePrice = dataFrame.ix[:, 2].tolist()  # 第二列为收盘价
        bottomUp = CIsLineAtBottomAndUp()
        if not bottomUp.doFilterLastDay(closePrice, lParam, rParam):
            return None
        res = {}
        res[u'01_股票代码'] = stockId
        res[u'02_日期'] = dates[-1]
        res[u'03_价格'] = closePrice[-1]
        return res

    def doAnalysisLastNDay(self, stockId=None, dataFrame=None,
                           lastN=1, lParam=None, rParam=None):
        pass

    def doManualAnalysis(self, stockId=None, dataFrame=None,
                         lParam=None, rParam=None):
        pass


if __name__ == '__main__':
    pass

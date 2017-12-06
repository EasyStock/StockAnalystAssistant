# coding=utf-8
'''
Created on 2017年11月20日

@author: jianpinh
'''

from StockQuota import StockQuota_AvgLines as SQAL
import pandas as pd
from Utility.PathUtil import IsFileExist


class CStockAnalysisQuotaMgr(object):
    def __init__(self):
        '''
        股票的指标管理
        '''
        self._stockID = None
        self._fileName = None
        self._rawData = None  # DataFrame
        self._avgLines_closePrice = None  # instance of CStockQuota_AvgLines
        self._mergedData = None   # DataFrame

    def _reset(self):
        self._stockID = None
        self._fileName = None
        self._rawData = None
        self._avgLines_closePrice = None

    def readFromFile(self, fileName):
        '''
        将excel 中的原始数据读取出来
        '''
        self._reset()
        if IsFileExist(fileName) is False:
            return

        self._fileName = fileName
        dataFrame = pd.read_excel(fileName)
        self._rawData = dataFrame
        self._rawDataTitle = dataFrame.columns.tolist()
        # print(self._rawData)
        tmpName = fileName[fileName.rfind('/')+1:fileName.rfind('.')]
        self._stockID = tmpName.split('_')[0]

    def getAvgLines(self, param=None):
        if self._rawData is None:
            return None

        if self._avgLines_closePrice is None:
            self._avgLines_closePrice = SQAL.CStockQuota_AvgLines()
        closePrice = self._rawData.ix[:, 2].tolist()  # 第二列为收盘价
        return self._avgLines_closePrice.getAvgLine(closePrice, param)

    def getMergeData(self):
        '''
        将原始数据与算好后的均线合并成一个DataFrame
        '''
        if self._mergedData is not None:
            return self._mergedData

        if self._rawData is None:
            return None

        if self._avgLines_closePrice is None:
            return None

        keys = sorted(self._avgLines_closePrice._avgLines.keys())
        self._mergedData = self._rawData.copy()
        # 将所有的均线合并到array 里面去
        for key in keys:
            title = u'%02d日均线' % (key)
            self._mergedData[title] = self._avgLines_closePrice._avgLines[key]
        self._mergedTitle = self._mergedData.columns.tolist()
        return self._mergedData

    def saveToFile(self, fileName):
        # 将合并好的数据转成dataFrame 然后存储成Excel文件
        mergedData = self.getMergeData()
        mergedData.to_excel(fileName, encoding='GBK', index=False)


if __name__ == '__main__':
    mgr = CStockAnalysisQuotaMgr()
    fileName = u'/Volumes/Data/StockData/合并后的股票历史信息/后复权/000022_2002 ~ 2017.xls'
    mgr.readFromFile(fileName)
    mgr.getAvgLines((5, 8, 13, 21, 34, 55, 89, 144, 233, 377))
    mgr.getMergeData()
    mgr.saveToFile(u'/tmp/dd.xls')

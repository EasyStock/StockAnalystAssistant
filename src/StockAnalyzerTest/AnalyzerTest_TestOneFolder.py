# coding=utf-8
'''
Created on 2017年11月26日

@author: jianpinh
'''

from StockAnalyzers import AverageLineThroughAnalysis as ALTA
import time
from Utility.PathUtil import CheckFileName


def TestOneFolder_ALTA(folder, saveFolder, retFileFullName):
    '''
    均线穿过分析
    '''
    CheckFileName(saveFolder)
    analyzer = ALTA.CAverageLineThroughAnalysis()
    # 分析倒数一天的数据
    res = analyzer.AnalysisOneFolder(folder, 1, None, None)
    analyzer.SaveAnalysisResultToFile(res, retFileFullName)

    for stockID in res:
        fileName = u'%s%s.xls' % (folder, stockID)
        print(stockID)
        saveFile = u'%s/%s.xls' % (saveFolder, stockID)
        test = ALTA.CAverageLineThroughAnalysis()
        result = test.doManualTest(fileName, 30, None)
        test.SaveAnalysisResultToFile(result, saveFile)


def TestOneFolder(analysizeName, folder, saveFolder=u'/tmp/均线穿过分析/'):
    '''
    analysizeName 可以是: AverageLineThroughAnalysis,
                        PositiveConverNegativeAnalysis
    '''
    t = time.localtime()
    ti = u'%04d%02d%02d_%02d%2d%02d' % (t.tm_year, t.tm_mon, t.tm_mday,
                                        t.tm_hour, t.tm_min, t.tm_sec)
    saveFolder = u'%s/%04d%02d%02d' % (saveFolder, t.tm_year,
                                       t.tm_mon, t.tm_mday)
    if analysizeName == 'AverageLineThroughAnalysis':
        retFileFullName = u'%s/均线穿过分析%s.xls' % (saveFolder, ti)
        TestOneFolder_ALTA(folder, saveFolder, retFileFullName)


if __name__ == '__main__':
    folder = u'/Volumes/Data/StockData/所有股票历史信息/后复权/同花顺/XLS/'
    analysize = 'AverageLineThroughAnalysis'
    TestOneFolder(analysize, folder)

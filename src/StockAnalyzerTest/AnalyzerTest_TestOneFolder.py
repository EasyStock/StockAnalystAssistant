# coding=utf-8
'''
Created on 2017年11月26日

@author: jianpinh
'''

from StockAnalyzers import AverageLineThroughAnalysisBase as ALTA
from StockAnalyzers import AverageLineThroughAnalysis21_34 as ALTA21_34
from StockAnalyzers import AverageLineThroughAnalysis13_34 as ALTA13_34
from StockAnalyzers import AverageLineThroughAnalysis8_34 as ALTA8_34
import time

from StockAnalyzers.StockAnalysisBase import AnalysisOneFolderWithMultiProcess
from Utility.PathUtil import CheckFileName


def TestOneFolder_ALTA_8_34(folder, saveFolder, retFileFullName):
    '''
    均线穿过分析
    '''
    CheckFileName(saveFolder)
    analyzer = ALTA8_34.CAverageLineThroughAnalysis8_34()
    res = AnalysisOneFolderWithMultiProcess(folder, analyzer, 1, None, None)
    # 分析倒数一天的数据
    analyzer.SaveAnalysisResultToFile(res, retFileFullName)
    for stockID in res:
        fileName = u'%s%s.xls' % (folder, stockID)
        print(stockID)
        saveFile = u'%s/8_34/%s.xls' % (saveFolder, stockID)
        test = ALTA8_34.CAverageLineThroughAnalysis8_34()
        result = test.doManualTest(fileName, 30, None)
        test.SaveAnalysisResultToFile(result, saveFile)

def TestOneFolder_ALTA_13_34(folder, saveFolder, retFileFullName):
    '''
    均线穿过分析
    '''
    CheckFileName(saveFolder)
    analyzer = ALTA13_34.CAverageLineThroughAnalysis13_34()
    res = AnalysisOneFolderWithMultiProcess(folder, analyzer, 1, None, None)
    # 分析倒数一天的数据
    analyzer.SaveAnalysisResultToFile(res, retFileFullName)
    for stockID in res:
        fileName = u'%s%s.xls' % (folder, stockID)
        print(stockID)
        saveFile = u'%s/13_34/%s.xls' % (saveFolder, stockID)
        test = ALTA13_34.CAverageLineThroughAnalysis13_34()
        result = test.doManualTest(fileName, 30, None)
        test.SaveAnalysisResultToFile(result, saveFile)

def TestOneFolder_ALTA_21_34(folder, saveFolder, retFileFullName):
    '''
    均线穿过分析
    '''
    CheckFileName(saveFolder)
    analyzer = ALTA21_34.CAverageLineThroughAnalysis21_34()
    res = AnalysisOneFolderWithMultiProcess(folder,analyzer, 1, None, None)
    # 分析倒数一天的数据
    analyzer.SaveAnalysisResultToFile(res, retFileFullName)
    for stockID in res:
        fileName = u'%s%s.xls' % (folder, stockID)
        print(stockID)
        saveFile = u'%s/21_34/%s.xls' % (saveFolder, stockID)
        test = ALTA21_34.CAverageLineThroughAnalysis21_34()
        result = test.doManualTest(fileName, 30, None)
        test.SaveAnalysisResultToFile(result, saveFile)

def TestOneFolder_ALTA(folder, saveFolder, retFileFullName):
    CheckFileName(saveFolder)
    analyzer = ALTA.CAverageLineThroughAnalysisBase()
    res = AnalysisOneFolderWithMultiProcess(folder, analyzer, 1, None, None)
    # 分析倒数一天的数据
    analyzer.SaveAnalysisResultToFile(res, retFileFullName)
    for stockID in res:
        fileName = u'%s%s.xls' % (folder, stockID)
        print(stockID)
        saveFile = u'%s/all/%s.xls' % (saveFolder, stockID)
        test = ALTA.CAverageLineThroughAnalysisBase()
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
    if analysizeName == 'AverageLineThroughAnalysis_21_34':
        retFileFullName = u'%s/均线穿过分析%s.xls' % (saveFolder, ti)
        TestOneFolder_ALTA(folder, saveFolder, retFileFullName)
    elif analysizeName == 'AverageLineThroughAnalysis':
        retFileFullName = u'%s/21_34均线穿过分析%s.xls' % (saveFolder, ti)
        TestOneFolder_ALTA_21_34(folder, saveFolder, retFileFullName)

        retFileFullName = u'%s/13_34均线穿过分析%s.xls' % (saveFolder, ti)
        TestOneFolder_ALTA_13_34(folder, saveFolder, retFileFullName)

        retFileFullName = u'%s/8_34均线穿过分析%s.xls' % (saveFolder, ti)
        TestOneFolder_ALTA_8_34(folder, saveFolder, retFileFullName)


if __name__ == '__main__':
    folder = u'/Volumes/Data/StockData/所有股票历史信息/后复权/同花顺/XLS/'
    analysize = 'AverageLineThroughAnalysis_21_34'
    TestOneFolder(analysize, folder)

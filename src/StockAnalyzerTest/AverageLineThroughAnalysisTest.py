# coding=utf-8
'''
Created on 2017年11月25日

@author: jianpinh
'''
from StockAnalyzers import AverageLineThroughAnalysis as ALTA
import test


def TestOneFile():
    fileName = u'/Volumes/Data/StockData/合并后的股票历史信息/600460_2003 ~ 2017.xls'
    retFileFullName = u'/Volumes/Data/StockData/合并后的股票历史信息/600460.xls'
    test = ALTA.CAverageLineThroughAnalysis()
    result = test.AnalysOneFile(fileName, None, None, None)
    test.SaveAnalysisResultToFile(result, retFileFullName)
    print (retFileFullName)


def TestOneFolder():
    # folder = u'/Volumes/Data/StockData/合并后的股票历史信息/后复权/'
    folder = u'/Volumes/Data/StockData/所有股票历史信息/后复权/同花顺/XLS/'
    retFileFullName = u'/Volumes/Data/StockData/合并后的股票历史信息/ALTAResult.xls'
    test = ALTA.CAverageLineThroughAnalysis()
    result = test.AnalysisOneFolder(folder, 1, None, None)
    test.SaveAnalysisResultToFile(result, retFileFullName)
    print (retFileFullName)


def DoManualTest_OneFile():
    stockIDs = [
        "600581", "002218", "600234", "000576", "000703", "000983",
        "002110", "000761", "002106", "600740", "601677", "600621",
        "600801", "600782", "600282", "600760", "600280", "600641",
        "600206", "600362", "600321", "000936", "002058", "000932",
        "600188", "601699", "002079", "600808", "600971", "002113",
        "002244", "000898", "002733", "601233", "600171", "600400",
        "601636", "600569", "600295", "603005", "600466", "600770"
        ]

    saveFolder = '/Volumes/Data/StockData/FF/'
    folder = u'/Volumes/Data/StockData/所有股票历史信息/后复权/同花顺/XLS/'
    for stockID in stockIDs:
        fileName = u'%s%s.xls' % (folder, stockID)
        saveFile = '%s/%s.xls' % (saveFolder, stockID)
        test = ALTA.CAverageLineThroughAnalysis()
        result = test.doManualTest(fileName, 30, None)
        test.SaveAnalysisResultToFile(result, saveFile)


if __name__ == '__main__':
    DoManualTest_OneFile()

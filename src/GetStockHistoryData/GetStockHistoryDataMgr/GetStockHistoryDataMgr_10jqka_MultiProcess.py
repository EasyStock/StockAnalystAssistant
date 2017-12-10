# coding=utf-8
'''
Created on 2017年11月29日

@author: jianpinh
'''
from Queue import Queue
from time import sleep

from GetStockHistoryData.Engines import Constants_10jqka as HDEC
import re

from Utility.MultiProcessMgr import CMultiProcessMgr
from Utility.PathUtil import DeleteFolderNotEmpty, CheckFileName, IsFileExist
import datetime

from GetStockHistoryData.Engines import HistoryDataEngine_10jqka as jqka

cookieIndex = 0
_CookieList = HDEC.eng_10jqka_CookieList
_cookieQueue = Queue()

def _initCookieQueue():
    global _CookieList
    for x in _CookieList:
        _cookieQueue.put(x)

def _getNextCookie():
    ret = _cookieQueue.get()
    _cookieQueue.put(ret)
    return  ret

def GetAllHistoryData_MultiProcess_Fun(param):
    sleep(0.01)
    try:
        [eng, stockID, autype, cookie, file_name] = param
        dataFrame = eng.getHistoryDataFromStartToNow(stockID, autype, cookie)
        if dataFrame is None:
            print('stockID:%06d data is none' % (int(stockID)))
            return False
        sleep(0.01)
        dataFrame.to_excel(file_name, encoding='GBK', index=False)
        return True
    except Exception:
        return False


def GetAllHistoryDataAndSaveTo_MultiProcess(folder, autype='hfq', forceUpdate=False):
    if autype == 'hfq':
        subFolder = u'%s/后复权/同花顺/XLS/' % (folder)
    elif autype == 'qfq':
        subFolder = u'%s/前复权/同花顺/XLS/' % (folder)
    elif autype == 'bfq':
        subFolder = u'%s/不复权/同花顺/XLS/' % (folder)
    else:
        subFolder = u'%s/后复权/同花顺/XLS/' % (folder)
    if forceUpdate:
        DeleteFolderNotEmpty(subFolder)
    CheckFileName(subFolder)

    import tushare as ts
    allStock = ts.get_stock_basics()
    sortedIndexs = sorted(allStock.index)
    jobs = []
    _initCookieQueue()
    for stockID in sortedIndexs:
        # 过滤掉创业板
        if re.findall("^30\d", stockID):
            continue
        file_name = u'%s/%s.xls' % (subFolder, stockID)
        if IsFileExist(file_name):
            continue
        cookie = _getNextCookie()
        eng = jqka.CHisotryDataEngine_10jqka()
        jobs.append([eng, stockID, autype, cookie, file_name])

    mgr = CMultiProcessMgr()
    mgr.StartMultiProcess(10, jobs, GetAllHistoryData_MultiProcess_Fun,False)


if __name__ == '__main__':
    foder = u'/Volumes/Data/StockData/所有股票历史信息/'
    GetAllHistoryDataAndSaveTo_MultiProcess(foder, 'hfq', True)

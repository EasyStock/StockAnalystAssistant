# coding=utf-8
'''
Created on 2017年11月29日

@author: jianpinh
'''
from time import sleep

from GetStockHistoryData.Engines import Constants_10jqka as HDEC
import re
from Utility.PathUtil import DeleteFolderNotEmpty, CheckFileName, IsFileExist
import datetime

from GetStockHistoryData.Engines import HistoryDataEngine_10jqka as jqka

cookieIndex = 0
_CookieList = HDEC.eng_10jqka_CookieList


def _getNextCookie():
    global _CookieList
    global cookieIndex
    if cookieIndex >= len(_CookieList):
        cookieIndex = 0
    cookie = _CookieList[cookieIndex]
    cookieIndex += 1
    return cookie


def GetAllHistoryDataAndSaveTo(folder, autype='hfq', forceUpdate=False):
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
    eng = jqka.CHisotryDataEngine_10jqka()
    count = 1
    start = datetime.datetime.now()
    last = start
    size = len(allStock.index)
    sortedIndexs = sorted(allStock.index)
    index = 1
    for stockID in sortedIndexs:
        # 过滤掉创业板
        if re.findall("^30\d", stockID):
            count += 1
            continue
        file_name = u'%s/%s.xls' % (subFolder, stockID)
        if IsFileExist(file_name):
            count += 1
            continue
        cookie = _getNextCookie()
        dataFrame = eng.getHistoryDataFromStartToNow(stockID, autype, cookie)
        #dataFrame = eng.getHistoryDataLastDay(stockID, autype, cookie)
        sleep(0.01)
        if dataFrame is None:
            print('stockID:%06d data is none' % (int(stockID)))
            continue
        dataFrame.to_excel(file_name, encoding='GBK', index=False)
        current = datetime.datetime.now()
        t = (current - last)
        total = current - start
        print('==StockID:%s,index:%d,all:%d,remain:%d,    \
              time:%s,totalTime:%s==' % (stockID, index, size, size-count,
                                         t, total))
        last = current
        count += 1
        index += 1
    allTime = datetime.datetime.now() - start
    print('allTime:%s' % (allTime))


if __name__ == '__main__':
    foder = u'/Volumes/Data/StockData/所有股票历史信息/'
    GetAllHistoryDataAndSaveTo(foder, 'hfq', False)

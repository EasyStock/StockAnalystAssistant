# coding=utf-8
'''
Created on 2017-10-27 23:00:38
@author: jianpinh

'''
# import GetStockHistoryData.Engines.HistoryDataEngineBase as hdeb
import httplib
import pandas as pd
from GetStockHistoryData.Engines.HistoryDataEngineBase import CHistoryDataEngineBase


class CHisotryDataEngine_10jqka(CHistoryDataEngineBase):
    def __init__(self, logger=None):
        super(CHisotryDataEngine_10jqka, self).__init__(logger)
        self._engineName = '同花顺'

    def _IsListSorted(self, lst):
        return sorted(lst) == lst or sorted(lst, reverse=True) == lst

    def _CheckSortYear(self, sortYear):
        if not isinstance(sortYear, (list, tuple)):
            return False
        res = [[], []]
        for item in sortYear:
            if len(item) != 2:
                raise Exception('sortYear data error')
            year = item[0]
            count = item[1]
            if year in res[0]:
                raise Exception('sortYear data error:year exist')
            res[0].append(year)
            res[1].append(count)

        if not self._IsListSorted(res[0]):
            return False

        return True

    def _GetRealHisotryData(self, data):
        '''
        将数据解析成字典
        '''
        if data is None:
            return None

        if not isinstance(data, (str, unicode)):
            return None
        if len(data) == 0:
            return None
        firstIndex = data.find('(')
        if firstIndex == -1:
            return None
        endIndex = data.rfind(')')
        if endIndex is None:
            return None
        subData = data[firstIndex+1:endIndex]
        formatedData = eval(subData)
        return formatedData

    def _CheckData(self, data):
        formatedData = self._GetRealHisotryData(data)
        if formatedData is None:
            return None

        if 'sortYear' not in formatedData:
            return None

        if 'price' not in formatedData:
            return None

        if 'volumn' not in formatedData:
            return None

        if 'dates' not in formatedData:
            return None

        return formatedData

    def _ParseDataFrom10jqka_lastDay(self, stockID, data):
        formatedData = self._GetRealHisotryData(data)
        if formatedData is None:
            return None
        firstKey = 'hs_%06d' % (int(stockID))
        if firstKey not in formatedData:
            return None
        subDict = formatedData[firstKey]
        # 日期
        if '1' not in subDict:
            return None

        # 开盘价
        if '7' not in subDict:
            return None

        # 最高价
        if '8' not in subDict:
            return None

        # 最低价
        if '9' not in subDict:
            return None

        # 收盘价
        if '11' not in subDict:
            return None

        # 成交量
        if '13' not in subDict:
            return None

        # 成交额
        if '19' not in subDict:
            return None
        date = subDict['1']
        priceO = subDict['7']
        priceC = subDict['11']
        priceH = subDict['8']
        priceL = subDict['9']
        volumn = subDict['13']

        historyData = [[date, priceO, priceC, priceH, priceL, volumn], ]
        title = [u'日期', u'开盘价', u'收盘价', u'最高价', u'最低价',  u'成交量(股)']
        dataframe = pd.DataFrame(historyData, columns=title)

        return dataframe

    def _ParseDataFrom10jqka_FromStartToNow(self, stockID, data):
        formatedData = self._CheckData(data)
        if formatedData is None:
            return None

        sortYear = formatedData['sortYear']
        price = formatedData['price'].split(',')
        volumn = formatedData['volumn'].split(',')
        dates = formatedData['dates'].split(',')
        if not self._CheckSortYear(sortYear):
            return None

        index = 0
        # stockName = formatedData['name'].decode('unicode_escape')
        # .encode('utf-8')
        if not isinstance(price, (list, tuple)) or len(price) == 0:
            return None

        if not isinstance(volumn, (list, tuple)) or len(volumn) == 0:
            return None

        if not isinstance(dates, (list, tuple)) or len(dates) == 0:
            return None

        historyData = []
        for item in sortYear:
            year = item[0]
            count = item[1]
            try:
                for x in range(count):

                    minP = float(int(price[(index + x)*4])/100.0)
                    openP = float(int(price[(index + x)*4+1])/100.0 + minP)
                    highP = float(int(price[(index + x)*4+2])/100.0 + minP)
                    closeP = float(int(price[(index + x)*4+3])/100.0 + minP)
                    date = dates[(index + x)]
                    fdate = '%s-%s-%s' % (year, date[:2], date[2:])
                    v = volumn[(index + x)]
                    oneDayData = [fdate, openP, closeP, highP, minP, v]
                    historyData.append(oneDayData)
            except Exception:
                print(stockID)
                print(price)
                print(x)
                continue
            index = index + count
        title = [u'日期', u'开盘价', u'收盘价', u'最高价', u'最低价',  u'成交量(股)']
        dataframe = pd.DataFrame(historyData, columns=title)
        return dataframe

    def getHistoryDataFromStartToNow(self, stockID, autype='hfq',
                                     lParam=None, rParam=None):
        '''
        lParam 为cookie 值
        rParam 必须为None，默认会自动计算叠加递归层级
        '''
        if rParam is None:
            rParam = 1
        else:
            rParam += 1
            if rParam >= 2:
                print('Current lparam = %s' % (rParam))

            if rParam > 5:
                return None

        if lParam is None:
            return None

        site = 'd.10jqka.com.cn'
        stockType = 2
        if autype == 'bfq':
            stockType = 0
        elif autype == 'qfq':
            stockType = 1
        else:
            stockType = 2
        url = '/v6/line/hs_%06d/%02d/all.js' % (int(stockID), stockType)
        head = {
                'referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
                }

        head['Cookie'] = lParam
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url, headers=head)
        try:
            r1 = conn.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                data = r1.read()
            elif r1.status == 403:
                print('403')
                return self.getHistoryDataFromStartToNow(stockID, autype,
                                                         lParam, rParam)
            else:
                return None
        except Exception as e:
            print(e)
            return self.getHistoryDataFromStartToNow(stockID, autype,
                                                     lParam, rParam)
        return self._ParseDataFrom10jqka_FromStartToNow(stockID, data)

    def getHistoryDataLastDay(self, stockID, autype='hfq',
                              lParam=None, rParam=None):
        '''
        获取最后一个交易日的历史数据
        lParam 为cookie 值
        rParam 必须为None，默认会自动计算叠加递归层级
        '''
        if rParam is None:
            rParam = 1
        else:
            rParam += 1
            if rParam >= 2:
                print('Current lparam = %s' % (rParam))

            if rParam > 5:
                return None

        if lParam is None:
            return None

        site = 'd.10jqka.com.cn'
        stockType = 2
        if autype == 'bfq':
            stockType = 0
        elif autype == 'qfq':
            stockType = 1
        else:
            stockType = 2
        url = '/v6/line/hs_%06d/%02d/today.js' % (int(stockID), stockType)
        head = {
                'referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
                }
        head['Cookie'] = lParam
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url, headers=head)
        try:
            r1 = conn.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                data = r1.read()
            elif r1.status == 403:
                print('403')
                return self.getHistoryDataLastDay(stockID, autype,
                                                  lParam, rParam)
            else:
                return None
        except Exception as e:
            print(e)
            return self.getHistoryDataLastDay(stockID, autype,
                                              lParam, rParam)

        return self._ParseDataFrom10jqka_lastDay(stockID, data)


if __name__ == '__main__':
    pass

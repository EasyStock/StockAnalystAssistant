# coding=utf-8
"""
Created on 2017-10-27 20:20:07
@author: jianpinh

"""


class CHistoryDataEngineBase(object):
    def __init__(self, logger=None):
        self._engineName = ''
        self._logger = logger

    def get_engine_name(self):
        return self._engineName

    def getHistoryDataOfOneQuarter(self, stockID, year, quarter,
                                   autype='hfq', lParam=None, rParam=None):
        raise Exception('not implement')

    def getHistoryDataFromStartToNow(self, stockID, autype='hfq', lParam=None,
                                     rParam=None):

        raise Exception('not implement')

    def getHistoryDataOfOneQuarterWithStocks(self, stockIDs, year, quarter,
                                             autype='hfq',
                                             lParam=None, rParam=None):
        raise Exception('not implement')

    def getHistoryDataTitle(self):
        raise Exception('not implement')

    engineName = property(get_engine_name, None, None, None)


if __name__ == '__main__':
    pass

# coding=utf-8
'''
Created on 2017-10-26 19:07:36
@author: jianpinh

'''


class CStockFilterBase(object):
    def __init__(self):
        self._filterName = ''

    def get_filter_name(self):
        return self._filterName

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        '''
        过滤最后一天
        '''
        raise Exception('DoFilterLastDay not implemented')

    def doFilterEveryDay(self, data=None, lParam=None, rParam=None):
        '''
        过滤每一天
        '''
        raise Exception('doFilterEveryDay not implemented')

    filterName = property(get_filter_name, None, None, None)


if __name__ == '__main__':
    pass

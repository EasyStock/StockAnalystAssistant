# coding=utf-8
'''
Created on 2017-10-15 12:18:53
@author: jianpinh

'''
from Utility.PathUtil import IsFileExist, IsFolderExist, ListAllTheFilesInDir,\
    CheckFileName
import pandas as pd


class CStockAnalysisBase(object):
    def __init__(self):
        self._analysisName = ''

    def get_analysis_name(self):
        return self._analysisName

    def doManualAnalysis(self, stockId=None, dataFrame=None,
                         lParam=None, rParam=None):
        raise Exception('DoManualAnalysis not implemented')

    def doManualTest(self, fileName, lParam=None, rParam=None):
        if IsFileExist(fileName) is False:
            return []

        dataFrame = pd.read_excel(fileName)
        tmpName = fileName[fileName.rfind('/')+1:fileName.rfind('.')]
        stockId = tmpName.split('_')[0]
        return self.doManualAnalysis(stockId, dataFrame, lParam, rParam)

    def doAnalysisLastNDay(self, stockId=None, dataFrame=None,
                           lastN=1, lParam=None, rParam=None):
        '''
        分析最后N天，例如:
        lastN =1 就是最后一天，
        lastN =2 就是最后两天，
        lastN = None,则分析每一天
        '''
        raise Exception('DoAnalysisLastNDay not implemented')

    def doAnalysisLastDay(self, stockId=None, dataFrame=None,
                          lParam=None, rParam=None):
        '''
        分析最后一天
        '''
        return self.DoAnalysisLastNDay(stockId, dataFrame, 1, lParam, rParam)

    def doAnalysisEveryDay(self, stockId=None, dataFrame=None,
                           lParam=None, rParam=None):
        '''
        分析每一天
        '''
        return self.doAnalysisLastNDay(stockId, dataFrame,
                                       None, lParam, rParam)

    def AnalysOneFile(self, fileName, lastN=1, lParam=None, rParam=None):
        if IsFileExist(fileName) is False:
            return []

        dataFrame = pd.read_excel(fileName)
        tmpName = fileName[fileName.rfind('/')+1:fileName.rfind('.')]
        stockId = tmpName.split('_')[0]
        res = self.doAnalysisLastNDay(stockId, dataFrame,
                                      lastN, lParam, rParam)
        if len(res) == 0:
            return None
        return {stockId: res}

    def AnalysisOneFolder(self, folder, lastN=1, lParam=None, rParam=None):
        if IsFolderExist(folder) is False:
            return None

        files = ListAllTheFilesInDir(folder)
        ret = {}
        for fileName in files:
            #    print fileName
            res = self.AnalysOneFile(fileName, lastN, lParam, rParam)
            if res is None:
                continue
            ret.update(res)
        return ret

    def PrintResult(self, res):
        if isinstance(res, (list, tuple)):
            for x in res:
                if isinstance(x, dict):
                    keys = sorted(x.keys())
                    print('====================')
                    for key in keys:
                        print(key, ':', x[key])
        elif isinstance(res, dict):
            for key in res:
                data = res[key]
                for x in data:
                    if isinstance(x, dict):
                        keys = sorted(x.keys())
                        print('====================')
                        for key in keys:
                            print(key, ':', x[key])

    def SaveAnalysisResultToFile(self, result, retFileFullName,
                                 sheetName='result'):
        title = None
        retData = []
        if isinstance(result, dict):
            for _, value in result.items():
                if not isinstance(value, (list, tuple)):
                    continue
                li = self.ListDictToList(value)
                if title is None:
                    title = li[0]
                if title != li[0]:
                    raise Exception('title not the same')
                retData.extend(li[1:])
        elif isinstance(result, (list, tuple)):
            li = self.ListDictToList(result)
            title = li[0]
            retData.extend(li[1:])
        else:
            raise Exception('data error')

        CheckFileName(retFileFullName)
        res = pd.DataFrame(retData, columns=title)
        res.to_excel(retFileFullName, sheetName, encoding='GBK', index=False)

    def DictToList(self, dict_):
        '''
        字典转换成列表，列表的第一项是排序后的key(列表),第二项是值(列表)
        '''
        if not isinstance(dict_, dict):
            return [[], []]
        keys = sorted(dict_.keys())
        v = []
        for key in keys:
            v.append(dict_[key])

        return [keys, v]

    def ListDictToList(self, ListDict):
        '''
        字典列表 转换成列表
        列表里面都装的是相同类型的字典(相同的Key,不同的value)
        遍历每个字典，然后转换成一个列表，列表的第一项是key(列表),剩下的是对应的值(每一项的值都是一个列表)
        '''
        if not isinstance(ListDict, (list, tuple)):
            return []

        keys = None
        ret = []
        for dict_ in ListDict:
            k, values = self.DictToList(dict_)
            if keys is None:
                keys = k
                ret.append(k)
            if keys != k:
                raise Exception('key not the same')
            ret.append(values)
        return ret

    analysisName = property(get_analysis_name, None, None, None)


if __name__ == '__main__':
    pass

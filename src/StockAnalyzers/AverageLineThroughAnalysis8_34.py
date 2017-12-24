# coding=utf-8
'''
Created on 2017-11-24 19:59:25
@author: jianpinh

'''
from StockAnalyzers.AverageLineThroughAnalysisBase import CAverageLineThroughAnalysisBase


class CAverageLineThroughAnalysis8_34(CAverageLineThroughAnalysisBase):
    def __init__(self):
        self._analysisName = '8日均线上穿34日分析器'


    def _isConditionMatch(self, avgLines, outRes, lParam=None, rParam=None):
        (line5, line8, line13, line21, line34) = avgLines

        if lParam is None:
            # 5日均线必须向上
            if not self._isLine5DirectionUp(line5):
                return  False
            # 8日均线必须向上
            if not self._isLine8DirectionUp(line8):
                return  False

            # 3. 21日均线上穿34日均线
            r1 = self._lineNThoughLineM(8, 34, line8, line34, outRes, 10)
            if not r1[0] or r1[1]>5:
                return False

            #添加一些附加信息
            #5日均线上传8，13，21，34
            self._lineNThoughLineM(5, 8, line5, line8, outRes, 10)
            self._lineNThoughLineM(5, 13, line5, line13, outRes, 10)
            self._lineNThoughLineM(5, 21, line5, line21, outRes, 10)
            self._lineNThoughLineM(5, 34, line5, line34, outRes, 10)

            # 8日均线上穿 13，21，34(r1)
            self._lineNThoughLineM(8, 13, line8, line13, outRes, 10)
            self._lineNThoughLineM(8, 21, line8, line21, outRes, 10)

            # 13 穿21，34(r2)
            self._lineNThoughLineM(13, 21, line13, line21, outRes, 10)
            self._lineNThoughLineM(13, 34, line13, line34, outRes, 10)

            # 21 穿 34(r3)
            self._lineNThoughLineM(21, 34, line21, line34, outRes, 10)
            return True
        else:
            self._isLine5DirectionUp(line5)
            self._isLine8DirectionUp(line8)

            self._lineNThoughLineM(5, 8, line5, line8, outRes, 10)
            self._lineNThoughLineM(5, 13, line5, line13, outRes, 10)
            self._lineNThoughLineM(5, 21, line5, line21, outRes, 10)
            self._lineNThoughLineM(5, 34, line5, line34, outRes, 10)

            self._lineNThoughLineM(8, 13, line8, line13, outRes, 10)
            self._lineNThoughLineM(8, 21, line8, line21, outRes, 10)
            self._lineNThoughLineM(8, 34, line8, line34, outRes, 10)

            self._lineNThoughLineM(13, 21, line13, line21, outRes, 10)
            self._lineNThoughLineM(13, 34, line13, line34, outRes, 10)

            self._lineNThoughLineM(21, 34, line21, line34, outRes, 10)
            return True




if __name__ == '__main__':
    pass

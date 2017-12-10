# coding=utf-8
'''
Created on 2017-10-27 13:29:38
@author: jianpinh

'''
import multiprocessing as mp
import datetime


def multiProcessJobFunc(param):
    if len(param)>=2:
        return param[0](param[1:])
    else:
        return  param[0]()

class CMultiProcessMgr(object):
    def __init__(self):
        self._succeed = 0
        self._failed = 0
        self._allTask = 0
        self._res = None
        self._startTime = None
        self._lastTime = None
    
    def getRes(self):
        return self._res
    
    def callBack(self,param):
        if isinstance(param, (list,tuple)):
            if param[0] is True:
                self._succeed = self._succeed +1
            else:
                self._failed = self._failed +1

            if self._res is not None:
                self._res.put(param[1])
        else:
            if param:
                self._succeed = self._succeed +1
            else:
                self._failed = self._failed +1
        
        remain = self._allTask-self._succeed-self._failed
        percentage = 1.0* (self._succeed+self._failed) / self._allTask *100
        current = datetime.datetime.now()
        timeSpend = None
        if self._lastTime is None:
            timeSpend = self._lastTime
        else:
            timeSpend = current - self._lastTime
        self._lastTime = current
        print 'all:%d, succeed:%d, failed:%d, remain:%d, percetage:%.3f%%,timeSpend:%s'%(self._allTask, self._succeed, self._failed,remain,percentage,timeSpend)
        
    
    def StartMultiProcess(self,processNum = 8, iterableJobs = [], jobFunc=None, mergeResult=False):
        if mergeResult is True:
            self._res = mp.Queue()
        pool = mp.Pool(processNum)
        self._allTask = len(iterableJobs)
        self._startTime = datetime.datetime.now()
        for job in iterableJobs:
            param = [jobFunc,]
            if isinstance(job, (list,tuple)):
                param.extend(job)
            else:
                param.append(job)
            pool.apply_async(multiProcessJobFunc, args = (param,), callback = self.callBack)
            
        pool.close()
        pool.join()
        end = datetime.datetime.now()
        print u'allTimeSpend:%s' % (end - self._startTime)


def testFun(param):
    res = param[0] * param[0]
    return  (True,{res:res})


if __name__ == '__main__':
    mgr = CMultiProcessMgr()
    mgr.StartMultiProcess(2, range(100), testFun, True)
    print mgr.getRes()

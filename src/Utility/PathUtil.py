# coding=utf-8
'''
Created on 2016年12月2日

@author: jianpinh
'''
import os
import re
import shutil
from shutil import rmtree


def IsFolderExist(path):
    if path is None:
        return False

    if (os.path.exists(path) and os.path.isdir(path)) is True:
        return True

    return False


def GetFullPathOfFile(fileName):
    res = GetFullPathAndFileNameOfFile(fileName)
    if res is not None:
        return res[0]
    return None


def GetFullPathAndFileNameOfFile(fileName):
    if fileName is None:
        return None

    res = os.path.split(fileName)
    path = res[0]
    return (os.path.abspath(path), res[1])


def MakeDirectoryIfNotExist(path):
    if path is None:
        return False

    if IsFolderExist(path):
        return True

    os.makedirs(path)
    return True


def GetAbsPath(path):
    if path is None:
        return None

    return os.path.abspath(path)


def CheckFileName(fileName):
    if IsFileExist(fileName) is True:
        return

    path = GetFullPathOfFile(fileName)
    MakeDirectoryIfNotExist(path)


def CheckPathName(path):
    return MakeDirectoryIfNotExist(path)


def IsFileExist(fileName):
    if fileName is None:
        return False

    if (os.path.exists(fileName) and os.path.isfile(fileName)) is True:
        return True

    return False


def IsItAFile(fileName):
    if fileName is None:
        return False

    if (os.path.exists(fileName) and os.path.isfile(fileName)) is True:
        return True

    return False


def IsItAFolder(path):
    if path is None:
        return False

    if (os.path.exists(path) and os.path.isdir(path)) is True:
        return True

    return False


def ListAllTheFolderInDirWithFullPath(path):
    if IsFolderExist(path) is False:
        return ()

    res = []
    for fileName in os.listdir(path):
        fullPath = os.path.join(path, fileName)
        if re.findall("^\.", fileName):
            continue
        if IsFolderExist(fullPath):
            res.append(fullPath)

    return res


def ListAllTheFolderInDirWithoutFullPath(path):
    if IsFolderExist(path) is False:
        return ()

    res = []
    for fileName in os.listdir(path):
        fullPath = os.path.join(path, fileName)
        if re.findall("^\.", fileName):
            continue
        if IsFolderExist(fullPath):
            res.append(fileName)

    return res


def ListAllTheFilesInDir(path):
    if IsFolderExist(path) is False:
        return ()

    res = []
    for fileName in os.listdir(path):
        fullPath = os.path.join(path, fileName)
        if re.findall("^\.", fileName):
            continue

        if IsFileExist(fullPath):
            res.append(fullPath)
    return res


def ListAllTheFilesInDir_Recursion(path):
    if IsFolderExist(path) is False:
        return ()

    res = []
    for root, _, files in os.walk(path):
        for name in files:
            if re.findall("^\.", name):
                continue
            fullPath = os.path.join(root, name)
            if IsFileExist(fullPath):
                res.append(fullPath)

    return res


def JoinPath(path, fileName):
    return os.path.join(path, fileName)


def ReNameFile(oldfileName, newFileName):
    if oldfileName is None or newFileName is None:
        return False

    if IsFileExist(oldfileName) is False:
        return False

    if IsFileExist(newFileName) is True:
        os.remove(newFileName)
    os.renames(oldfileName, newFileName)
    return True


def DeleteFile(fileName):
    if fileName is None:
        return
    if IsFileExist(fileName) is False:
        return
    os.remove(fileName)


def DeleteFolderOfEmpty(folder_):
    if folder_ is None:
        return
    if IsFolderExist(folder_) is False:
        return
    os.rmdir(folder_)


def DeleteFolderNotEmpty(folder_):
    if folder_ is None:
        return

    if IsFolderExist(folder_) is False:
        return

    msg = u'确认要删除目录:%s 吗' % (folder_)
    raw_input(msg)
    rmtree(folder_)


def CopyFileToFolder(filePath, folder):
    if IsFileExist(filePath) is False:
        return
    folder = GetAbsPath(folder) + u'/'
    MakeDirectoryIfNotExist(folder)
    if IsFolderExist(folder) is False:
        return
    shutil.copy(filePath, folder)


def CopyFileToDestWithFullName(filePath, fullName):
    if IsFileExist(filePath) is False:
        return
    CheckFileName(fullName)
    shutil.copy(filePath, fullName)


def RemoveAllFileInFolder(folder):
    if IsFolderExist(folder) is False:
        return
    files = ListAllTheFilesInDir(folder)
    for fi in files:
        DeleteFile(fi)


def GetFileName(fullName):
    if fullName is None:
        return None
    return fullName[fullName.rfind(u'/')+1:]


def GetFileExt(fullName):
    if fullName is None:
        return None
    return fullName[fullName.rfind(u'.')+1:]


def RemoveAllDS_StoreFileInTheFolder(folder):
    return RemoveAllExceptionFileInTheFolder(folder, "^\.DS_Store")


def RemoveAllExceptionFileWithListInTheFolder(folder, key_List):
    if isinstance(key_List, tuple) is False:
        return False
    if isinstance(key_List, list):
        return False
    for key in key_List:
        RemoveAllExceptionFileInTheFolder(folder, key)


def RemoveAllExceptionFileInTheFolder(folder, re_Key):
    if IsFolderExist(folder) is False:
        return ()

    for root, _, files in os.walk(folder):
        for name in files:
            if re.findall(re_Key, name):
                fullPath = os.path.join(root, name)
                DeleteFile(fullPath)
                print(fullPath)


if __name__ == '__main__':
    f = u'/Volumes/Data/StockData'
    RemoveAllDS_StoreFileInTheFolder(f)

# -*- coding: utf-8 -*-
"""
生产CMake拷贝文件的脚步
@author: blan

"""

import os
import os.path
import argparse

file = object

def file_extension(path):
    strs = os.path.splitext(path)
    return  strs[1]

def findAndReplace (strRe, dir):
    global  file
    fileNames = os.listdir (dir)
    for fileName in fileNames:
        if file_extension(fileName) == '.h':
            print(fileName)
            gstr = strRe % fileName
            file.write(gstr)
            file.write('\n')

def getHomeDir ():
    return os.path.expanduser("~/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="the source header")
    parser.add_argument("--dst", help="the destination in cmake")
    args = parser.parse_args()

    file = open(getHomeDir () + "/gcmakeout.txt", 'w')

    #findAndReplace ("configure_file(${TOP_DIR}/net/ipnet/coreip/src/ipcom/include/%s ${HDR_DIR} COPYONLY)" ,
    #                "/workspace/blan/vx7-git/vxworks-7/pkgs/net/ipnet/coreip/src/ipcom/include")

    dst = "configure_file(${TOP_DIR}/%s/%s ${HDR_DIR} COPYONLY)" % (args.dst, '%s')
    findAndReplace (dst , args.src)

    file.close()
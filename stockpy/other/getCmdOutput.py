# -*- coding: utf-8 -*-
# author: Bin Lan
# email:  jetlan@live.cn

import os, re

# execute command, and return the output

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()

if __name__ == '__main__':
    cmd = "ifconfig"
    result = execCmd(cmd)
    print (result)


# -*- coding: utf-8 -*-

import json
import os.path

def loadFont():
    f = open('./Settings.json', 'w')  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    setting = json.load(f)
    family = setting['BaseSettings']['size']   #注意多重结构的读取语法
    size = setting['fontSize']   
    return family

t = loadFont()

print(t)

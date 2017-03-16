# -*- coding: utf-8 -*-

import serial
import time
import json
import ast
import udp_inout

data_back=0

def upload_packaging(json_package):
    #print "in the uploading ",json_package
    json_buff=json.loads(json_package)
    #动脉按压
    if json_buff["struct_id"]==51:
        global data_back
        #颈动脉按压
        if json_buff["can_id"]==176:
            if json_buff["data_val"][0]==1:
                data_back |=0b0010
            else:
                data_back &=0b1101
            if json_buff["data_val"][1]==1:
                data_back |=0b0010
            else:
                data_back &=0b1110
            udp_inout.udp_boardcasting(json_buff,11,data_back)
            # if json_buff["data_val"][1]==1:
            #     print "Pulse center pressed\r\n"
            # else:
            #     print "You release it\r\n"
    #电量
    if json_buff["struct_id"]==41:
        udp_inout.udp_boardcasting(json_buff,11,json_buff["data_val"])
        # print "Power level=", json_buff["data_val"]
    #充电状态
    if json_buff["struct_id"]==56:
        udp_inout.udp_boardcasting(json_buff,11,json_buff["data_val"])
        # if json_buff["data_val"]==1:
        #     print "Charging now\r"
        # else:
        #     print "Uncharged\r"
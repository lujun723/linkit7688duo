# -*- coding: utf-8 -*-

import serial
import time
import json
import ast
import udp_inout

def upload_packaging(json_package):
    #print "in the uploading ",json_package
    json_buff=json.loads(json_package)
    udp_inout.udp_boardcasting(json_package)
    if json_buff["struct_id"]==51:
        if json_buff["can_id"]==176:
            if json_buff["data_val"][1]==1:
                print "Pulse center pressed\r\n"
            else:
                print "You release it\r\n"

    if json_buff["struct_id"]==41:
        print "Power level=", json_buff["data_val"]

    if json_buff["struct_id"]==56:
        if json_buff["data_val"]==1:
            print "Charging now\r"
        else:
            print "Uncharged\r"
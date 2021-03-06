# -*- coding: utf-8 -*-

import serial
import time
import json
import ast
import json_parser

process_flag=0
s = None
config = None
sendup_package={"can_id":0, "struct_id":0, "data_lens":0, "upload_lens":0,"data_val": [0,0]}
json_package=json.dumps(sendup_package)
dict_object=None

def load_config():
    with open('data.json') as json_file:
        data = json.load(json_file)#变成python对象了：str，list，dict等
        return data

def setup():
    global s
    global config
    # open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1) # the baudrate is set to 57600 and should be the same as the one # specified in the Arduino sketch uploaded to ATmega32U4.
    s = serial.Serial("/dev/ttyS0", 57600)
    config = load_config()



def loop():
    data = ''
    read_buf=['']
    #while s.inWaiting() > 0:
    while read_buf[-1] !='}':
        read_buf.append(s.read(1))
    data =''.join(read_buf)
    json_data=data_process(data)
    json_parser.upload_packaging(json_data)

        #print data_hex[:2],data_hex[2:4],data_hex[4:6],data_hex[6:8],data_hex[-2:]

def data_process(data_buf):
    global json_package
    #print (data_buf)
    #print (data_buf)
    data_buf = ast.literal_eval(json.dumps(data_buf))
    #print "Now length is ", len(data_buf)
    
    try:
        dict_object=json.loads(data_buf)
        for item in config:
            if item["can_id"]==112:
                sendup_package["can_id"]=item["can_id"]
                for val in item["data"]:
                    if val["can_struct_id"]==dict_object["data"][0]:
                        sendup_package["struct_id"]=val["struct_id"]
                        sendup_package["data_val"]=dict_object["data"][1]
                        sendup_package["data_lens"]=val["data_lens"]
                        sendup_package["upload_lens"]=val["upload_lens"]
                        #print val["name"]
                        #print " is ", sendup_package["data_val"]
                        json_package=json.dumps(sendup_package)
                        #print json_package
                        #print '\n'
            else :
                item["can_id"]==dict_object["data"][0]
                sendup_package["can_id"]=dict_object["data"][0]
                #print "176 is get in\n"
                for val in item["data"]:
                    if val["can_struct_id"]==dict_object["data"][1]:
                        #print "can struct id ok"
                        sendup_package["struct_id"]=val["struct_id"]
                        #print type(val["data_lens"])
                        sendup_package["data_val"]=dict_object["data"][2:(2+val["data_lens"])]
                        sendup_package["data_lens"]=val["data_lens"]
                        sendup_package["upload_lens"]=val["upload_lens"]
                        #print val["name"]
                        #print " is " ,sendup_package["data_val"][1]
                        json_package=json.dumps(sendup_package)
                        #print json_package
                        #print '\n'
    
    except Exception,e:
        print Exception,":",e
        print "ERROR data_buf is ",data_buf

    return json_package   
    
    """
    print dict_object["SubBoard_ID"]
    print dict_object["data_len"]
    print dict_object["data"]
    """

if __name__ == '__main__':
    setup()
    while True:
        loop()
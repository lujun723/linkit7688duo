# -*- coding: utf-8 -*-
import json
import time
import socket,sys

cmd_lens=5
cmd_struct_id_l=78
cmd_struct_id_h=00
cmd_data=98
cmd_package_id=1000
cmd_sum=58

cmd_head = "0a11"
cmd_lens = "%02x" % cmd_lens
cmd_struct_id_l = "%02x" % cmd_struct_id_l
cmd_struct_id_h = "%02x" % cmd_struct_id_h
cmd_data = "%02x" % cmd_data
cmd_package_id_l = "%02x" % (cmd_package_id%256)
cmd_package_id_h = "%02x" % (cmd_package_id/256)
cmd_sum = "%02x" % cmd_sum
cmd_send = cmd_head+cmd_lens+cmd_struct_id_l+cmd_struct_id_h+cmd_data+cmd_package_id_l+cmd_package_id_h+cmd_sum



dest = ('<broadcast>', 18000)

sendup_package={"struct_id":0, "data_lens":0, "data_val": 0}
#json_package=json.dumps(sendup_package)#变成Json了
#package=json.loads(json_package)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)


def store(data):
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load_config():
    with open('data.json') as json_file:
        data = json.load(json_file)#变成python对象了：str，list，dict等
        return data

can_id=112
can_struct_id=83
can_data_lens=1
can_val=55

def udp_boardcasting():
    hex_cmd_send = cmd_send.decode("hex")
    s.sendto(hex_cmd_send,dest)
    print hex_cmd_send


if __name__ == "__main__":
    udp_boardcasting()
    data = load_config()
    for item in data:
        if(item["can_id"]==can_id):
            for val in item["data"]:
                if(val["can_struct_id"]==can_struct_id):
                    sendup_package["struct_id"]=val["struct_id"]
                    sendup_package["data_val"]=can_val
                    sendup_package["data_lens"]=can_data_lens
                    json_package=json.dumps(sendup_package)
                    print val["name"]
                    print json_package



                  
                
"""
    for item in data:
        for val in item["data"]:
            print val["val"]


    print type(data)
    dict_object=json.dumps(data)
    json_object=json.loads(dict_object)
    print type(dict_object)
    print type(json_object)
    print encodedjson
    data.sort(key=lambda x:x["can_id"])
    print type(data)
    print type(encodedjson)
    for item in data:
        for val in item.get("data"):
            print val.get("val")
    print encodedjson[0]["can_id"]
"""
    

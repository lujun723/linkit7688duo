# -*- coding: utf-8 -*-
import json
import time

sendup_package={"struct_id":0, "data_lens":0, "data_val": 0}
#json_package=json.dumps(sendup_package)#变成Json了
#package=json.loads(json_package)

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


if __name__ == "__main__":

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
    

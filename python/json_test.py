# -*- coding: utf-8 -*-

import json
import time

def store(data):
    with open('can_protocol.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load():
    with open('can_protocol.json') as json_file:
        data = json.load(json_file)
        return data


if __name__ == "__main__":
    data=load()
    print data.keys()
    #print data["subboard"]["can_id"]
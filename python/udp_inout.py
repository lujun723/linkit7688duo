#coding:utf-8
 
import socket,sys
 
dest = ('<broadcast>', 18000)
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
 


def udp_boardcasting(json_temp):
    s.sendto(json_temp,dest)
 
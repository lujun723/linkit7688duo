#coding:utf-8
 
import socket,sys
 
dest = ('<broadcast>', 18000)
 
cmd_package_id=0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
 


def udp_boardcasting(json_temp,cmd_kind,data):
    if cmd_kind==11:
        global cmd_package_id
        cmd_package_id+=1
        if cmd_package_id==254:
            cmd_package_id+=2
        if cmd_package_id==60000:
            cmd_package_id=0
        cmd_head = "0a11"
        cmd_lens = "%02x" % (8+json_temp["upload_lens"])
        cmd_struct_id_l = "%02x" % (json_temp["struct_id"]%256)
        cmd_struct_id_h = "%02x" % (json_temp["struct_id"]/256)
        cmd_data = "%02x" % data
        cmd_package_id_l = "%02x" % (cmd_package_id%256)
        cmd_package_id_h = "%02x" % (cmd_package_id/256)
        cmd_tail = "fffe"

        cmd_sum = "%02x" % (sum([10,17,8,json_temp["upload_lens"],(json_temp["struct_id"]%256),(json_temp["struct_id"]/256),data,(cmd_package_id%256),(cmd_package_id/256)])%256)
        cmd_send = cmd_head+cmd_lens+cmd_struct_id_l+cmd_struct_id_h+cmd_data+cmd_package_id_l+cmd_package_id_h+cmd_sum+cmd_tail
        print cmd_send
        hex_cmd_send = cmd_send.replace(' ', '').decode("hex")
        s.sendto(hex_cmd_send,dest)
 
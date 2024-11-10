#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytvh
import tvh_data
import pprint
import grid as gdt
tv = pytvh.tvh(tvh_data.host,tvh_data.port,tvh_data.username,tvh_data.password)
services = tv.get_services
channels = tv.get_grid
ultra = channels
channel_list = []
 
print(channel_list)
u_list = {}
unum = 0
for x in ultra:
  u_list[str(x['number'])] = [x['name'],x['uuid'],x['services']]
#cache_py = open('chan_list.py','w')
#cache_py.write("channels =" + pprint.pformat(u_list) + ',\n')
#cache_py.close()
print(tv.get_events_by_channel('Yankees'))
#  print(u_list['631'][2])

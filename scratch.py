#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tvh_data
import json
import requests as req
import pytvh as tvh
import pprint
import ch
import datetime
import collections
api_path = 'api/channel/list'
now = 'racknerd.kg8.me:9981/api/epg/events/grid#  ?limit=999&channel=ESPN&mode=now'
tv = tvh.tvh(tvh_data.host,tvh_data.port,tvh_data.username,tvh_data.password)
play_fubo = tv.get_play_url("ae045f8abd46dcea88bc7ce5410368dd")
#list_streams = "api/service/streams?uuid="
lineup={}
grid_lineup = tv.get_grid
#chc =ch.channels[0]['631'][0]
#print(tv.get_events_by_channel(chc))
u_list = {}
unum = 0
#for x in grid_lineup:
#  u_list[str(x['number'])] = [x['name'],x['uuid'],x['services']]
#  unum += 1
#  #print(x['name'])
my_ch = tv.ch
now = datetime.datetime.now()
p_url = lambda uuid: tv.get_play_url(uuid)
#tv_layout = open('index.html','w')
#tv_layout.write("<html>"+ "\n" + '<head> <link rel="stylesheet" href="https://unpkg.com/mvp.css"> </head>'+ "\n" + "<body><table>"+ "\n")
h = []
num = 1
x = grid_lineup
eewlist = sorted(x, key=lambda d: str(d['number']))
#      print(c['name'][0:22])

    #   if num <= 3:
        #  try:
events = tv.get_events_by_channel('TBS')
for e in events[0:3]:
    print(e)

#tv.record_event('4084132')











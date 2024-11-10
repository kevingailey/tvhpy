#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import pytvh
import tvh_data
import datetime

now = datetime.datetime.now()
tv = pytvh.tvh(tvh_data.host,tvh_data.port,tvh_data.username,tvh_data.password)
p_url = lambda uuid: tv.get_play_url(uuid)
g = tv.get_grid
chans = []
for c in g:
    table_name.append(c['name'])
table_n = sorted(table_name)

def events_to_table_row(channel_uuid):
    for c in channel_uuid:
        try:
            home_pg.write('<tr><td><a href="#" onclick="' + "changeChannel('" + p_url(c['uuid'])  + "');return false;"+ '">' + "<img width='250px' height='250px'" + 'src="' + c['icon']  + '"/></a></td>')
        except:
            home_pg.write('<tr><td><a href="#"' + 'onclick="changeChannel' + "('"+ p_url(c['uuid'])  + "')" + ';return false;"> Play ' + c['name']  + '</a></td>')
            try:
                events = tv.get_events_by_channel(c['name'])
                for e in events:
                    #home_pg.write('<td>' + e['title'] + '</td>')
            except:
                #home_pg.write('<td> no events for ' + c['name']  + '</td>')
        #home_pg.write('</tr>')
    









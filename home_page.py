#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import kcg as pytvh
import kg8_data as tvh_data
import datetime

# <script> function changeChannel(channel){document.getElementById('player').src = channel}</script>  
now = datetime.datetime.now()
tv = pytvh.tvh(tvh_data.host,tvh_data.port,tvh_data.username,tvh_data.password)
p_url = lambda uuid: tv.get_kg8_url(uuid)
g = tv.get_grid
chans = []
home_pg = open('play_pg/index.html','w')
home_pg.write('<html>' + "\n" + '<head><title> updated: ' + str(now.month) + '/' + str(now.day) +  ' </title> '+ '\n'  +' <link rel="stylesheet" href="main.css"  /> </head>' + '\n' + '<body>' + '\n')
home_pg.write("<script> function changeChannel(channel){document.getElementById('player').src = channel;}</script>" + '\n' + '\n')
home_pg.write('<div id="video_player">' + '\n' + '\n')
home_pg.write('<video id="player" controls  >' + '\n')
home_pg.write('<source src="https://www.kg8.org/ticket/stream/channel/c5b0c490680790b5f528c921b7b31dc0" type="video/mp4" autoplay="true" />' + '\n')
home_pg.write('</video>' + '\n')
home_pg.write('<div id="topButtons">' + '\n' + '\n')
home_pg.write('<button onclick="changeChannel(' + "'https://www.kg8.org/ticket/stream/channel/2b8dddc30ce4dc35970501240a1cadfe')" + '" ><h4> PPV Event </h4></button> <button onclick="changeChannel(' + "'https://plex:8675867586758675@tvh.kg8.me:443/play/ticket/stream/channel/e0462ab697c0296c2d549715000562c4')" + '" ><h4>TNT</h4></button> <button onclick="changeChannel(' + "'https://plex:8675867586758675@tvh.kg8.me:443/play/ticket/stream/channel/b507eb37a46cdaaaa2720df7ac5884df')" + '" ><h4>TBS</h4></button> <button onclick="changeChannel(' + "'https://plex:8675867586758675@tvh.kg8.me:443/play/ticket/stream/channel/332eba934d6512f146e4b13b3249cf7')" + '" ><h4>YES</h4></button></div>' + '\n')
home_pg.write('</div>' + '\n' + '\n')
home_pg.write('</div>' + '\n' + '\n')
home_pg.write('<table>' + '\n')

table_name = []
newlist = sorted(g, key=lambda d: d['name'])
for c in newlist:
    try:
        s_url = '<a href="#" ' + 'onclick="changeChannel' + "('"+ p_url(c['uuid'])  + "')" + ';return false;">'
        i_url = "<img width='150px' height='150px'" + 'src="' + c['icon']  + '"/>'
        home_pg.write('<tr><td class="logo">' + s_url + i_url  + '</a></td>' + '\n')
    except:
        s_url = '<a href="#" ' + 'onclick="changeChannel' + "('"+ p_url(c['uuid'])  + "')" + ';return false;"> <h4>Play ' + c['name']  + '</h4>'
        home_pg.write('<tr><td class="logo">' + s_url + '</a></td>' + '\n')
    try:
        events = tv.get_events_by_channel(c['name'])
        for e in events[0:15]:
            r_url = "<a href=" + str('ling to record event') + e['eventId']
            home_pg.write('<td class="epg"><h5>' + s_url + e['title'] + '</a></h5><h6>' + datetime.datetime.fromtimestamp(int(e['start'])).strftime('%H:%M  %m/%d')  + '</h6> <p> ' + s_url + e['description'][0:120]  + '</a></p></td>' + '\n')
    except:
        for i in range(3):
            home_pg.write('<td class="epg"><h3>no</h3></td><td><h3>events</h3></td><td><h3>for</h3></td><td><h3>' + c['name']  + '</h3></td>' + '\n')
    home_pg.write('</tr>' + '\n')
    print('generated guide data for ', c['name'])

home_pg.write('</table>' + '\n' + '\n')
home_pg.write('</body><foot> updated: ' +  str(now) + '</foot></html>' + '\n')
home_pg.close()
print('xxxxxx -- done -- xxxx')
for e in "DONE":
    print(e,"--------",e,"***********",e,"--------",e)












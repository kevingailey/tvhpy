#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import pytvh
import tvh_data
import datetime
import os
now = datetime.datetime.now()
tv = pytvh.tvh(tvh_data.host,tvh_data.port,tvh_data.username,tvh_data.password)
p_url = lambda uuid: tv.get_kg8_url(uuid)
for c in tv.get_grid:
    chan_url = p_url(c['uuid'])
    try:    
        play_pg = os.makedirs('play_pg/' + c['name'], exist_ok=True)
        play_pg = open('play_pg/' + c['name']  + '/index.html','w')
    except:    
        play_pg = os.makedirs('play_pg/' + str(c['number']), exist_ok=True)        
        play_pg = open('play_pg/' + str(c['number'])  + '/index.html','w')
    play_pg.write("<html>"+ "\n" + "<head><title>" + c['name'] +  '</title>  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css" type="text/css"> <link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css" media="screen" /> <link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura-dark.css" media="screen and (prefers-color-scheme: dark)" />   </head>' + "\n" + "<body>"+ "\n")
    #play_pg.write('<h1>' + c['name'] + '</h1>')
    play_pg.write('<p id="video"></style><video id="player" controls width="100%" ><source src="' + chan_url + '"')
    play_pg.write(' type="video/mp4" autoplay="true" />')
    try:
        play_pg.write('<div id="icon"><img src="' + c['icon']+ '" /> </div>')
    except KeyError:
        continue
        #play_pg.write('<div id="icon"></div>')
    try:
        events = tv.get_events_by_channel(c['name'])
        play_pg.write('<table><thead><tr><th><td>' + c['name']  + ' Upcoming Events</td></th></tr></thead><tbody>') 
        for e in events:
            show_time = datetime.datetime.fromtimestamp(int(e['start'])).strftime('%m/%d  %H:%M')
            show_name = e['title']
            play_pg.write('<tr><td>' + show_time + '</td><td>' + show_name  + '</td></tr>') 
        play_pg.write('</tbody><tfoot><tr><td>last generated: </td><td> ' + str(now.month)+ "/" + str(now.day) + " @ " + str(now.hour) + ":" + str(now.minute)  + "</td></tr></tfoot></table>") 
    except:
        play_pg.write('<div id="events"><h4>' + c['name'] + ' No events</h4></div>')
        play_pg.write(' </p></body>'+ "\n" + "<footer>" +"last generated: " + str(now.month)+ "/" + str(now.day) + " @ " + str(now.hour) + ":" + str(now.minute)  + "</footer>" + "\n" + "</html>")
    play_pg.close()
    print(c)












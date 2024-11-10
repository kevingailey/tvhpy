#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests as req
import json
import tvh_data
import pprint
class tvh:
    def __init__(self,host,port,username,password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.url = "https://" + host + ':' + port + "/api/"
        self.ch_list = {}
        self.ch
    def _url(self,path):
        return self.url + path
    def _request(self,path):
        requests =  req.get(self._url(path), auth=(self.username, self.password))
        return requests
    def _return_json(self,path):
        j = json.loads(self._request(path).text, strict=False)
        return j
    @property
    def get_connections(self):
        return self._return_json("status/connections")['entries']
    @property
    def get_subscriptions(self):
        return self._return_json("status/subscriptions")['entries']
    @property
    def get_channels(self):
        return self._return_json("channel/list?list=enabled")
    @property
    def get_epg(self):
        epg = self._return_json("epg/events/grid")['entries']
        return epg
    @property
    def get_grid(self):
        grid = self._return_json("channel/grid?limit=100000")['entries']
        return grid
    @property
    def epg_grab(self):
        path = "epggrab/internal/rerun"
        return self._return_json(path) 
    def record_event(self,event_id):
        path = "dvr/entry/create_by_event?event_id=" + event_id
        return self._return_json(path) 
    def get_events_by_number(self,channel_num):
        path = "epg/events/grid?channelNumber=" + channel_num
        return self._return_json(path)['entries'] 
    def get_events_by_channel(self,channel_name):
        path = "epg/events/grid?channel=" + channel_name
        return self._return_json(path)['entries'] 
    @property
    def get_services(self):
        return self._return_json("service/list?list=enabled")['entries'] 
    def get_kg8_url(self, uuid):
        url = "https://" + self.host +  "/ticket/stream/channel/" + uuid 
        return url
    def get_play_url(self, uuid):
        url = "https://" + self.username + ":" + self.password + "@" + self.host + ':' + self.port + "/play/ticket/stream/channel/" + uuid 
        return url
    def get_streams(self,uuid):
        path = "service/streams?uuid=" + uuid
        return self._return_json(path)
    @property
    def ch(self):
        ch_list = {}
        channels = self.get_grid
        for c in channels:
            ch_list[str(c['number'])] = [c['name'],c['uuid'],c['services']]
        self.ch_list = ch_list
        cache = open('ch.py', 'w')
        cache.write("ch_list = " + pprint.pformat(ch_list) +'\n')
        cache.close()
        return ch_list
    











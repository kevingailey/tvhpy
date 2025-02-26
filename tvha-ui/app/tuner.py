#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, Response
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# TVHeadend configuration
TVHEADEND_URL = 'https://www.kg8.org'  # Replace with your TVHeadend URL
USERNAME = 'xx'               # Replace with your TVHeadend username
PASSWORD = 'xx'               # Replace with your TVHeadend password
@app.route('/discover.json')
def discover():
    discoverData = {
        'FriendlyName': 'tvhProxy',
        'Manufacturer': 'kg8tv',
        'ModelNumber': 'kg8US',
        'FirmwareName': 'berkley_14_2',
        'TunerCount': '8',
        'FirmwareVersion': '20150826',
        'DeviceID': 'kg8tv',
        'BaseURL': 'http://www.kg8.org',
        'LineupURL': 'http://192.168.0.122:5670/lineup.json'
    }

    return jsonify(discoverData)
@app.route('/lineup.json')
def lineup():
    # Endpoint to get the list of channels from TVHeadend
    api_url = f'{TVHEADEND_URL}/api/channel/grid'

    # Make the request to TVHeadend API
    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return Response(f"Error contacting TVHeadend API: {e}", status=500)
    
    channels = data.get('entries', [])
    lineup = []

    for channel in channels:
        channel_number = channel.get('number', '')
        channel_name = channel.get('name', '')
        channel_uuid = channel.get('uuid', '')

        # Build the streaming URL for each channel
        stream_url = f"{TVHEADEND_URL}/stream/channel/{channel_uuid}?profile=pass"

        # Build the lineup entry
        lineup_entry = {
            "GuideNumber": str(channel_number),
            "GuideName": channel_name,
            "URL": stream_url
        }
        lineup.append(lineup_entry)
    
    return jsonify(lineup)

@app.route('/lineup_status.json')
def status():
    return jsonify({
        'ScanInProgress': 0,
        'ScanPossible': 0,
        'Source': "Cable",
        'SourceList': ['Cable']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5670)

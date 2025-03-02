#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, Flask, jsonify, Response, request, redirect, url_for, send_file, send_from_directory
import subprocess
import threading
import redis
import pickle
import os
import requests
from requests.auth import HTTPBasicAuth
from xml.dom import minidom
import argparse
import datetime
import xml.etree.ElementTree as ET

# Import the tvh library (ensure the tvh module is in your PYTHONPATH)
from pytvh import tvh

app = Flask(__name__)

# Directory where HLS segments and playlist will be written
OUTPUT_DIR = "hls_output"
PLAYLIST_FILE = "output.m3u8"
PLAYLIST_PATH = os.path.join(OUTPUT_DIR, PLAYLIST_FILE)

def run_ffmpeg(stream1, stream2, stream3, stream4):
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Overwrite existing files
        "-i", stream1,
        "-i", stream2,
        "-i", stream3,
        "-i", stream4,
        "-filter_complex",
        (
            "[0:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [a0];"
            "[1:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [a1];"
            "[2:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [a2];"
            "[3:v] setpts=PTS-STARTPTS, scale=iw/2:ih/2 [a3];"
            "[a0][a1] hstack=inputs=2 [top];"
            "[a2][a3] hstack=inputs=2 [bottom];"
            "[top][bottom] vstack=inputs=2"
        ),
        "-c:v", "libx264",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "3",
        "-hls_flags", "delete_segments",
        "-hls_segment_filename", os.path.join(OUTPUT_DIR, "segment_%03d.ts"),
        "-hls_base_url", "/hls/",
        PLAYLIST_PATH
    ]
    
    subprocess.run(ffmpeg_command)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get stream URLs from the form drop-down selections
        stream1 = request.form.get("stream1")
        stream2 = request.form.get("stream2")
        stream3 = request.form.get("stream3")
        stream4 = request.form.get("stream4")
        
        # Start ffmpeg in a background thread so the web request is not blocked.
        threading.Thread(target=run_ffmpeg, args=(stream1, stream2, stream3, stream4)).start()
        
        # Redirect to the page with the video player.
        return redirect(url_for("stream"))
    
    # Create a tvh client instance using your TVHeadend details
    # (Make sure to update the host, port, username, and password as needed)
    tvh_client = tvh("www.kg8.org", "9981", "plex", "8675867586758675")
    
    # Use the tvh library to get the channels.
    # The property 'ch' returns a dictionary mapping channel numbers to
    # a list: [channel name, uuid, services]
    channels = tvh_client.ch
    
    # Build options for the drop-down.
    # We will generate the streaming URL using get_play_url for each channel.
    options = []
    for ch_num, ch_data in channels.items():
        name, uuid, services = ch_data
        stream_url = tvh_client.get_play_url(uuid)
        options.append((name, stream_url))
    
    # Generate the HTML options for the <select> element.
    options_html = ""
    for name, stream_url in options:
        options_html += f'<option value="{stream_url}">{name}</option>\n'
    
    # Build the HTML form with 4 drop-downs, each populated with the stream URLs.
    html = f'''
    <html>
      <body>
        <h1>Select 4 Streams</h1>
        <form method="post">
          Stream 1: 
          <select name="stream1">
            {options_html}
          </select>
          <br>
          Stream 2: 
          <select name="stream2">
            {options_html}
          </select>
          <br>
          Stream 3: 
          <select name="stream3">
            {options_html}
          </select>
          <br>
          Stream 4: 
          <select name="stream4">
            {options_html}
          </select>
          <br>
          <input type="submit" value="Start Streaming">
        </form>
      </body>
    </html>
    '''
    return html

@app.route("/stream")
def stream():
    return '''
    <html>
      <head>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
      </head>
      <body>
        <h1>Live Stream Output</h1>
        <video id="video" width="640" height="480" controls autoplay></video>
        <script>
          var video = document.getElementById('video');
          if (Hls.isSupported()) {
            var hls = new Hls();
            hls.loadSource('/output');
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {{
              video.play();
            }});
          } else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
            video.src = '/output';
            video.addEventListener('loadedmetadata', function() {{
              video.play();
            }});
          }}
        </script>
      </body>
    </html>
    '''

@app.route("/output")
def output():
    return send_file(PLAYLIST_PATH, mimetype="application/vnd.apple.mpegurl")

@app.route("/hls/<path:filename>")
def hls_static(filename):
    return send_from_directory(OUTPUT_DIR, filename)

# (Other routes and functions remain unchanged)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5670)

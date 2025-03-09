from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

@app.route('/iptv.m3u', methods=['GET'])
def get_m3u():
    # Get parameters from request
    username = request.args.get('username')
    password = request.args.get('password')
    server_url = request.args.get('server')

    if not all([username, password, server_url]):
        return "Missing parameters. Please provide username, password, and server.", 400

    # Ensure server URL is properly formatted
    if not server_url.startswith(('http://', 'https://')):
        server_url = 'http://' + server_url

    # Remove trailing slash if present
    server_url = server_url.rstrip('/')

    # Base API URL
    api_base_url = f"{server_url}/player_api.php"

    # Get all categories and channels
    try:
        # Authenticate and get user info
        params = {
            'username': username,
            'password': password
        }

        # Get live streams
        live_params = params.copy()
        live_params['action'] = 'get_live_categories'
        live_categories_response = requests.get(api_base_url, params=live_params)
        live_categories = live_categories_response.json()

        # Get all live streams
        live_streams_params = params.copy()
        live_streams_params['action'] = 'get_live_streams'
        live_streams_response = requests.get(api_base_url, params=live_streams_params)
        live_streams = live_streams_response.json()

        # Generate M3U content
        m3u_content = "#EXTM3U\n"

        # Add live streams to M3U
        for stream in live_streams:
            stream_id = stream.get('stream_id')
            name = stream.get('name', 'Unknown')
            logo = stream.get('stream_icon', '')
            category = stream.get('category_name', 'Uncategorized')

            # Create stream URL
            stream_url = f"{server_url}/live/{username}/{password}/{stream_id}.ts"

            # Add stream to M3U
            m3u_content += f'#EXTINF:-1 tvg-id="{stream_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{name}\n'
            m3u_content += f"{stream_url}\n"

        # Return M3U file
        return Response(
            m3u_content,
            mimetype='audio/x-mpegurl',
            headers={'Content-Disposition': 'attachment; filename=iptv.m3u'}
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/vod.m3u', methods=['GET'])
def get_vod_m3u():
    # Get parameters from request
    username = request.args.get('username')
    password = request.args.get('password')
    server_url = request.args.get('server')

    if not all([username, password, server_url]):
        return "Missing parameters. Please provide username, password, and server.", 400

    # Ensure server URL is properly formatted
    if not server_url.startswith(('http://', 'https://')):
        server_url = 'http://' + server_url

    # Remove trailing slash if present
    server_url = server_url.rstrip('/')

    # Base API URL
    api_base_url = f"{server_url}/player_api.php"

    try:
        # Authenticate and get user info
        params = {
            'username': username,
            'password': password
        }

        # Get VOD categories
        vod_params = params.copy()
        vod_params['action'] = 'get_vod_categories'
        vod_categories_response = requests.get(api_base_url, params=vod_params)
        vod_categories = vod_categories_response.json()

        # Get all VOD streams
        vod_streams_params = params.copy()
        vod_streams_params['action'] = 'get_vod_streams'
        vod_streams_response = requests.get(api_base_url, params=vod_streams_params)
        vod_streams = vod_streams_response.json()

        # Generate M3U content
        m3u_content = "#EXTM3U\n"

        # Add VOD streams to M3U
        for stream in vod_streams:
            stream_id = stream.get('stream_id')
            name = stream.get('name', 'Unknown')
            logo = stream.get('stream_icon', '')
            category = stream.get('category_name', 'Uncategorized')

            # Create stream URL
            stream_url = f"{server_url}/movie/{username}/{password}/{stream_id}.mp4"

            # Add stream to M3U
            m3u_content += f'#EXTINF:-1 tvg-id="{stream_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="VOD: {category}",{name}\n'
            m3u_content += f"{stream_url}\n"

        # Return M3U file
        return Response(
            m3u_content,
            mimetype='audio/x-mpegurl',
            headers={'Content-Disposition': 'attachment; filename=vod.m3u'}
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/series.m3u', methods=['GET'])
def get_series_m3u():
    # Get parameters from request
    username = request.args.get('username')
    password = request.args.get('password')
    server_url = request.args.get('server')

    if not all([username, password, server_url]):
        return "Missing parameters. Please provide username, password, and server.", 400

    # Ensure server URL is properly formatted
    if not server_url.startswith(('http://', 'https://')):
        server_url = 'http://' + server_url

    # Remove trailing slash if present
    server_url = server_url.rstrip('/')

    # Base API URL
    api_base_url = f"{server_url}/player_api.php"

    try:
        # Authenticate and get user info
        params = {
            'username': username,
            'password': password
        }

        # Get series categories
        series_params = params.copy()
        series_params['action'] = 'get_series_categories'
        series_categories_response = requests.get(api_base_url, params=series_params)
        series_categories = series_categories_response.json()

        # Get all series
        series_params = params.copy()
        series_params['action'] = 'get_series'
        series_response = requests.get(api_base_url, params=series_params)
        series_list = series_response.json()

        # Generate M3U content
        m3u_content = "#EXTM3U\n"

        # Add series episodes to M3U
        for series in series_list:
            series_id = series.get('series_id')
            name = series.get('name', 'Unknown')
            logo = series.get('cover', '')
            category = series.get('category_name', 'Uncategorized')

            # Get series info with episodes
            series_info_params = params.copy()
            series_info_params['action'] = 'get_series_info'
            series_info_params['series_id'] = series_id
            series_info_response = requests.get(api_base_url, params=series_info_params)
            series_info = series_info_response.json()

            if 'episodes' in series_info:
                for season_num, episodes in series_info['episodes'].items():
                    for episode in episodes:
                        episode_id = episode.get('id')
                        episode_num = episode.get('episode_num', '0')
                        episode_title = episode.get('title', f'Episode {episode_num}')
                        full_title = f"{name} - S{season_num}E{episode_num} - {episode_title}"

                        # Create stream URL
                        stream_url = f"{server_url}/series/{username}/{password}/{episode_id}.mp4"

                        # Add stream to M3U
                        m3u_content += f'#EXTINF:-1 tvg-id="{episode_id}" tvg-name="{full_title}" tvg-logo="{logo}" group-title="Series: {category}",{full_title}\n'
                        m3u_content += f"{stream_url}\n"

        # Return M3U file
        return Response(
            m3u_content,
            mimetype='audio/x-mpegurl',
            headers={'Content-Disposition': 'attachment; filename=series.m3u'}
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/', methods=['GET'])
def index():
    return """
    <html>
        <head>
            <title>Xtream IPTV M3U Generator</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                form { margin: 20px 0; }
                label { display: block; margin: 10px 0 5px; }
                input[type="text"], input[type="password"] { width: 300px; padding: 8px; }
                input[type="submit"] { margin-top: 15px; padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                .note { color: #666; font-size: 0.9em; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>Xtream IPTV M3U Generator</h1>
            <form id="iptv-form">
                <label for="server">Server URL:</label>
                <input type="text" id="server" name="server" placeholder="e.g., http://example.com:1234" required>

                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <input type="submit" value="Generate Live TV M3U" onclick="generateM3U('iptv.m3u'); return false;">
                <input type="submit" value="Generate VOD M3U" onclick="generateM3U('vod.m3u'); return false;">
                <input type="submit" value="Generate Series M3U" onclick="generateM3U('series.m3u'); return false;">
            </form>

            <div class="note">
                <p>Note: Your credentials are only used to generate the M3U file and are not stored on the server.</p>
                <p>Direct M3U URLs (for media players):</p>
                <div id="direct-urls"></div>
            </div>

            <script>
                function generateM3U(endpoint) {
                    const server = document.getElementById('server').value;
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;

                    if (!server || !username || !password) {
                        alert('Please fill in all fields');
                        return;
                    }

                    const url = `/${endpoint}?server=${encodeURIComponent(server)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
                    window.location.href = url;

                    // Update direct URLs
                    updateDirectUrls();
                }

                function updateDirectUrls() {
                    const server = document.getElementById('server').value;
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;

                    if (!server || !username || !password) {
                        return;
                    }

                    const baseUrl = window.location.origin;
                    const urlsDiv = document.getElementById('direct-urls');

                    const liveUrl = `${baseUrl}/iptv.m3u?server=${encodeURIComponent(server)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
                    const vodUrl = `${baseUrl}/vod.m3u?server=${encodeURIComponent(server)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
                    const seriesUrl = `${baseUrl}/series.m3u?server=${encodeURIComponent(server)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;

                    urlsDiv.innerHTML = `
                        <p><strong>Live TV:</strong> ${liveUrl}</p>
                        <p><strong>VOD:</strong> ${vodUrl}</p>
                        <p><strong>Series:</strong> ${seriesUrl}</p>
                    `;
                }
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

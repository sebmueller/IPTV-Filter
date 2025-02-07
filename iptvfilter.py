import requests
from flask import Flask, request, Response
from urllib.parse import urljoin, urlencode
import json

app = Flask(__name__)

TARGET_URL = "TARGET_URL:8080"
NEW_USERNAME = "NEW_USERNAME"
NEW_PASSWORD = "NEW_PASSWORD"

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    # Query-Parameter ersetzen
    query_params = request.args.to_dict()
    if 'username' in query_params:
        query_params['username'] = NEW_USERNAME
    if 'password' in query_params:
        query_params['password'] = NEW_PASSWORD
    
    target_url = f"{TARGET_URL}/{path}?{urlencode(query_params)}"
    headers = {key: value for key, value in request.headers.items()}

    try:
        if path == "player_api.php" and query_params.get('username') == NEW_USERNAME and query_params.get('password') == NEW_PASSWORD:
            action = query_params.get('action')
            resp = requests.get(target_url, headers=headers)
            data = resp.json()

            # Filterung und Anpassung basierend auf der Aktion
            if action == 'get_live_streams':
                filtered_data = [entry for entry in data if 'name' in entry and ("DE:" in entry['name'] or "XXX:" in entry['name'])]
            elif action == 'get_vod_streams':
                filtered_data = [entry for entry in data if 'name' in entry and ("DE-" in entry['name'] or "XXX-" in entry['name'])]
            elif action == 'get_series':
                filtered_data = [entry for entry in data if 'name' in entry and "(DE-)" in entry['name']]
            elif action == 'get_live_categories':
                filtered_data = [entry for entry in data if 'category_name' in entry and ("DE " in entry['category_name'] or "FOR ADULTS" in entry['category_name'])]
            elif action == 'get_vod_categories':
                filtered_data = [entry for entry in data if 'category_name' in entry and ("V|DE" in entry['category_name'] or "XXX" in entry['category_name'])]
            elif action == 'get_series_categories':
                filtered_data = [entry for entry in data if 'category_name' in entry and "S|DE" in entry['category_name']]
            else:
                filtered_data = data
                # Wenn keine Aktion angegeben ist
                if action is None:
                    if 'user_info' in data:
                        data['user_info']['username'] = NEW_USERNAME
                        data['user_info']['password'] = NEW_PASSWORD

            # Gefilterte Daten als JSON
            modified_content = json.dumps(filtered_data)

            print(f"Forwarding special request to: {target_url}")
            response = Response(modified_content, resp.status_code, resp.raw.headers.items())
        else:
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False
            )
            response = Response(resp.content, resp.status_code, resp.raw.headers.items())

        print(f"Forwarding request to: {target_url}")
        return response
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

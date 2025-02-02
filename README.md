Small Python Tool.

Opens a port and forwards all communication to an IPTV provider

Filters out all unwanted channels.

Usage:

Set credentials for IPTV

TARGET_URL = "TARGET_URL:8080"
NEW_USERNAME = "NEW_USERNAME"
NEW_PASSWORD = "NEW_PASSWORD"


add Filters, you want to allow to pass. all other channels will be blocked.


            if action == 'get_live_streams':
                filtered_data = [entry for entry in data if 'name' in entry and ("DE:" in entry['name'] or "XXX:" in entry['name'])]
            elif action == 'get_vod_streams':
                filtered_data = [entry for entry in data if 'name' in entry and ("DE-" in entry['name'] or "XXX-" in entry['name'])]
            elif action == 'get_series':
                filtered_data = [entry for entry in data if 'name' in entry and "(DE-)" in entry['name']]


Nice result is a clean channel list without 1000 of unwanted channels.


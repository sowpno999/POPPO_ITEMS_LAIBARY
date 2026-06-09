#This Code Was Made By POPPO OFFICIAL 
#This Code Was Made By POPPO OFFICIAL
#This Code Was Made By POPPO OFFICIAL
#This Code Was Made By POPPO OFFICIAL
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import json
import os
from time import sleep
import base64

app = Flask(__name__)
CORS(app)

ENCRYPTED_API = "aHR0cHM6Ly9mcmVlLWZpcmUtaWNvbi1hcGktYXlhbi1sZWdlbmQudmVyY2VsLmFwcC9pbmZvP2l0ZW1faWQ9"
ENCRYPTED_URL = "aHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL1NoYWhHQ3JlYXRvci9pY29uQG1haW4vUE5HLw=="
ENCRYPTED_USER_AGENT = "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2"

def decrypt_string(encoded_string):
    try:
        decoded = base64.b64decode(encoded_string).decode('utf-8')
        return decoded
    except:
        return ""

def get_info_api_url():
    return decrypt_string(ENCRYPTED_API)

def get_cdn_url():
    return decrypt_string(ENCRYPTED_URL)

def get_user_agent():
    return decrypt_string(ENCRYPTED_USER_AGENT)

DATABASE_FILE = 'items_database.json'
items_database = {}

def load_database_from_json():
    global items_database
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                items_database = json.load(f)
            print(f"Database loaded: {len(items_database)} items")
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            return False
    else:
        print(f"Database file not found")
        return False

def save_database_to_json():
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(items_database, f, indent=2, ensure_ascii=False)
        print(f"Database saved")
        return True
    except Exception as e:
        print(f"Error saving database: {e}")
        return False

def fetch_from_api(item_id):
    try:
        base_info_url = get_info_api_url()
        info_url = f"{base_info_url}{item_id}"
        cdn_base = get_cdn_url()
        image_url = f"{cdn_base}{item_id}.png"
        user_agent = get_user_agent()
        
        print(f"Fetching: {item_id}")
        
        response = requests.get(info_url, timeout=10, headers={
            'User-Agent': user_agent
        })
        
        if response.status_code == 200:
            data = response.json()
            
            return {
                'success': True,
                'item_id': item_id,
                'name': data.get('name', f'Item {item_id}'),
                'item_type': data.get('type', data.get('itemType', 'Unknown')),
                'rarity': data.get('Rare', data.get('rarity', 'Common')),
                'collection_type': data.get('collectionType', 'N/A'),
                'is_unique': data.get('isUnique', False),
                'description': data.get('description', 'No description available'),
                'icon': data.get('icon', ''),
                'image_url': image_url
            }
        else:
            return {
                'success': True,
                'item_id': item_id,
                'name': f'Item {item_id}',
                'item_type': 'Emote',
                'rarity': 'Purple',
                'collection_type': 'Collection',
                'is_unique': False,
                'description': 'Free Fire Item',
                'icon': '',
                'image_url': image_url
            }
    
    except Exception as e:
        print(f"API Error for {item_id}: {e}")
        cdn_base = get_cdn_url()
        return {
            'success': True,
            'item_id': item_id,
            'name': f'Item {item_id}',
            'item_type': 'Emote',
            'rarity': 'Purple',
            'collection_type': 'Collection',
            'is_unique': False,
            'description': 'Free Fire Item',
            'icon': '',
            'image_url': f"{cdn_base}{item_id}.png"
        }

DEFAULT_ITEMS = [
    909052002, 909052011, 909052012, 909052004, 909052007, 909052009, 909052003,
    909051001, 909052005, 909052001, 909042008, 909041005, 909033001, 909038010,
    909038012, 909045001, 909049010, 909051003, 909000063, 909037011, 909049012,
    909000002, 909051014, 909050009, 909051013, 909051010, 909051004, 909051002,
    909048015, 909051001, 909044015, 909041008, 909049003, 909050008, 909049001,
    909041013, 909050014, 909050015, 909050002, 909000034, 909000012, 909000020,
    909000014, 909000010, 909038004, 909040004, 909041012, 909041003, 909000084,
    909000142, 909000086, 909000087, 909000088, 909000095, 909000125, 909000129,
    909000130, 909000135, 909000143, 909034003, 909033005, 909000034, 909000039,
    909000055, 909000064, 909000071, 909000074, 909000080, 909034009, 909035006,
    909034014, 909035001, 909035002, 909035003, 909035010, 909036001, 909036002,
    909036004, 909036008, 909036010, 909037003, 909037004, 909037009, 909038001,
    909037002, 909037006, 909037008, 909037010, 909037011, 909038003, 909038006,
    909038008, 909038011, 909039004, 909039006, 909040001, 909052012, 909040004,
    909040005, 909052002, 909000081, 909000075, 909000085, 909000134, 909000098,
    909035007, 909051012, 909000141, 909034008, 909051015, 909041002, 909039004,
    909042008, 909051014, 909039012, 909040010, 909035010, 909041005, 909051003,
    909034001, 909053002, 909048016, 909053003, 909053004, 909047015, 909053005,
    909046015, 909053006, 909042006, 909042002, 909040009, 909053007, 909053008,
    909053009, 909036010, 909053003, 909000089, 909000096, 909000077, 909053011, 909000054
]

UNIQUE_ITEMS = list(set(DEFAULT_ITEMS))

def load_or_fetch_items():
    global items_database
    
    if load_database_from_json():
        print("="*50)
        print("DATABASE LOADED FROM JSON FILE")
        print("="*50)
        print(f"Total items: {len(items_database)}")
        print("="*50 + "\n")
        return
    
    print("="*50)
    print("NO DATABASE FOUND. FETCHING FROM API...")
    print("="*50)
    print(f"Total items to fetch: {len(UNIQUE_ITEMS)}")
    print("="*50 + "\n")
    
    for idx, item_id in enumerate(UNIQUE_ITEMS, 1):
        item_id_str = str(item_id)
        
        if item_id_str not in items_database:
            print(f"[{idx}/{len(UNIQUE_ITEMS)}] Fetching: {item_id}", end=" ")
            item_data = fetch_from_api(item_id)
            
            if item_data['success']:
                items_database[item_id_str] = item_data
                print(f"OK - {item_data['name'][:30]}")
            else:
                print(f"FAILED")
            
            sleep(0.1)
    
    save_database_to_json()
    
    print("\n" + "="*50)
    print("DATABASE CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"Total items saved: {len(items_database)}")
    print(f"Database file: {DATABASE_FILE}")
    print("="*50 + "\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_all_items():
    return jsonify(list(items_database.values()))

@app.route('/api/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item_id_str = str(item_id)
    
    if item_id_str in items_database:
        return jsonify(items_database[item_id_str])
    
    item_data = fetch_from_api(item_id)
    
    if item_data['success']:
        items_database[item_id_str] = item_data
        save_database_to_json()
        return jsonify(item_data)
    
    return jsonify({'success': False, 'error': 'Item not found'}), 404

@app.route('/api/add', methods=['POST'])
def add_item():
    data = request.get_json()
    item_id = str(data.get('item_id'))
    
    if not item_id:
        return jsonify({'success': False, 'error': 'Item ID required'}), 400
    
    if item_id in items_database:
        return jsonify({'success': False, 'error': 'Item already exists'}), 409
    
    item_data = fetch_from_api(int(item_id))
    
    if item_data['success']:
        items_database[item_id] = item_data
        save_database_to_json()
        return jsonify({'success': True, 'item': item_data})
    
    return jsonify({'success': False, 'error': 'Invalid item ID'}), 404

@app.route('/api/remove/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    item_id_str = str(item_id)
    
    if item_id_str in items_database:
        del items_database[item_id_str]
        save_database_to_json()
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Item not found'}), 404

@app.route('/api/database/info', methods=['GET'])
def database_info():
    return jsonify({
        'total_items': len(items_database),
        'database_file': DATABASE_FILE,
        'file_exists': os.path.exists(DATABASE_FILE)
    })

print("\n" + "="*50)
print("POPPO ITEMS LIBRARY BACKEND")
print("="*50)

load_or_fetch_items()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("SERVER STARTING")
    print("="*50)
    print(f"Server URL: http://localhost:5000")
    print(f"Database: {DATABASE_FILE}")
    print(f"Total Items Ready: {len(items_database)}")
    print("="*50 + "\n")
    print("Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
#This Code Was Made By POPPO OFFICIAL
#This Code Was Made By POPPO OFFICIAL
#This Code Was Made By POPPO OFFICIAL
#This Code Was Made By POPPO OFFICIAL
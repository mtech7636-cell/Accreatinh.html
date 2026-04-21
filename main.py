import os, json, requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEYS = {"CPM1": "AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA", "CPM2": "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ"}
URLS = {"CPM1": "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4", "CPM2": "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17_AppI"}

@app.route('/')
def home(): return render_template('index.html')

@app.route('/unlock', methods=['POST'])
def unlock():
    data = request.json
    email, pwd, game = data['email'], data['password'], data['game']
    
    auth = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEYS[game]}", json={'email': email, 'password': pwd, 'returnSecureToken': True}).json()
    
    if 'idToken' in auth:
        # All-in-one Data Payload
        payload = {'data': json.dumps({
            'RatingData': {'money': 50000000, 'coin': 50000, 'race_win': 5000, 'time': 10000000000}, 
            'LocalData': {'money': 50000000, 'coin': 50000, 'owned_cars': list(range(1, 185)), 'unlock_all_cars': True}
        })}
        requests.post(URLS[game], headers={'Authorization': f"Bearer {auth['idToken']}", 'Content-Type': 'application/json'}, json=payload)
        return jsonify({"status": "success", "message": "👑 SUCCESS! RESTART GAME."})
    return jsonify({"status": "error", "message": "INVALID LOGIN!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

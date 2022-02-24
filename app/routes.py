from app import app
from flask import render_template
import requests
import json

@app.route('/')
def index():
    return 'This is the endpoint for icon-depot microservice.'

@app.route('/icon-list')
def get_icon_list():
    r = requests.get('https://fonts.google.com/metadata/icons')
    rtext = r.text[5:]
    with open('app/static/icon_list.json', 'w') as json_file:
        json_file.write(rtext)
        json_file.close
    with open('app/static/icon_list.json') as json_file:
        data = json.load(json_file)
        icons = data['icons']
        icon_list = {'icons': []}
        for icon in icons:
            entry = {
                'name' : icon['name'],
                'categories' : icon['categories']
            }
            icon_list['icons'].append(entry)
    return icon_list
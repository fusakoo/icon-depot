from app import app
from flask import render_template
import requests
import json

@app.route('/')
def index():
    return 'This is the endpoint for icon-depot microservice.'

@app.route('/icons-available')
def get_icon_available():
    r = requests.get('https://fonts.google.com/metadata/icons')
    rtext = r.text[5:]
    with open('app/static/icon_list.json', 'w') as json_file:
        json_file.write(rtext)
        json_file.close
    with open('app/static/icon_list.json') as json_file:
        data = json.load(json_file)
        icons = data['icons']
        icon_dict = {'icons': []}
        for icon in icons:
            entry = {
                'name' : icon['name'],
                'categories' : icon['categories']
            }
            icon_dict['icons'].append(entry)
    return icon_dict

@app.route('/icon/<icon_name>')
def get_icon(icon_name):
    icon_dict = get_icon_available()
    icons = icon_dict['icons']
    for icon in icons:
        name = icon.get('name')
        if name == icon_name:
            output = {
                'html' : '<span class="material-icons">{}</span>'.format(icon_name)
            }
            return output

@app.route('/icons', methods=['POST'])
def get_icons_json():
    return 'Json page'
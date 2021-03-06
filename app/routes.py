import flask
from app import app
from flask import render_template, request
import requests
import json

@app.route('/')
def index():
    '''
    Index page
    '''
    return render_template('index.html')

@app.route('/icons-available')
def get_icons_available():
    '''
    Return a list of icons available by checking the materials icon metadata
    '''
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
                'tags' : icon['tags'],
                'categories' : icon['categories']
            }
            icon_dict['icons'].append(entry)
    response = flask.jsonify(icon_dict)
    return response

@app.route('/categories-available')
def get_categories():
    '''
    Return a list of categories available by checking the metadata
    '''
    icon_dict = json.loads(get_icons_available().get_data())
    icons = icon_dict['icons']
    output = []
    for icon in icons:
        categories = icon['categories']
        for category in categories:
            if category not in output:
                output.append(category)
    print(output)
    response = flask.jsonify(output)
    return response

@app.route('/tags-available')
def get_tags():
    '''
    Return a list of categories available by checking the metadata
    '''
    icon_dict = json.loads(get_icons_available().get_data())
    icons = icon_dict['icons']
    output = []
    for icon in icons:
        tags = icon['tags']
        for tag in tags:
            if tag not in output:
                output.append(tag)
    print(output)
    response = flask.jsonify(output)
    return response

def check_if_available(icon_name):
    '''
    Checks if the name exists in the available list of icons
    '''
    icon_dict = json.loads(get_icons_available().get_data())
    icons = icon_dict['icons']
    for icon in icons:
        name = icon.get('name')
        if name == icon_name:
            return True
    return False

@app.route('/icon/<icon_name>')
def get_icon(icon_name):
    '''
    Checks available icons & returns a dict containing an html for the icon
    '''
    if check_if_available(icon_name):
        output = {
            'html' : '<span class=\"material-icons\">{}</span>'.format(icon_name)
        }
        response = flask.jsonify(output)
        return response

@app.route('/icons', methods=['POST'])
def icons_json():
    '''
    Checks available icons & returns a dict containing list of html for the icons
    '''
    response = flask.Response()
    response.headers["Access-Control-Allow-Origin"] = "*"

    request_data = request.get_json()
    icon_names = request_data['icon_list']
    output = { 'html': [] }
    for icon_name in icon_names:
        if check_if_available(icon_name):
            icon_html = '<span class=\"material-icons\">{}</span>'.format(icon_name)
            output['html'].append(icon_html)
    response = flask.jsonify(output)
    return response

@app.route('/icons-value', methods=['POST'])
def icons_values_json():
    '''
    Checks available icons & returns a dict containing list of html for the icons
    '''
    response = flask.Response()
    response.headers["Access-Control-Allow-Origin"] = "*"

    request_data = request.get_json()
    icon_names = request_data['icon_list']
    output = { 'html': [] }
    for icon_name in icon_names:
        if check_if_available(icon_name):
            icon_html = '<span class="material-icons" value="{}">{}</span>'.format(icon_name, icon_name)
            output['html'].append(icon_html)
    response = flask.jsonify(output)
    return response
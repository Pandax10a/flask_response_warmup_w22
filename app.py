from re import A
from flask import Flask, make_response, request
import json
import apihelper as a
import dbhelpers as dh

app = Flask(__name__)

@app.post('/api/hero')

# adding a hero by passing 3 argument(name, description, img_url)
def add_new_hero():
    name = request.json.get('name')
    description = request.json.get('description')
    img_url = request.json.get('img_url')

    # checking to see if each value that is entered by client is a str, if not it stops there
    valid_check = a.check_endpoint_info(request.json, ['name', 'description', 'img_url'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL add_new_hero(?,?,?)', [name, description, img_url])
    if(type(result) == list):
        # using make response to make it easier for me to debug
        # http response 200 = success, 400 = connection problem
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.get('/api/hero')

def all_hero():
    result = dh.run_statement('CALL all_hero()')
    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.post('/api/villain')

# adding a villain by passing 3 argument(name, description, img_url)
def add_new_villain():
    name = request.json.get('name')
    description = request.json.get('description')
    img_url = request.json.get('img_url')
    hero_id = request.json.get('hero_id')

    # checking to see if each value that is entered by client is a str, if not it stops there
    valid_check = a.check_endpoint_info(request.json, ['name', 'description', 'img_url', 'hero_id'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL add_new_villain(?,?,?)', [name, description, img_url, hero_id])
    if(type(result) == list):
        # using make response to make it easier for me to debug
        # http response 200 = success, 400 = connection problem
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.get('/api/villain')
def show_all_villain_related_to_hero():
    hero_id = request.args.get('hero_id')

    valid_check = a.check_endpoint_info(request.args, ['hero_id'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL show_all_villain_related_hero(?)', [hero_id])
    if(type(result) == list):
      
        # http response 200 = success, 400 = connection problem
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)


app.run(debug=True)

from bottle import run, post, request
from functions import *

@post('/webfest')
def read_json():

    name = request.json['name']

    if name in allowed_functions:

        return allowed_functions[name]()

    else:

        return error()


run(host='localhost', port=8080, debug=True)

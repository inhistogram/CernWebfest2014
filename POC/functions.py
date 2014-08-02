def hello_world():
    return {'status':'OK', 'response':'Hello world!'}

def duck_you():
    return {'status':'OK', 'response':'Duck you too!'}

def error():
    return {'status':'Not OK', 'response':'A problem has been found.'}

allowed_functions = {'hello_world' : hello_world, 'duck_you' : duck_you}

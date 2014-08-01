from bottle import run, post, request

@post('/webfest')
def read_json():

    if (request.json['name'] == 'hello_world'):
        print "Hello World!"

        #Automagic conversion from dict to JSON
        return {'status':'OK', 'response':'Hello world!'}

    else:
        print "Not a nice thing to say .-."

        #Automagic conversion from dict to JSON
        return {'status':'Not OK', 'response':'Duck you too!'}


run(host='localhost', port=8080, debug=True)

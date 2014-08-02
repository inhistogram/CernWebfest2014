import urllib2, json

#Create JSON
jdata1 = json.dumps({"name":"hello_world"})
jdata2 = json.dumps({"name":"duck_you"})
jdata3 = json.dumps({"name":"random_string"})

#Create request
req1 = urllib2.Request("http://localhost:8080/webfest", jdata1, {'Content-Type': 'application/json'})
req2 = urllib2.Request("http://localhost:8080/webfest", jdata2, {'Content-Type': 'application/json'})
req3 = urllib2.Request("http://localhost:8080/webfest", jdata3, {'Content-Type': 'application/json'})

#Send request
response1 = urllib2.urlopen(req1)
response2 = urllib2.urlopen(req2)
response3 = urllib2.urlopen(req3)

#Visualice JSON
print json.load(response1)
print json.load(response2)
print json.load(response3)


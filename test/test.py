import requests
r = requests.post("http://p3rl4.ddns.net:5000", data={'foo': 'soy raspberry pi 1'})
# And done.
print(r.text) # displays the result body.

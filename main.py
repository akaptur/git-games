from flask import Flask, render_template, request, redirect, url_for
from flask_sockets import Sockets
import docker
import requests # this is silly
import pdb
import os
import json

app = Flask(__name__)
sockets = Sockets(app)

create = json.dumps({
         "Hostname":"",
         "User":"",
         "Memory":0,
         "MemorySwap":0,
         "AttachStdin":False,
         "AttachStdout":True,
         "AttachStderr":True,
         "PortSpecs":None,
         "Tty":False,
         "OpenStdin":True,
         "StdinOnce":False,
         "Env":None,
         "Cmd":[
                 "date"
         ],
         "Image":"ubuntu",
         "Volumes":{
                 "/tmp": {}
         },
         "WorkingDir":"",
         "DisableNetwork": False,
         "ExposedPorts":{
                 "22/tcp": {}
         }
    })

dock = docker.Client(base_url=os.environ["DOCKER_HOST"])
base_url = "http" + os.environ["DOCKER_HOST"][3:] # base URL for daemon

@app.route('/login', methods=['GET','POST'])
def login():
    pass

@app.route('/admin', methods=["GET"])
def admin():
    """ Show a list of containers."""
    r = requests.get(base_url + '/containers/json', params={'all': 1})
    app.containers = r.json()
    return str([c[u"Names"] for c in app.containers])

@app.route('/', methods=['GET'])
def home():
    """ Spin up a new container and redirect to level 1."""
    r = requests.post(base_url + '/containers/create', data=create)
    # hardcode to go to level 1 for now
    return redirect(url_for('levels', level=1))

@sockets.route('/echo')
def echo(sock):
    message = sock.receive()
    print message
    sock.send(message[::-1])

@sockets.route('/levels/<level>', methods=['GET', 'POST'])
def levels(level, sock):
    if request.method == 'GET':

        return render_template('level.html')
    else:
        # send command to docker and redirect
        # attach to container
        container_id = app.containers[0][u'Id']
        r = requests.post(base_url + '/containers/%s/attach' % container_id, params={"stdin":True, "stdout": True})
        # pdb.set_trace()
        command = request.form['command']


if __name__ == '__main__':
    app.run(debug=True)

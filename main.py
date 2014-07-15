from flask import Flask, render_template, request, redirect, url_for
import docker
import requests # this is silly
import pdb
import os
import json

app = Flask(__name__)

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
         "OpenStdin":False,
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

@app.route('/levels/<level>', methods=['GET', 'POST'])
def levels(level):
    if request.method == 'GET':
        return render_template('level.html')
    else:
        pass
        # send command to docker and redirect
        # command = request.form['command']


if __name__ == '__main__':
    app.run(debug=True)

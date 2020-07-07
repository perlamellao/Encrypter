from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response
import requests
from urllib.request import urlopen
import os
import static.files.running as running
from pyDes import des
from pyfladesk import init_gui
import subprocess
import hashlib
import time
from random import randint
import subprocess
import sys


# Crear instancia Flask
app = Flask(__name__)

# VARIABLES GLOBALES


global init_dir
global act
global passhsh
global debian

debian="/static/css/img/debian.png"
passhsh = "f5a617102abb078c922452642ea57f3b"
init_dir = os.path.dirname(os.path.abspath(__file__))
# RUTAS DE LA APLICACIÓN WEBVIEW


@app.route('/')
def index():
    return render_template('init.html')


@app.route('/home')
def home():
    checkonline()
    return render_template('mainv1.html', activos=activos, on_off=on_off, inet_connection=inet_connection)


@app.route('/raspissh')
def raspissh():
    return render_template('ssh1.html')


@app.route('/ssh')
def ssh():
    checkonline()
    return render_template('ssh.html', on_off_ssh=on_off_ssh, inet_connection=inet_connection, debian=debian)


@app.route('/archivoe')
def archivoe():
    checkonline()
    return render_template('archivoe.html', on_off=on_off, inet_connection=inet_connection)


@app.route('/encriptar', methods=['POST', 'GET'])
def encriptar():
    print("ENCRIPTANDO.......")
    encriptaFiles(str(passhsh))
    return render_template('endencrypt.html')


@app.route('/desencriptar', methods=['POST', 'GET'])
def desencriptar():
    print("DESENCRIPTANDO.......")
    desencriptaFiles(str(passhsh))
    return render_template('enddecrypt.html')

@app.route('/main')
def log():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        passwd_tmp = request.form['passwd']
        hsh_tmp = hashlib.md5(passwd_tmp.encode()).hexdigest()
        if passhsh == hsh_tmp:
            return render_template('mainv0.html', activos=activos, on_off=on_off, inet_connection=inet_connection)
        else:
            return render_template('errorpopup.html')



@app.route('/sendssh', methods=['POST', 'GET'])
def sendssh():
    command = request.form['command']
    requests.post("http://p3rl4.me:1324/sendssh", data={'command': command})
    time.sleep(3)
    sshobj = urlopen('http://p3rl4.me:1324/sendssh')
    output = sshobj.read().decode('utf-8')
    return render_template('ssh1.html', ssh_output=output)


@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(randint(0, 1))

    return Response(generate(), mimetype='text/event-stream')


@app.route('/logout')
def logout():
    return render_template('logout.html')

# FUNCIONES
def checkonline():
    global activos
    global on_off
    global on_off_ssh
    global inet_connection
    global debian
    try:
        activos=running.check()
        if activos > 0:
            debian="/static/css/img/debian.png"
            on_off_ssh=''
        else:
            debian="/static/css/img/debian_off.png"
            on_off_ssh='disconnected'
        inet_connection='Modo Online'

        on_off=''
    except:
        activos=0
        on_off='disconnected'
        debian="/static/css/img/debian.png"
        inet_connection='Modo Offline'


def encriptaFiles(user_pass):
    os.chdir(filesdir)
    for filen in os.listdir(filesdir):
        f = open(filen, 'rb+')
        d = f.read()
        f.close()
        key = des(user_pass)
        d = key.encrypt(d, ' ')
        f = open(filen, 'wb+')
        f.write(d)
        f.close()
    os.chdir(init_dir)
    return True


def desencriptaFiles(user_pass):
    os.chdir(filesdir)
    for filen in os.listdir(filesdir):
        f = open(filen, 'rb+')
        d = f.read()
        f.close()
        key = des(user_pass)
        d = key.decrypt(d, ' ')
        f = open(filen, 'wb+')
        f.write(d)
        f.close()
    os.chdir(init_dir)
    return True

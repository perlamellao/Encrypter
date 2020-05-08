from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response
import static.files.running as running
import os
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


global passhsh
global filesdir
global init_dir
global PiHost1
global COMMAND
global act
activos=running.check()
PiHost1 = "pi@192.168.1.9"
COMMAND = ""
init_dir = os.path.dirname(os.path.abspath(__file__))
# RUTAS DE LA APLICACIÓN WEBVIEW


@app.route('/')
def index():
    return render_template('init.html')


@app.route('/home')
def home():
    activos=running.check()
    return render_template('mainv1.html', activos=activos)

@app.route('/raspissh')
def raspissh():
    return render_template('ssh1.html')

@app.route('/ssh')
def ssh():
    return render_template('ssh.html')


@app.route('/archivoe')
def archivoe():
    return render_template('archivoe.html')


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
def main():
    res = subprocess.run(['ls', '/volumes'], stdout=subprocess.PIPE)
    resd = res.stdout.decode('UTF-8')
    if resd[0] == "6":
        return render_template('connected.html')
    else:
        return render_template('error.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    global passhsh
    global filesdir
    res = subprocess.run(['ls', '/volumes'], stdout=subprocess.PIPE)
    resd = res.stdout.decode('UTF-8')
    if request.method == 'POST':
        passwd = request.form['passwd']
        passhsh = int(hashlib.sha256(passwd.encode('utf-8')).hexdigest(), 16) % 10**8
        if str(passhsh) == str(resd.splitlines()[0]):
            filesdir = "/Volumes/"+str(passhsh)+"/files"
            return render_template('mainv0.html', activos=activos)
        else:
            return render_template('errorpopup.html')

@app.route('/sendssh', methods=['POST', 'GET'])
def sendssh():
    global PiHost1
    global COMMAND
    global result
    COMMAND = request.form['command']
    try:
        with subprocess.Popen(["ssh", "%s" % PiHost1, COMMAND], shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as ssh:
            global result
            result = ssh.stdout.readlines()
        stringlist=[x.decode('utf-8') for x in result]
        fullStr = ''.join(stringlist)
    except:
        fullStr = "Ha ocurrido un error"
    return render_template('ssh1.html', ssh_output=fullStr)


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


# INICIAR GUI

if __name__ == '__main__':
    init_gui(app, window_title="PerlaVault", height=489, width=881)

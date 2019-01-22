# -*- coding: utf-8 -*-

from time import sleep
from flask import Flask, render_template
from wires_acc_file import wires_acc_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    with open('wires_acc.log') as f:
        lines = f.readlines()
        lines.reverse()
    return app.response_class(lines[0:50], mimetype='text/plain')

@app.route('/latest')
def latest():
    acc_file = wires_acc_file('C:\\Users\\hb9uf.UF-Pilatus\\Documents\\WIRESXA\\AccHistory\\WiresAccess.log')
    calls = sorted(acc_file.calls, key=lambda i: i.get_timestamp_epoch(),reverse=True)
    return render_template('latest.html', calls = calls)

app.run(host='0.0.0.0')

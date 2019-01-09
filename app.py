#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

x = 3
y = 2

@app.route('/')
def index():
    return render_template('app.html', x=x, y=y)


@app.route('/setPosition')
def setPosition():
    global x, y
    x = request.args.get('x')
    y = request.args.get('y')
    print(request.args)
    return ''


@app.route('/getPosition')
def getPosition():
    return '{"x": %s, "y": %s}' % (x, y)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

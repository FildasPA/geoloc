#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
     return render_template('app.html', bottom='133px', left='126px')

if __name__ == '__main__':
    app.run(debug=True)

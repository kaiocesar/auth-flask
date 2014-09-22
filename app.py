#!/usr/bin/env python
# coding: utf-8 

from flask import Flask

app = Flask('auth_flask', static_url_path='')
app.config.from_object('settings')
app.config['SECRET_KEY'] = "a7506f01e276a8e3283084aed62c7596" 

import views


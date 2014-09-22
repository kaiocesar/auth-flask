#!/usr/bin/env python
# coding: utf-8 

from flask import Flask
from blueprints.articles import articles_blueprint

def create_app(config_filename=None):
	app = Flask('auth_flask', static_url_path='')
	app.config['SECRET_KEY'] = "a7506f01e276a8e3283084aed62c7596" 

	if config_filename:
		app.config.from_pyfile(config_filename)
		
	app.register_blueprint(articles_blueprint)

	return app





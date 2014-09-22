#!/usr/bin/env python
# coding: utf-8 

import os
from datetime import datetime
from werkzeug import secure_filename
from flask import request, current_app, send_from_directory, render_template, url_for 

from db import Articles
from app import app

@app.route("/media/<path:filename>")
def media(filename):
	return send_from_directory(current_app.config.get("MEDIA_ROOT"), filename)

@app.route("/")
def index():
	articles = [dict(article) for article in Articles.all()]
	return render_template("default/index.html", articles= articles)

@app.route("/about")
def about():
	return render_template("default/about.html")

@app.route("/contact")
def contact():
	return render_template("default/contact.html")

@app.route("/article/<int:article_id>")
def article_details(article_id):
	article = Articles.find_one(id=article_id)
	return render_template("default/article-details.html", article=article)

@app.route("/articles", methods=["GET","POST"])
def articles():
	return "listing all articles"

@app.route("/search")
def search():
	q = request.args.get("question")
	results = Articles.query('SELECT * FROM articles WHERE title like "%%s%" ' % (q))
	questions = [dic(article) for article in results]
	return render_template("default/search.html", questions= questions)




"""
==========================================
	Authentication routes
==========================================
"""
@app.route("/admin")
def admin():
	return render_template("admin/default/index.html")

@app.route("/admin/articles", methods=["GET","POST"])
def articlesAdmin():
	lista = [dict(article) for article in Articles.all()]
	return render_template("admin/articles/index.html", articles = lista )

@app.route("/admin/article-add", methods=["GET","POST"])
def addArticle():
	flashMessage = None

	if request.method == "POST":
		datas = request.form.to_dict()
		image = request.files.get('image')
		if image:
			filename = secure_filename(image.filename)
			path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
			image.save(path)
			datas['image'] = filename
		datas['create_at'] = datetime.now()
		new_article = Articles.insert(datas)
		flashMessage = True

	return render_template("admin/articles/add.html", flashMessage = flashMessage)

@app.route("/admin/article/edit/<int:article_id>", methods=["GET","POST"])
def editArticle(article_id):
	flashMessage = None
	if request.method == "POST":
		datas = request.form.to_dict()
		image = request.files.get('image')
		if image:
			filename = secure_filename(image.filename)
			path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
			image.save(path)
			datas['image'] = filename

		Articles.update(datas, ['id'])
		flashMessage = True

	article = Articles.find_one(id=article_id)

	return render_template("admin/articles/edit.html", article= article, flashMessage= flashMessage)

@app.route("/admin/article/delete/<int:article_id>", methods=["GET"])
def del_article(article_id):
	Articles.delete(id=article_id)
	return redirect("/admin/articles")
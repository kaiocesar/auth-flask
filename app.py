#!/usr/bin/env python
# coding: utf-8 

import os
from werkzeug import secure_filename
from flask import Flask, request, render_template, redirect, url_for, current_app, send_from_directory
from db import Articles


app = Flask(__name__, static_url_path='')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')

@app.route("/media/<path:filename>")
def media(filename):
	return send_from_directory(current_app.config.get("MEDIA_ROOT"), filename)

@app.route("/")
def index():
	articles = Articles.all()
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


# Authentucation routes
@app.route("/admin")
def admin():
	return render_template("admin/default/index.html")

@app.route("/admin/articles", methods=["GET","POST"])
def articlesAdmin():
	return render_template("admin/articles/index.html", articles = Articles.all())

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


if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
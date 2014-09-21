from flask import Flask, request, render_template, redirect
from db import Articles

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
	return render_template("default/index.html")

@app.route("/about")
def about():
	return render_template("default/about.html")

@app.route("/contact")
def contact():
	return render_template("default/contact.html")

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
		new_article = Articles.insert(datas)
		flashMessage = True

	return render_template("admin/articles/add.html", flashMessage = flashMessage)

@app.route("/admin/article/edit/<int:article_id>", methods=["GET","POST"])
def editArticle(article_id):
	flashMessage = None
	if request.method == "POST":
		datas = request.form.to_dict()
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
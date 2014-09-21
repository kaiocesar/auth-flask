from flask import Flask, request, render_template


class flask.ext.login.LoginManager(app=None, add_context_processor=True):
login_manager = LoginManager()

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

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
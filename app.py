import os
import json
from flask import Flask
from flask import render_template, send_from_directory, Response, url_for, request

# app initialization
app = Flask(__name__)
app.config.update(
	DEBUG = True,
	SECRET_KEY = 'de2bd1431941f180a22cb2169fa6d80a0a0cbaeea597e215'
)

# controllers
@app.route('/<path:url>')
def index(url):
	url = "http://"+url
	finalUrl = "https://www.readability.com/api/content/v1/parser?url="+url+"&token=24b51ae751a061db205c4366fbdb7f4b267be3de"
	import urllib2
	response = urllib2.urlopen(finalUrl)
	html=response.read()
	web = json.loads(html)
	return render_template("render.html", web=web)

@app.route("/")
def home():
	return "welcome home"

@app.route('/about')
def about():
	return render_template('about.html')

# special file handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

# error handlers
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# server launchpad
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
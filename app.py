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

from urlparse import urlparse, urlunparse

@app.before_request
def redirect_www():
    """Redirect www requests to non-www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'www.reedme.in':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'reedme.in'
        return redirect(urlunparse(urlparts_list), code=301)

# controllers
@app.route('/<path:url>', methods=['GET'])
def index(url):
	if url.find('https://') != -1:
		url = url.replace("https://","http://")
	if url.find('http://') == -1 and url.find('https://') == -1:
		url = "http://"+url
	key = ['448add193d4827f4594d1ce2342f64eac01ddc36','24b51ae751a061db205c4366fbdb7f4b267be3de']
	import random
	number = random.randint(0,1)
	randomKey = key[number]
	finalUrl = "https://www.readability.com/api/content/v1/parser?url="+url+"&token="+randomKey
	import urllib2
	response = urllib2.urlopen(finalUrl)
	html=response.read()
	web = json.loads(html)
	return render_template("render.html", web=web)

@app.route("/")
def home():
	return render_template("index.html", pageTitle="reedme home")

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
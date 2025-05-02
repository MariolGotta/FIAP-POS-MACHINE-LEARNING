from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "user1": "password1",
    "user2": "password2"
}


def get_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
        return jsonify({"title": title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


app.config['SWAGGER'] = {
    'title': 'Minha API',
    'uiversion': 3
}

swagger = Swagger(app)


@app.route('/scrape/title', methods=['GET'])
@auth.login_required
def scrape_title():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    return get_title(url)


if __name__ == '__main__':
    app.run(debug=True)

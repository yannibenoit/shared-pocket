from flask import Flask, render_template, request, redirect, session
from back.api.pocket import Pocket
from back.database.database import MongoDB
from back.modules.user import User
from back.modules.articles import Articles
import os
import binascii

app = Flask(__name__)
pocket = Pocket()
user = User()
article = Articles()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth_pocket', methods=['GET', 'POST'])
def auth_pocket():
    if request.method == 'POST':
        if request.form.get('connect') == 'Connect my Pocket':
            code = pocket.get_app_request_token()
            redirect_uri = pocket.redirect_uri
            return redirect(f'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}')


@app.route('/get_token')
def get_session_token():
    session_id = str(binascii.hexlify(os.urandom(12)))
    return redirect(f'/get_token/{session_id}')


@app.route('/get_token/<session_id>')
def get_token(session_id):
    try:
        data = pocket.get_user_access_token()
        if data:
            name = data.get('username', '').lower()
            access_token = data.get('access_token', '')
            session['pocket_username'] = name

            if not user.get_user(name):
                user_data = {'username': name, 'access_token': access_token}
                user_id = user.create_user(user_data)
                session['pocket_user_id'] = str(user_id)
                user.create_user_index()

            return redirect(f'/data/user/{name}')
        else:
            return render_template('index.html')
    except Exception as e:
        print(e)

    return render_template('index.html')


@app.route('/data/user/<name>')
def get_content(name):
    data_ = pocket.get_user_content()
    size = len(data_['content'])
    username = session['pocket_username']
    articles = article.get_articles()
    articles_ids = [item['item_id'] for item in articles]
    try:
        for d in data_['content']:
            if d['item_id'] not in articles_ids:
                print(d)
                d.update({'user_id': user.get_user(username)['_id']})
                article.create_article(d)
                article.create_article_index()
    except Exception as e:
        print(e)
    if data_:
        return render_template('hello.html', name=username, content_size=size, articles=[item['given_title'] for item in articles])
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True, port=5000)



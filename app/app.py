from flask import Flask, render_template,request, redirect, session, url_for
import json
from bson import Binary, Code
from bson.json_util import dumps
from back.pocket.pocket import Pocket
from back.database.database import MongoDB




pocket = Pocket()
db = MongoDB()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mqjdfmqfjmsqlfjmqfjmj'

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template("homepage.html")

    @app.route('/auth_pocket', methods=['GET', 'POST'])
    def auth_pocket():
        if request.method == 'POST':
            if request.form.get('connect') == 'Connect my Pocket':
                code = pocket.get_app_request_token()
                redirect_uri = pocket.redirect_uri
                return redirect(f'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}')

    @app.route('/get_token')
    def get_token(name='user'):
        try:
            db.delete_all_documents('users')
            data = pocket.get_user_access_token()
            if data:
                name = data.get('username', '')
                access_token = data.get('access_token', '')
                user_id = db.insert('users', {'username': name,'access_token': access_token})
                session['pocket_username'] = name
                session['pocket_user_id'] = str(user_id)
                db.create_index('username', 'users')

                return redirect(f'/data/user/{user_id}')
            else:
                return render_template('index.html')
        except Exception as e:
            print(e)

        return render_template('index.html')



    @app.route('/data/user/<user_id>')
    def get_content(user_id):
        data_ = pocket.get_user_content()
        size = len(data_['content'])
        username =session['pocket_username']
        try:
            db.delete_all_documents('articles')
            for d in data_['content']:
                d.update({'user_id': session['pocket_user_id']})
                print(db.insert('articles',d))

            db.create_index('item_id', 'articles')
        except Exception as e :
            print(e)
        if data_:
            return render_template('hello.html', name=username, content_size=size)
        else:
            return render_template('index.html')

    return app

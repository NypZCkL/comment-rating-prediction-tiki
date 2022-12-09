from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.resources.comment import Comment, createcomment, commentList

api = Api(app)

@app.route('/')
def home():
    comment_list = commentList.get(commentList)[0]
    comments = comment_list['comment_list']
    return render_template('index.html', comments=comments)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(Comment, '/comment/<int:_id>')
api.add_resource(createcomment, '/comment')
api.add_resource(commentList, '/comments')
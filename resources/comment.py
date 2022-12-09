from flask_restful import Resource, reqparse
from models.comment import CommentModel
from sqlalchemy import desc

import re
import pandas as pd
import joblib
from underthesea import word_tokenize

def standardize_data(text):
  # Remove . ? , at index final
  text = re.sub(r"[\.,\?]+$-", "", text)
  # Remove all . , " ... in sentences
  text = text.replace(",", " ").replace(".", " ") \
          .replace(";", " ").replace("“", " ") \
          .replace(":", " ").replace("”", " ") \
          .replace('"', " ").replace("'", " ") \
          .replace("!", " ").replace("?", " ") \
          .replace("-", " ").replace("?", " ")
  return text.strip()

def tokenizer(text):
  return word_tokenize(text)

def lowercase(text):
  return text.lower()

acronyms = pd.read_csv('./acronym_vi.txt', delimiter='\t', names=[0, 1])
stopwords = pd.read_csv('./stopwords-nlp-vi.txt', names=[0])
stopwords = stopwords[0].to_list()

def replace_acronyms(text):
  list_text = text
  for i in range(len(text)):
    for j in range(len(acronyms)):
      if list_text[i] == acronyms[0][j]:
        list_text[i] = acronyms[1][j]
  return list_text

def remove_stopwords(text):
  list_text = text
  words = []
  for word in list_text:
    if word not in stopwords:
      words.append(word)
  return words

def join_text(list_text):
  text = ' '.join(list_text)
  return word_tokenize(text, format='text')

def process_text(text):
  result = standardize_data(text)
  result = lowercase(result)
  result = tokenizer(result)
  result = replace_acronyms(result)
  result = remove_stopwords(result)
  return join_text(result)

emb = joblib.load('./tfidf.pkl')
model_svm = joblib.load('./svm.pkl')
model_dt = joblib.load('./randomforest.pkl')
model_rf = joblib.load('./decisiontree.pkl')

class Comment(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('content',
    type=str,
    required=True,
    location='form',
    help='This field can not be blank!'
  )

  def get(self, _id):
    comment = CommentModel.find_by_id(_id)
    if comment:
      return comment.json(), 200
    return {'message': 'comment not found'}, 404

  def put(self, _id):
    comment = CommentModel.find_by_id(_id)
    if comment:
      data = self.parser.parse_args()
      if data['content'] == '':
        return {'message': 'invalid content'}, 401

      if comment.content == data['content']:
        return {'message': 'require diffferent content'}, 400

      comment.content = data['content']
      content = process_text(data['content'])
      content = emb.transform([content])
      comment.rating_svm = int(model_svm.predict(content)[0])
      comment.rating_dt = int(model_dt.predict(content)[0])
      comment.rating_rf = int(model_rf.predict(content)[0])

      comment.save_to_db()
      return comment.json(), 200
      
    return {'message': 'comment not found'}, 404
  
  def delete(self, _id):
    comment = CommentModel.find_by_id(_id)
    if comment:
      comment.delete_db()
    return {'message': 'comment deleted'}, 200

class createcomment(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('content',
    type=str,
    required=True,
    location='form',
    help='This field can not be blank!'
  )

  def post(self):
    data = self.parser.parse_args()
    if data['content'] == '':
      return {'message': 'invalid content'}, 401

    content = process_text(data['content'])
    content = emb.transform([content])

    rating_svm = int(model_svm.predict(content)[0])
    rating_dt = int(model_dt.predict(content)[0])
    rating_rf = int(model_rf.predict(content)[0])

    comment = CommentModel(content=data['content'], rating_svm=rating_svm, rating_dt=rating_dt, rating_rf=rating_rf)
    comment.save_to_db()
    return {'message': 'comment created'}, 201
    

class commentList(Resource):
  def get(self):
    comments = []
    for comment in CommentModel.query.order_by(desc(CommentModel.id)).all():
      comments.append(comment.json())
    return {'comment_list': comments}, 200
from db import db

class CommentModel(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String())
    rating_svm = db.Column(db.Integer)
    rating_dt = db.Column(db.Integer)
    rating_rf = db.Column(db.Integer)

    def __init__(self, content, rating_svm, rating_dt, rating_rf):
        self.content = content
        self.rating_svm = rating_svm
        self.rating_dt = rating_dt
        self.rating_rf = rating_rf
    
    def json(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating_svm': self.rating_svm,
            'rating_dt': self.rating_dt,
            'rating_rf': self.rating_rf,
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()
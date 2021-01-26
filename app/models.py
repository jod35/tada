from .exts import db
from datetime import datetime

########################
##### The task model####
########################


class Task(db.Model):

    '''The Task Model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"task => {self.name}"

    # save
    def save(self):
        db.session.add(self)
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_desc(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

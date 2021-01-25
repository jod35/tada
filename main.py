from flask import (
		Flask,
		jsonify,
		make_response,
		request,
		render_template
		)

from marshmallow import fields, Schema
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



import os

BASEDIR=os.path.dirname(os.path.realpath(__file__))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(BASEDIR,'tasks.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
#app.config["SQLALCHEMY_ECHO"]=True


db=SQLAlchemy(app)
fa=FontAwesome(app)

#task model
class Task(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,nullable=False)
	description=db.Column(db.Text,nullable=False)
	date=db.Column(db.DateTime,default=datetime.utcnow)

	def __repr__(self):
		return f"task => {self.name}"

	def save(self):
		db.session.add(self)
		db.session.commit()


	def delete(self):
		db.session.delete(self)
		db.session.commit()

		
#the model's schema
class TaskSchema(Schema):
	id=fields.Int()
	name=fields.Str()
	description=fields.Str()
	date=fields.DateTime()

#welcome message
@app.route('/')
def index():
	tasks=Task.query.order_by(Task.id.desc()).all()
	return render_template('index.html',tasks=tasks)


#get all tasks
@app.route('/api/tasks',methods=['GET'])
def get_all_tasks():
	tasks=Task.query.all()
	response=TaskSchema(many=True).dump(tasks)

	return make_response(jsonify({"tasks":response}),200)

#get a task by id
@app.route('/api/task/<int:id>',methods=['GET'])
def get_a_task(id):
	task=Task.query.get_or_404(id)

	response=TaskSchema().dump(task)

	return make_response(jsonify({"task":response}),200)

#create a new task
@app.route('/api/tasks',methods=['POST'])
def create_task():
	data=request.get_json()

	new_task=Task(name=data.get('name'),description=data.get('description'))

	new_task.save()
	response=TaskSchema().dump(new_task)
	return make_response(jsonify({"task":response,"success":True,"message":"CREATED"}),200)

#update a task
@app.route('/api/task/<int:id>',methods=['PUT'])
def update_task(id):
	task=Task.query.get_or_404(id)
	data=request.get_json()
	task.name=data.get('name')
	task.description=data.get('description')
	db.session.commit()

	response=TaskSchema().dump(task)
	return make_response(jsonify({"task":response,"success":True,"message":"UPDATED"}),200)


#delete a task
@app.route('/api/task/<int:id>',methods=['DELETE'])
def delete_a_task(id):
	task=Task.query.get_or_404(id)
	db.session.delete(task)
	db.session.commit()
	response=TaskSchema().dump(task)
	return make_response(jsonify({"task":response,"success":True,"message":"DELETED"}),200)




#handle a 404 error
@app.errorhandler(404)
def not_found(err):
	return make_response(jsonify({"message":"Resource Not Found"}),200)

#handle a 500 error
@app.errorhandler(500)
def internal_error(err):
	return make_response(jsonify({"message":"Internal Server Error"}),500)



if __name__ == '__main__':
	#db.create_all()
	app.run()

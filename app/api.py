from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields, Namespace
from .models import Task
from .exts import db

resources = Blueprint('api', __name__)

api = Api(resources, title="Task Api",
          default="Task Resources", default_label="The Endpoints for tasks",
          description="A simple service for tasks"
          )


task_model = api.model(
    'Task',
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "description": fields.String(),
        "date": fields.DateTime(dt_format='rfc822')
    }
)


@api.route('/tasks')
class TaskResources(Resource):
    @api.marshal_with(task_model, envelope='tasks')
    def get(self):
        ''' Get all tasks'''
        tasks = Task.get_all()

        return tasks

    @api.marshal_with(task_model, envelope='task')
    def post(self):
        ''' Create a task resource'''
        data = request.get_json()

        new_task = Task(
            name=data.get('name'),
            description=data.get('description')
        )

        new_task.save()

        return new_task


@api.route('/task/<int:id>')
class TaskResource(Resource):
    @api.marshal_with(task_model, envelope='task')
    def get(self, id):
        '''Get a task by ID'''

        task = Task.get_by_id(id)

        return task

    @api.marshal_with(task_model, envelope='task')
    def patch(self, id):
        '''Update a task with an ID'''

        task = Task.get_by_id(id)

        data = request.get_json()

        task.name = data.get('name')

        task.description = data.get('description')

        db.session.commit()

        return task

    @api.marshal_with(task_model, envelope='task')
    def delete(self, id):
        '''Delete a task by its ID'''
        task = Task.get_by_id(id)

        task.delete()

        return task

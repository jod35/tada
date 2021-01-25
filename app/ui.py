from flask import Blueprint,render_template
from .models import Task

ui=Blueprint('ui',__name__)

@ui.route('/')
def index():
    tasks=Task.get_desc()
    return render_template('index.html',tasks=tasks)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

# 初始化Flask应用
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 定义任务模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.DateTime)

    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date

# 定义任务Schema
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# 路由定义
@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    description = request.json.get('description', '')
    due_date_str = request.json.get('due_date', None)
    due_date = parse_datetime(due_date_str) if due_date_str else None

    new_task = Task(title, description, due_date)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

def parse_datetime(date_str):
    """将日期字符串转换为datetime对象"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
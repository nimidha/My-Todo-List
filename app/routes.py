from flask import Blueprint, render_template, request, redirect, url_for
from .models import ToDo
from . import db
from datetime import datetime
from datetime import date 

todo_routes = Blueprint('todo_routes', __name__)

@todo_routes.route('/')
def home():
    tasks = ToDo.query.order_by(ToDo.date_created.desc()).all()
    today = date.today()  # ✅ define 'today'
    for t in tasks:
        print(f"Task: {t.task} | Due Date: {t.due_date} | Type: {type(t.due_date)}")
    # Dashboard stats
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks

    #today = date.today()

    return render_template('add_task.html', tasks=tasks,
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks,
                           today=today)


@todo_routes.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    due_date_str = request.form.get('due_date')
    
    due_date_obj = None
    if due_date_str:
        due_date_obj = datetime.strptime(due_date_str, '%Y-%m-%d').date()

    # ✅ Include due_date when creating the task
    new_task = ToDo(task=task_content, due_date=due_date_obj)
    
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo_routes.home'))


@todo_routes.route('/complete/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task_id):
    task = ToDo.query.get_or_404(task_id)
    task.completed = not task.completed
    task.completed_date = datetime.utcnow() if task.completed else None
    db.session.commit()
    return redirect(url_for('todo_routes.home'))


@todo_routes.route('/delete/<int:id>')
def delete(id):
    task = ToDo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo_routes.home'))

# Show the edit form
@todo_routes.route('/edit/<int:task_id>')
def edit_task(task_id):
    task = ToDo.query.get_or_404(task_id)
    return render_template('edit_task.html', task=task)

# Update task after editing
@todo_routes.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = ToDo.query.get_or_404(task_id)
    task.task = request.form['task']  # Update the task text
    db.session.commit()
    return redirect(url_for('todo_routes.home'))


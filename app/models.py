from app import db
from datetime import datetime
from datetime import date

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.Date, nullable= True)


    @property
    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < date.today()
        return False
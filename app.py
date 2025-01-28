from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App Setup
app = Flask(__name__)
Scss(app)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# Data Class - Row of data
class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

#Runs the app within the local machine
with app.app_context():
    db.create_all()



# Routes To Webpages
# Homepage
@app.route("/", methods=["POST", "GET"])
def index():
    # Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = myTask(content=current_task)
        # Add to the db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # See all current tasks
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template('index.html', tasks=tasks)
    
# Delete a task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

# Edit a task
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):
    edit_task = myTask.query.get_or_404(id)
    if request.method == "POST":
        edit_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("edit.html", task=edit_task)



# Runner and Debugger     
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, redirect ,render_template, request, url_for 
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#app.config['SECRET_KEY']="secretkey"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
# app.config['SQLALCHEMY_DATABASE_URI']="mysql://username:password@localhost/db_name"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class todo(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String(100))
  complete=db.Column(db.Boolean)



@app.route("/")
def index():
  #show all todo
  todo_list=todo.query.all()
  print(todo_list)
  return render_template('base.html',todo_list=todo_list,name="Sara")

with app.app_context():
  db.create_all()
@app.route("/add",methods=["POST"])
def add():
  title=request.form.get("todo")
  new_todo=todo(title=title,complete=False)
  with app.app_context():
    db.session.add(new_todo)
    db.session.commit()
  return redirect(url_for('index'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
  todo_1=todo.query.filter_by(id=todo_id).first()
  todo_1.complete=True
  db.session.commit()
  return redirect(url_for('index'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
  # title=request.form.get("title") 
  new_todo=todo.query.filter_by(id=todo_id).first()
  # new_todo.title=title
  print(new_todo)
  db.session.delete(new_todo)
  db.session.commit()
  return redirect(url_for('index'))
if __name__=="__main__":
  app.run(debug=True)



from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return f"{self.title} - {self.sno}"


with app.app_context():
     db.create_all()    

@app.route('/',methods=['GET','POST'])
def m1():
    if request.method == 'POST': 
        title=request.form['title']
        desc =request.form['desc']
        todo= Todo(title=title , desc =desc)
        db.session.add(todo)
        db.session.commit()
    all_todo=Todo.query.all()
    print(all_todo)
    return render_template('index.html',all_todo=all_todo)

@app.route('/show')
def product():
    all_todo=Todo.query.all()
    print(all_todo)
    return 'This is product page'


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
   if request.method == 'POST':
        title=request.form['title']
        desc =request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
       
   todo=Todo.query.filter_by(sno=sno).first()
   return render_template('update.html',todo=todo)
   

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


 
if __name__ == "__main__":
    app.run(debug=True)




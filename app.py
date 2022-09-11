from flask import Flask, render_template, url_for, request, redirect

from flask_sqlalchemy import SQLAlchemy
'''
n_1 Understand the use of SQLAlchemy-
SQLAlchemy is an ORM - object relational mapper.
It transfers data stored in a sql database into python objects.
Then you can use python objects to create/update/delete data instead of writing straight sql.
(speeds up dev time)
Eg. sqlite:////tmp/test.db

To connect to different db's check: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

Eg. for local sql connect than using SQLAlchemy object: 
mysql://username:password@server/db

'''

from datetime import datetime

# n_2
app = Flask(__name__)  # syntax...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# to connect to db. ['SQLALCHEMY_DATABASE_URI']... is syntax.
db = SQLAlchemy(app)  # syntax...


# n_5
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Note primary key...
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# the above code will create the columns... , it's the syntax ...
# we call it creating a db model ~ Basically SCHEMA...
# Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def __repr__(self):
        return '<Task %r>' % self.id


# n_8
# we add methods 'POST', 'GET' to indicate how many methods would '/' route have
@app.route('/', methods=['POST', 'GET'])
def index():
    # n_10 we add the check to see it it's a POST or GET method,
    # Note that we get 'request' variable from import flask...
    if request.method == 'POST':
        task_content = request.form['content']
        # taking content part from input part (name="content") in the form which is in index.html: <input type="text" name="content" id="content" />

        # n_11, Now we add the contents/data from form to the Sqlite db. We have our data model in Todo class.
        # Hence created object for the class and passed task_content
        # Since recall, if class A {}... then object is obj = A()...
        new_task = Todo(content=task_content)

        # n_12, adding db session...
        # Recall: db = SQLAlchemy(app)
        try:
            db.session.add(new_task)
            db.session.commit()  # commit once data pushed & then redirect...
            # redirect is a function in flask itself, Used to redirect to another route
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    # n_13
    # else case where now our route is request.method == 'GET'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Note that since it is a GET req, hence we return
        # everything in our db in a dat wise sorted manner...
        # ~ Todo.query.order_by.all()...
        # and render the index.html file
        # we are passing the 'tasks' = Todo.query.order_by(Todo.date_created).all()
        # passing tasks parameter in index html file, where we see how using Jinja
        # the db contents would be rendered...
        return render_template('index.html', tasks=tasks)


# n_15 , adding delete route, added <int:id> to specifically uniquely redirect to this id to delete it
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
# got the whole row data with that id using SQLAlchemy Sqllite querying logic to delete it later
    try:
        db.session.delete(task_to_delete)
        db.session.commit()  # committing and redirecting
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


# n_final... Similarly coding the update route...
# Also for deployment we can use heroku, create a procfile & deploy..
# Just for reference if stuck: https://stackoverflow.com/questions/38851564/heroku-gunicorn-procfile
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


'''n_6
to create a route 

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html') # will render index.html in home route 
    ### return render_template('index.html', tasks=tasks) # will render same the html, but also pass tasks parameter
'''
# sidenote: you can also return a html page directly than importing file,
# though it's not a recommended approach: ''' <html> <h1> abcd </h1> </html>... '''


# n_7
if __name__ == "__main__":
    app.run(debug=True)
    # this will run app in debug mode, remove debug=True, when pushing code to prod

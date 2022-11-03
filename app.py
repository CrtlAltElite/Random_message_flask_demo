from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MessageForm(FlaskForm):
    title = StringField('Subject',validators=[DataRequired()])
    body = StringField('Message',validators=[DataRequired()])
    author = StringField('Your Name',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AuthorForm(FlaskForm):
    author = StringField('Your Name',validators=[DataRequired()])
    submit = SubmitField('Submit') 



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    author = db.Column(db.String)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    form = MessageForm()
    if request.method=='POST' and form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        author=form.author.data
        new_message = Message(title=title, body=body, author=author)
        db.session.add(new_message)
        db.session.commit()
        return "Thanks for contacting us"

    return render_template('message.html', form=form)

@app.route('/see_message', methods=['GET'])
def see_message():
    all_messages = Message.query.all()
    return render_template('my_messages.html', messages=all_messages)

@app.route('/message_by_author', methods=['GET', 'POST'])
def message_by_author():
    form = AuthorForm()
    if request.method=='POST' and form.validate_on_submit():
        author = form.author.data
        person_messages = Message.query.filter_by(author=author).all()
        return render_template('my_messages.html', messages=person_messages)
    return render_template('message_by_author.html',form=form)

@app.route('/edit_message', methods=['GET'])
def edit_message():
    messages= Message.query.all()
    return render_template('edit_message.html', messages=messages)

@app.route('/edit_form', methods=['POST'])
def edit_form():
    message_id=request.form.get("message")
    this_message=Message.query.get(message_id)
    form = MessageForm()
    return render_template('edit_form.html', form=form, message=this_message)

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    form = MessageForm()
    title=form.title.data
    body=form.body.data
    author=form.author.data
    message_to_edit = Message.query.get(id)
    message_to_edit.title=title
    message_to_edit.body=body
    message_to_edit.author=author
    db.session.add(message_to_edit)
    db.session.commit()

    return 'I editted that for you thanks!'


from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import csv
import pandas as pd 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'


class LoginForm(FlaskForm):
    # username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    gitname = StringField('gitname', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    gitname = StringField('gitname', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)]) 

@app.route('/')
def index():
    return render_template('beg.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        df_fin = pd.read_csv('reg_user.csv')
        ind = (df_fin[df_fin['Gitname']==form.gitname.data].index.values)
        pswd = df_fin.loc[ind,'Password'].values
        pswd=''.join(pswd)
        print(pswd)
        if pswd==form.password.data:
            print(pswd)
            return render_template('beg.html')
    return render_template('login.html',form=form)



@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        # print(form.username.data)
        df=pd.read_csv('reg_user.csv')
        key_list=df['Gitname'].to_list()
        if form.gitname.data not in key_list:
            with open('reg_user.csv', mode='a') as user_list:
                reg_user_writer = csv.writer(user_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                reg_user_writer.writerow([form.username.data,form.gitname.data,form.email.data,form.password.data])
        df_fin = pd.read_csv('reg_user.csv')
        ind = (df_fin[df_fin['Gitname']==form.gitname.data].index.values)
        global git_username
        git_username = df_fin.loc[ind,'Gitname'].values
        git_username=''.join(git_username)
        print(git_username)
    return render_template('signup.html',form=form)


if __name__ == '__main__':
    app.run()
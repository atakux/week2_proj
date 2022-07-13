from itertools import permutations
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from util import weather_api,places_api,suggested_places_api

app = Flask(__name__)

proxied = FlaskBehindProxy(app)  ## add this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'eae4d31ce5ddcbd006c3fca0d8183dd2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('search')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/search")
def search():
    form = ResearchForm
    if form.validate_on_submit():
        weather = weather_api(city = form.city_name.data)
        

    return render_template('search_place.html', subtitle='Search Page', text='This is the home page')

@app.route("/result")
def home():
    return render_template('result.html', subtitle='Result Page', text='Result will be displayed here')

# driver code
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
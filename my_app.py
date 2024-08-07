from flask import Flask, render_template, redirect, url_for, request
import hashlib  # библиотека для хеширования
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, LoginManager, logout_user
from models import db, Users, NewsFilms

app = Flask(__name__)

# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "SECRET_KEY"
# Initialize flask-sqlalchemy extension

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()

admin = Admin(app)
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(NewsFilms, db.session))


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/')
def main_page():
    news_all = NewsFilms.query.order_by(NewsFilms.created_at.desc()).all()
    news_all = news_all[:2]
    return render_template('main_page.html', news_all=news_all)


@app.route('/news/')
def news_page():
    news_all = NewsFilms.query.order_by(NewsFilms.created_at.desc()).all()
    return render_template('news_page.html', news_all=news_all)


@app.route('/news/<int:id>/')
def new_page(id):
    news = NewsFilms.query.filter_by(id=id).first()
    return render_template('new_page.html', news=news)


@app.route('/registration/', methods=['GET', 'POST'])
def registration_page():
    users_list = set()
    error = None  # обнуляем переменную ошибок
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        age = request.form['age']
        email = request.form['email']
        users_all = Users.query.all()
        for User in users_all:
            users_list.add(User.username)
        if username in users_list:
            error = 'Такой пользователь уже существует'
            return render_template('registration_page.html', error=error)
        elif repeat_password != password:
            error = 'Пароли не совпадают'
            return render_template('registration_page.html', error=error)
        elif int(age) < 16:
            error = 'Вы должны быть старше 16'
            return render_template('registration_page.html', error=error)
        else:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # шифруем пароль в sha-256
            user = Users(username=username, password=hashed_password, email=email)
            db.session.add(user)
            db.session.commit()
            return render_template('registration_page.html',
                                   error='Поздравляю вы зарегистрированы, теперь можете авторизоваться')
    else:
        return render_template('registration_page.html')


@app.route('/login/', methods=['GET', 'POST'])
def login_view():
    error = None  # обнуляем переменную ошибок
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # шифруем пароль в sha-256
        user = Users.query.filter_by(username=username).first()
        if user.password == hashed_password:
            login_user(user)
            return render_template('login_view.html', user=username)
        else:
            error = 'Неправильное имя пользователя или пароль'
            return render_template('login_view.html', error=error)
    else:
        return render_template('login_view.html')


@app.route('/logout/')
def logout():
    logout_user()
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)

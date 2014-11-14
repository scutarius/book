# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, session, g, flash, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm
# , oid

from database import db_session
from sqlalchemy import or_, update

from forms import LoginForm, BookUpload, SearchForm, EditAutor, EditBook, RegForm
from models import User, Book, Author

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/index', methods = ['GET', 'POST'])
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = SearchForm()
    search = request.args.get('search')
    if not search: search = ''
    
    query = db_session.query(Book.id, Book.name, Author.name).\
                            select_from(Book, Author).\
                            filter(Author.books, \
                                or_(Book.name.like(u"%%%s%%" % search), Author.name.like(u"%%%s%%" % search)))

    return render_template('index.html',
        title = 'Home',
        query=query,
        form=form
        )


def pwd_hash(gh):
    import hashlib
    h = hashlib.sha256()
    h.update(gh)
    return h.hexdigest()


@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = RegForm()
    if request.method == 'POST' and form.validate():
        login = form.login.data
        email = form.email.data
        password = pwd_hash(form.password1.data)

        user = User(login = login, password = password, email=email)
        db_session.add(user)
        db_session.commit()
        
        flash('Thanks for registering')

        return redirect(url_for('login'))
    return render_template('lr/registration.html', 
        title = 'Registration',
        form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    print form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        login = form.login.data
        password = pwd_hash(form.password.data)
        
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(login = login).first()

        if user.password==password:
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember = remember_me)
        # return redirect(url_for('index'))

    return render_template('lr/login.html', 
        title = 'Sign In',
        form = form)

@app.route('/add_book',  methods = ['GET', 'POST'])
@login_required
def add_book():
    forms = BookUpload()
    form = SearchForm()

    if request.method == 'POST':
        title = forms.title.data
        author = forms.author.data
        
        q_author = Author.query.filter_by(name=author).first()

        if q_author:
            # Убедимся, что данный автор имеет данную книгу
            # Ибо может быть другой автор с таким же названием книги
            q_book = Book.query.filter(Book.authors.any(Author.id==q_author.id), Book.name==title).first()
            if q_book:
                pass
            else:
                q_author.books.append(Book(name=title))
                db_session.add(q_author)
                db_session.commit() 
        else:
            q_author = Author(name=author)
            q_author.books.append(Book(name=title))
            db_session.add(q_author)
            db_session.commit()
        
        return redirect(url_for('add_book'))

    return render_template('book/add_book.html',
        title = 'add book',
        forms = forms,
        form = form
        )

@app.route('/edit_auth',  methods = ['GET', 'POST'])
@login_required
def edit_auth():
    forms = EditAutor()
    form = SearchForm()
    a = request.args.get('a')
    if request.method == 'POST':
        author = forms.author.data

        db_session.query(Author).filter(Author.name == a).update({'name': author})
        db_session.commit()

        return redirect(url_for('index'))

    query = db_session.query(Author).filter(Author.name==a).first()

    return render_template('book/edit_auth.html',
        title = 'edit form',
        forms = forms,
        form = form,
        name=a
        )

@app.route('/edit_book',  methods = ['GET', 'POST'])
@login_required
def edit_book():
    forms = EditBook()
    form = SearchForm()

    a = request.args.get('a')
    b = request.args.get('b')
    if request.method == 'POST':
        book = forms.book.data

        query = db_session.query(Book.id, Book.name, Author.name).\
                            select_from(Book, Author).\
                            filter(Author.books, Book.name==b, Author.name==a).first()
        id = query.id
        
        db_session.query(Book).filter(Book.id==id).update({'name': book})
        db_session.commit()

        return redirect(url_for('index'))

    return render_template('book/edit_book.html',
        title = 'edit form',
        forms = forms,
        form = form,
        name_a = a,
        name_b = b
        )

@app.before_request
def before_request():
    g.user = current_user


# @oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(login = nickname, password = resp.email)
        db_session.add(user)
        db_session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return username == 'admin' and password == 'secret'

# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#     'Could not verify your access level for that URL.\n'
#     'You have to login with proper credentials', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'})

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated

# @app.route('/secret-page')
# @requires_auth
# def secret_page():
#     return render_template('secret_page.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/_ajax_delete', methods=["POST", "GET"])
def _ajax_delete():
    id = request.args.get('id')
    query = db_session.query(Book).filter(Book.id==id).first()
    # Находим книгу, что необходимо удалить
    a_query=db_session.query(Author).filter(Author.books, Book.id==query.id).first()
    a_name = a_query.name
    # Находим автора книги и берем имя
    count=db_session.query(Book).filter(Author.books, Author.name==a_name).count()
    # Сколько у автора книг?
    if count==1:
        db_session.delete(a_query)  # Если одна - смело удаляем и автора
    db_session.delete(query)        # и книгу с базы
    db_session.commit()

    return jsonify(result='book'+str(id))


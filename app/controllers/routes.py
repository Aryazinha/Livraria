from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.book import Book
from app.models.person import Person
from app.models.borrow import Borrow
from app.models.historico import Historico
from app.models.user import User
from app.forms.login_form import LoginForm
from app.forms.registration_form import RegistrationForm
from app.forms.book_form import BookForm
from app.forms.person_form import PersonForm
from app.forms.borrow_form import BorrowForm
from flask import current_app as app
from datetime import datetime
from flask import Blueprint

main = Blueprint('main', __name__, template_folder='../templates')


@main.route('/')
@login_required
def index():
    # Dados para os gráficos do dashboard
    ranking_person = db.session.query(Person.name, db.func.count(Borrow.id)).join(Borrow).group_by(Person.id).order_by(db.func.count(Borrow.id).desc()).all()
    ranking_books = db.session.query(Book.title, db.func.count(Borrow.id)).join(Borrow).group_by(Book.id).order_by(db.func.count(Borrow.id).desc()).all()
    book_genres = db.session.query(Book.genero, db.func.count(Book.id)).group_by(Book.genero).all()
    available_books = db.session.query(Book).filter_by(available=True).all()
    unavailable_books = db.session.query(Book).filter_by(available=False).all()

    ranking_person_data = {
        'labels': [p[0] for p in ranking_person],
        'data': [p[1] for p in ranking_person]
    }

    ranking_books_data = {
        'labels': [b[0] for b in ranking_books],
        'data': [b[1] for b in ranking_books]
    }

    book_genres_data = {
        'labels': [g[0] for g in book_genres],
        'data': [g[1] for g in book_genres]
    }

    return render_template(
        "index.html",
        ranking_person_data=ranking_person_data,
        ranking_books_data=ranking_books_data,
        book_genres_data=book_genres_data,
        available_books=available_books,
        unavailable_books=unavailable_books
    )



@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form =  LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha inválidos')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)

        user.last_login = datetime.utcnow()
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template(
        "login.html",
        form = form
    )

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso! Você pode fazer login agora.')
        
        return redirect(url_for('main.login'))
    
    return render_template(
        "register.html",
        form = form
    )

@main.route('/books', methods=['GET', 'POST'])
@login_required
def manager_books():
    form = BookForm()

    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genero=form.genero.data,
            available=form.available.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )

        db.session.add(book)
        db.session.commit()
        flash('Livro adicionado com sucesso!')

        return redirect(url_for('main.manager_books'))

    books = Book.query.all()
    
    return render_template(
        "books.html",
        form=form,
        books=books
    )

@main.route('/books/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    Borrow.query.filter_by(book_id=book.id).delete()
    Historico.query.filter_by(book_id=book.id).delete()

    db.session.delete(book)
    db.session.commit()
    flash(f"Livro '{book.title}' excluído com sucesso!")

    return redirect(url_for('main.manager_books'))


@main.route('/books/update/<int:book_id>', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.genero = form.genero.data
        book.available = form.available.data
        book.updated_by = current_user.id

        db.session.commit()
        flash(f"Livro '{book.title}' atualizado com sucesso!")

        return redirect(url_for('main.manager_books'))
    
    return render_template(
        "book_form.html",
        form=form,
    )


@main.route('/persons', methods=['GET', 'POST'])
@login_required
def manager_persons():
    form = PersonForm()

    if form.validate_on_submit():
        person = Person(
            name=form.name.data,
            sobrenome=form.sobrenome.data,
            email=form.email.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )

        db.session.add(person)
        db.session.commit()
        flash('Pessoa adicionada com sucesso!')

        return redirect(url_for('main.manager_persons'))

    persons = Person.query.all()

    return render_template(
        "persons.html",
        form=form,
        persons=persons
    )


@main.route('/persons/update/<int:person_id>', methods=['GET', 'POST'])
@login_required
def update_person(person_id):
    person = Person.query.get_or_404(person_id)
    form = PersonForm(obj=person)

    if form.validate_on_submit():
        person.name = form.name.data
        person.sobrenome = form.sobrenome.data
        person.email = form.email.data
        person.updated_by = current_user.id

        db.session.commit()
        flash(f"Pessoa '{person.name}' atualizada com sucesso!")

        return redirect(url_for('main.manager_persons'))

    return render_template(
        "person_form.html",
        form=form,
    )


@main.route('/persons/delete/<int:person_id>', methods=['GET', 'POST'])
@login_required
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)

    Borrow.query.filter_by(person_id=person.id).delete()
    Historico.query.filter_by(person_id=person.id).delete()

    db.session.delete(person)
    db.session.commit()
    flash(f"Pessoa '{person.name}' excluída com sucesso!")

    return redirect(url_for('main.manager_persons'))


@main.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow_book():
    form = BorrowForm()

    form.book_id.choices = [(book.id, book.title) for book in Book.query.filter_by(available=True).all()]
    form.person_id.choices = [(person.id, f"{person.name} {person.sobrenome}") for person in Person.query.all()]

    if form.validate_on_submit():
        borrow = Borrow(
            book_id=form.book_id.data,
            person_id=form.person_id.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )

        book = Book.query.get(form.book_id.data)
        book.available = False

        db.session.add(borrow)
        db.session.commit()

        historico = Historico(
            book_id = form.book_id.data,
            person_id = form.person_id.data,
            borrow_date = datetime.utcnow(),
            return_date = None
        )

        db.session.add(historico)
        db.session.commit()

        return redirect(url_for('main.borrow_book'))

    return render_template(
        "borrow_form.html",
        form=form
    )

@main.route('/historico')
@login_required
def view_historico():
    historico = Historico.query.order_by(Historico.borrow_date.desc()).all()

    return render_template(
        "historico.html",
        historico=historico
    )

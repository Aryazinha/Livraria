from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_wtf import CSRFProtect

from flask_login import LoginManager



db = SQLAlchemy()

migrate = Migrate()

csrf = CSRFProtect()

login_manager = LoginManager()



def create_app():

    app = Flask(__name__)

    app.config.from_object('config.Config')



    db.init_app(app)

    migrate.init_app(app, db)

    csrf.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'main.login'



    from app.controllers.routes import main

    app.register_blueprint(main)



    from app.models.user import User



    @login_manager.user_loader

    def load_user(user_id):

        return User.query.get(int(user_id))



    with app.app_context():



        from app.models.book import Book

        from app.models.person import Person

        from app.models.borrow import Borrow

        from app.models.historico import Historico



        db.create_all()



    return app


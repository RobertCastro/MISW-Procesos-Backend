from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from modelos import db, Usuario
from app_utils import add_resources_urls

def create_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admon_reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app_context = app.app_context()
    app_context.push()
    add_resources_urls(app)
    CORS(app)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Usuario.query.filter_by(id=identity).one_or_none()

    return app


if __name__ == '__main__':
    app = create_flask_app()
    db.init_app(app)
    db.create_all()
    app.run()
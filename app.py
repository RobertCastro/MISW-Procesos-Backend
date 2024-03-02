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

    db.init_app(app)

    # Add CORS support
    CORS(app)

    # Initialize JWT
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Usuario.query.filter_by(id=identity).one_or_none()

    add_resources_urls(app)
    
    return app

app = create_flask_app()

if __name__ == '__main__':
    app.run()
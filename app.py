from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from vistas.bancos import VistaBancos
from vistas.movimiento import VistaMovimiento
from vistas.movimientos import VistaMovimientos
from vistas.propiedades import VistaPropiedades
from vistas.propiedad import VistaPropiedad
from vistas.reserva import VistaReserva
from vistas.reservas import VistaReservas
from vistas.sign_in import VistaSignIn
from vistas.login import VistaLogIn
from modelos import db, Usuario
from vistas.tipo_movimientos import VistaTipoMovimientos
from vistas.roles import VistaRoles
from vistas.tipo_ids import VistaTipoId
from vistas.mantenimientos import VistaMantenimientos

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

    # Register API endpoints
    api = Api(app)
    api.add_resource(VistaSignIn, '/signin', '/signin/<int:id_usuario>')
    api.add_resource(VistaLogIn, '/login')
    api.add_resource(VistaPropiedades, '/propiedades')
    api.add_resource(VistaPropiedad, '/propiedades/<int:id_propiedad>')
    api.add_resource(VistaReservas, '/propiedades/<int:id_propiedad>/reservas')
    api.add_resource(VistaReserva, '/reservas/<int:id_reserva>')
    api.add_resource(VistaMovimientos, '/propiedades/<int:id_propiedad>/movimientos')
    api.add_resource(VistaMovimiento, '/movimientos/<int:id_movimiento>')
    api.add_resource(VistaBancos, '/bancos')
    api.add_resource(VistaTipoMovimientos, '/tipo-movimientos')
    api.add_resource(VistaRoles, '/roles')
    api.add_resource(VistaTipoId, '/tipo-ids')
    
    # Mantenimientos
    api.add_resource(VistaMantenimientos, '/propiedades/<int:id_propiedad>/mantenimientos')
    return app

app = create_flask_app()

if __name__ == '__main__':
    # Only run the app if executed directly
    app.run(
        debug=True
    )

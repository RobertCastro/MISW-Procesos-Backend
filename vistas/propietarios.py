from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc
from flask import jsonify

from modelos import Usuario, db, UsuarioSchema

usuario_schema = UsuarioSchema()

class VistaPropietarios(Resource):
    @jwt_required()
    def get(self):
        if current_user.rol.value != 'ADMINISTRADOR':
            return {'mensaje': 'No tiene permisos para listar usuarios'}, 400
        
        propietarios = Usuario.query.filter(Usuario.rol == 'PROPIETARIO').all()

        return [{'nombre':propietario.nombre } for propietario in propietarios],200
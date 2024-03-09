from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoRol


class VistaRoles(Resource):

    @jwt_required()
    def get(self):
        return jsonify([rol.name for rol in TipoRol])

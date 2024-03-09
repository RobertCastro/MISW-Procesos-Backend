from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoId


class VistaTipoId(Resource):

    @jwt_required()
    def get(self):
        return jsonify([tipo_id.name for tipo_id in TipoId])

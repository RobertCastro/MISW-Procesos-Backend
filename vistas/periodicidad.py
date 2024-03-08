from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import Periodicidad


class VistaPeriodicidad(Resource):

    @jwt_required()
    def get(self):
        return jsonify([periodicidad.name for periodicidad in Periodicidad])

import json
from flask import make_response, request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, db
from sqlalchemy import exc
mantenimiento_schema = MantenimientoSchema(many=True)

class VistaConsultarUnMantenimiento(Resource):

    @jwt_required()
    def get(self, id_mantenimiento):

        if mantenimiento is None:
            return {"mensaje": "Mantenimiento no encontrado"}, 404

        mantenimientos_query = Mantenimiento.query.filter_by(id=id_mantenimiento)
        mantenimiento = mantenimientos_query.one_or_404()

        return mantenimiento_schema.dump(mantenimiento), 200
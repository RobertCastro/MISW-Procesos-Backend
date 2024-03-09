import json
from flask import make_response, request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, db
from sqlalchemy import exc
mantenimiento_schema = MantenimientoSchema()

class VistaConsultarUnMantenimiento(Resource):

    @jwt_required()
    def get(self, id_mantenimiento):
        try:
            mantenimientos_query = Mantenimiento.query.filter_by(id=id_mantenimiento)
            mantenimiento = mantenimientos_query.one_or_none()
            if not mantenimiento:
                return {"error": "El mantenimiento no existe"}, 404
            return mantenimiento_schema.dump(mantenimiento)
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error consultando el mantenimiento'}, 409
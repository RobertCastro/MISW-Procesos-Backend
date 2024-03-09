import json
from flask import make_response, request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, db
from sqlalchemy import exc
from vistas.utils import buscar_mantenimiento
mantenimiento_schema = MantenimientoSchema(many=True)

class VistaEditarMantenimientos(Resource):
    
    @jwt_required()
    def put(self, id_propiedad, id_mantenimiento):
        try:
            rol = current_user.rol.value
            if rol != 'ADMINISTRADOR':
                return {'mensaje': 'No tiene permisos para crear mantenimientos'}, 400
            
            propiedad = Propiedad.query.get(id_propiedad)
            if not propiedad:
                return {"error": "La propiedad no existe"}, 404            
            
            resultado_buscar_mantenimiento = buscar_mantenimiento(id_mantenimiento, current_user.id)
            if resultado_buscar_mantenimiento.error:
                return resultado_buscar_mantenimiento.error

            mantenimiento = resultado_buscar_mantenimiento.mantenimiento

            mantenimiento_schema.load(request.json, session=db.session, instance=mantenimiento, partial=True)
            db.session.commit() 
            return mantenimiento_schema.dump(mantenimiento)
        
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error editando el mantenimiento. Revise los datos proporcionados'}, 409
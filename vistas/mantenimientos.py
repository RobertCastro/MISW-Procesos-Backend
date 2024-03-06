import json
from flask import make_response, request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, db
from sqlalchemy import exc
mantenimiento_schema = MantenimientoSchema(many=True)

class VistaMantenimientos(Resource):

    @jwt_required()
    def get(self, id_propiedad):
        current_user = get_current_user()
        propiedad = Propiedad.query.get(id_propiedad)

        if propiedad is None:
            return {"mensaje": "Propiedad no encontrada"}, 404

        if current_user.rol.value != 'ADMINISTRADOR' and propiedad.id_usuario != current_user.id:
            return {"mensaje": "Acceso denegado"}, 403

        mantenimientos_query = Mantenimiento.query.filter_by(id_propiedad=id_propiedad)
        mantenimientos = mantenimientos_query.all()

        return mantenimiento_schema.dump(mantenimientos), 200
    
    
    @jwt_required()
    def post(self, id_propiedad):
        try:
            esquema = MantenimientoSchema(session=db.session)
            datos = request.get_json()
            mantenimiento = esquema.load(datos)
            
            rol = current_user.rol.value
            if rol != 'ADMINISTRADOR':
                return {'mensaje': 'No tiene permisos para crear mantenimientos'}, 403
            
            propiedad = Propiedad.query.get(id_propiedad)
            if not propiedad:
                return {"error": "La propiedad no existe"}, 404

            mantenimiento.id_propiedad = id_propiedad
            db.session.add(mantenimiento)
            db.session.commit()

        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error creando el mantenimiento. Revise los datos proporcionados'}, 500
        
        return esquema.dump(mantenimiento), 201

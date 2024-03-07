from flask import request
from flask_jwt_extended import get_current_user, jwt_required
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
    def put(self, id_propiedad, id_mantenimiento):
        current_user = get_current_user()

        if current_user.rol.value != 'ADMINISTRADOR':
            return {"mensaje": "Acceso denegado"}, 403

        propiedad = Propiedad.query.get(id_propiedad)

        if propiedad is None:
            return {"mensaje": "Propiedad no encontrada"}, 404

        mantenimiento = Mantenimiento.query.get(id_mantenimiento)

        if mantenimiento is None:
                    return {"mensaje": "Mantenimiento no encontrado"}, 404
        
        #TODO: Completar estraegia de edicion.


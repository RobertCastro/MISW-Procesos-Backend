from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc

from modelos import Propiedad, db, PropiedadSchema

propiedad_schema = PropiedadSchema()


class VistaPropiedades(Resource):

    @jwt_required()
    def post(self):
        rol=current_user.rol.value
        try:
            if rol != 'ADMINISTRADOR':
                return {'mensaje': 'No tiene permisos para crear propiedades'}, 400
            propiedad = propiedad_schema.load(request.json, session=db.session)
            propiedad.id_usuario = current_user.id
            db.session.add(propiedad)
            db.session.commit()
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'mensaje': 'Hubo un error creando la propiedad. Revise los datos proporcionados'}, 400
        return propiedad_schema.dump(propiedad), 201
    
    @jwt_required()
    def get(self):
        if current_user.rol.value == 'ADMINISTRADOR':
            propiedades = Propiedad.query.all()
        else:
            propiedades = Propiedad.query.filter(Propiedad.id_usuario == current_user.id)

        return propiedad_schema.dump(propiedades, many=True)

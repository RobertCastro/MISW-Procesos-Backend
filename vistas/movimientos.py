from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Movimiento, MovimientoSchema, Propiedad, db
from vistas.utils import buscar_propiedad
from sqlalchemy import exc

movimiento_schema = MovimientoSchema()


class VistaMovimientos(Resource):

    @jwt_required()
    def post(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
           return resultado_buscar_propiedad.error
        try:
            rol=current_user.rol.value
            if rol != 'ADMINISTRADOR':
                return {'mensaje': 'No tiene permisos para crear movimientos'}, 400
            movimiento = movimiento_schema.load(request.json, session=db.session)
            movimiento.id_propiedad = id_propiedad
            db.session.add(movimiento)
            db.session.commit()
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error creando el movimiento. Revise los datos proporcionados'}, 400
        return movimiento_schema.dump(movimiento), 201

    @jwt_required()
    def get(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
           return resultado_buscar_propiedad.error
        
        rol=current_user.rol
        movimientos=None

        if rol.value =='ADMINISTRADOR':
            movimientos = db.session.query(Movimiento).filter(Movimiento.id_propiedad == id_propiedad).all()
        else:
            movimientos = db.session.query(Movimiento).join(Propiedad).filter(Propiedad.id_usuario == current_user.id, Propiedad.id == id_propiedad).all()
        return movimiento_schema.dump(movimientos, many=True)
    
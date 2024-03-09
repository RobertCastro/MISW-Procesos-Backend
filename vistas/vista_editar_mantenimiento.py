import json
from flask import make_response, request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import Mantenimiento, MantenimientoSchema, Propiedad, db
from sqlalchemy import exc
from vistas.utils import buscar_mantenimiento
mantenimiento_schema = MantenimientoSchema()

class VistaEditarMantenimientos(Resource):
    
    @jwt_required()
    def put(self, id_propiedad, id_mantenimiento):
        print('Editar mantenimiento id_propiedad:', id_propiedad)
        print('Editar mantenimiento id_mantenimiento:', id_mantenimiento)

        try:
            rol = current_user.rol.value
            if rol != 'ADMINISTRADOR':
                return {'mensaje': 'No tiene permisos para editar mantenimientos'}, 400
            
            print('antes de consultar propiedad')
            propiedad = Propiedad.query.get(id_propiedad)
            print('propiedad:', propiedad)
            if not propiedad:
                return {"error": "La propiedad no existe"}, 404            
            
            print('current user: ', current_user.id)
            print('id_mantenimiento:', id_mantenimiento)
            resultado_buscar_mantenimiento = buscar_mantenimiento(id_mantenimiento, current_user.id)
            if resultado_buscar_mantenimiento.error:
                return resultado_buscar_mantenimiento.error
            
            mantenimiento = resultado_buscar_mantenimiento.mantenimiento

            print('mantenimiento:', mantenimiento)
            print('request.json:', request.json)
            print('ACTUAL mantenimiento.id:', mantenimiento.id)
            print('NUEVO mantenimiento.id:', request.json.get('id'))
            print('ACTUAL mantenimiento.id_propiedad:', mantenimiento.id_propiedad)
            print('NUEVO mantenimiento.id_propiedad:', request.json.get('id_propiedad'))
            print('ACTUAL mantenimiento.id_usuario:', mantenimiento.id_usuario)
            print('NUEVO mantenimiento.id_usuario:', request.json.get('id_usuario'))
            print('ACTUAL mantenimiento.tipo_mantenimiento:', mantenimiento.tipo_mantenimiento)
            print('NUEVO mantenimiento.tipo_mantenimiento:', request.json.get('tipo_mantenimiento'))
    


           
            mantenimiento_en_edicion = json.loads(json.dumps(request.json))
            
            mantenimiento_schema.load(mantenimiento_en_edicion, 
                                      session=db.session, 
                                      instance=Mantenimiento().query.get(id_mantenimiento), 
                                      partial=True)
            

            db.session.commit() 
            return mantenimiento_schema.dump(mantenimiento)
        
        except ValidationError as validation_error:
            return validation_error.messages, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'mensaje': 'Hubo un error editando el mantenimiento. Revise los datos proporcionados'}, 409
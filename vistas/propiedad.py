from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from modelos import Propiedad, PropiedadSchema, db, Usuario
from vistas.utils import buscar_propiedad

propiedad_schema = PropiedadSchema()

class VistaPropiedad(Resource):

    @jwt_required()
    def put(self, id_propiedad):
        rol = current_user.rol.value

        if rol != 'ADMINISTRADOR':
            return {"mensaje": "usuario no es administrador no puede editar propiedad"}, 404

        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        for key, value in request.json.items():
            setattr(resultado_buscar_propiedad.propiedad, key, value)
        
        nombre_propietario = request.json.get('nombre_propietario')
        
        if nombre_propietario:
            propietario = Usuario.query.filter(Usuario.nombre == nombre_propietario, Usuario.rol == 'PROPIETARIO').first()
            
            if not propietario:
                return {"mensaje": "El nombre de propietario a ingresar no existe en el listado de propietarios"}, 400

            celular_propietario = propietario.celular
            setattr(resultado_buscar_propiedad.propiedad, 'numero_contacto', celular_propietario)

        if nombre_propietario == '':
                return {"mensaje": "El nombre de propietario no puede estar vacío"}, 400

        db.session.commit() 
        return propiedad_schema.dump(resultado_buscar_propiedad.propiedad)
    
    @jwt_required()
    def delete(self, id_propiedad):
        rol = current_user.rol.value
        if rol != 'ADMINISTRADOR':
            return "El usuario no es administrador no debe poder eliminar propiedades", 400
        
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        Propiedad.query.filter(Propiedad.id == id_propiedad).delete()
        db.session.commit()
        return "", 204
    
    @jwt_required()
    def get(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        return propiedad_schema.dump(resultado_buscar_propiedad.propiedad)

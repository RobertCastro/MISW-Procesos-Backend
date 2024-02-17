from sqlalchemy import exc
from flask import request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource

from modelos import db, Usuario, UsuarioSchema

usuario_schema = UsuarioSchema()


class VistaSignIn(Resource):

    def post(self):

        rol = str(request.json["rol"])

        if rol == "":
            return {"mensaje": "El rol no puede ser vacio"}, 400
        
        if request.json["usuario"] == "":
            return {"mensaje": "El usuario no puede ser vacio"}, 400
        
        if request.json["contrasena"] == "":
            return {"mensaje": "La contrasena no puede ser vacia"}, 400
        
        if len(request.json["usuario"]) > 50:
            return {"mensaje": "El usuario debe tener maximo 50 caracteres"}, 400

        if rol == "PROPIETARIO":
            if request.json["nombre"] == "":
                return {"mensaje": "El nombre no puede ser vacio"}, 400
            
            if request.json["apellidos"] == "":
                return {"mensaje": "Los apellidos no pueden ser vacios"}, 400
            
            if request.json["tipoIdentificacion"] == "":
                return {"mensaje": "El tipo de identificacion no puede ser vacio"}, 400
            
            if request.json["correo"] == "":
                return {"mensaje": "El correo no puede ser vacio"}, 400
            
            if request.json["celular"] == "":
                return {"mensaje": "El celular no puede ser vacio"}, 400
            
            if request.json["identificacion"] == "":
                return {"mensaje": "La identificacion no puede ser vacia"}, 400

        nuevo_usuario = None

        if rol == "PROPIETARIO":
            nuevo_usuario = Usuario(
                usuario=request.json["usuario"], 
                contrasena=request.json["contrasena"],
                rol=request.json["rol"],
                nombre=request.json["nombre"],
                apellidos=request.json["apellidos"],
                tipo_id=request.json["tipoIdentificacion"],
                identificacion=request.json["identificacion"],
                correo=request.json["correo"],
                celular=request.json["celular"])
            
        if rol == "ADMINISTRADOR":
            nuevo_usuario = Usuario(
                usuario=request.json["usuario"], 
                contrasena=request.json["contrasena"],
                rol=request.json["rol"])

        db.session.add(nuevo_usuario)
        
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return {"mensaje": "Ya existe un usuario con este identificador"}, 400
        
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado", "token": token_de_acceso, "id": nuevo_usuario.id}, 201

    @jwt_required()
    def put(self, id_usuario):
        usuario_token = current_user
        if id_usuario != current_user.id:
            return {"mensaje": "Peticion invalida"}, 400
        usuario_token.contrasena = request.json.get("contrasena", usuario_token.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario_token)

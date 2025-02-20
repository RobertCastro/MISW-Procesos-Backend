from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from modelos import Usuario, db


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        if usuario is None:
            return "Verifique los datos ingresados", 404
        
        additional_claims = {
            "rol": usuario.rol.name
        }
        
        token_de_acceso = create_access_token(identity=usuario.id, additional_claims=additional_claims)
        return {"mensaje": "Inicio de sesion exitoso", "token": token_de_acceso,"rol":usuario.rol.value, "idUsuario" : usuario.id}, 200

import json
from modelos import Usuario, db, TipoRol
from flask_jwt_extended import create_access_token, decode_token

class TestVistaLogin:

    def setup_method(self):
        usuario = Usuario(usuario='test_user', contrasena='123456', rol=TipoRol.ADMINISTRADOR.value)
        db.session.add(usuario)
        db.session.commit()

        self.datos_usuario = {
            'usuario': 'test_user',
            'contrasena': '123456',
            'rol':TipoRol.ADMINISTRADOR.value
        }

    def actuar(self, client, datos_usuario):
        self.respuesta = client.post('/login', data=json.dumps(datos_usuario), headers={'Content-Type': 'application/json'})
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_si_login_exitoso(self, client):
        self.actuar(client, self.datos_usuario)
        assert self.respuesta.status_code == 200

    def test_retorna_token_si_login_exitoso(self, client):
        self.actuar(client, self.datos_usuario)
        assert 'token' in self.respuesta_json.keys()

    def test_retorna_rol_si_login_exitoso(self, client):
        self.actuar(client, self.datos_usuario)
        access_token = self.respuesta_json['token']
        decoded_token = decode_token(access_token)
        assert decoded_token['rol'] == "ADMINISTRADOR"

    def test_retorna_404_si_login_fallido_usuario(self, client):
        self.datos_usuario.update({'usuario': 'usuario_no_existe'})
        self.actuar(client, self.datos_usuario)
        assert self.respuesta.status_code == 404

    def test_retorna_404_si_login_fallido_contrasena(self, client):
        self.datos_usuario.update({'contrasena': '123'})
        self.actuar(client, self.datos_usuario)
        assert self.respuesta.status_code == 404

    def test_retorna_404_si_login_fallido_usuario_contrasena(self, client):
        datos_incorrectos = {
            'usuario': 'usuario_no_existe',
            'contrasena': '123',
        }
        self.actuar(client, datos_incorrectos)
        assert self.respuesta.status_code == 404

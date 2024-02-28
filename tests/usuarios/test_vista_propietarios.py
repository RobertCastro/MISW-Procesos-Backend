#corre con pytest -s -k test_vista_propietarios.py
import json
from faker import Faker
from flask_jwt_extended import create_access_token
from modelos import Usuario, db,TipoRol


class TestListarPropietarios:

    def setup_method(self):
        self.data_factory = Faker()
        self.datos_usuario_admin = Usuario(usuario='test_admin', contrasena='123456', rol=TipoRol.ADMINISTRADOR.value)
        self.datos_usuario_propietario = Usuario(usuario='test_propietario', contrasena='123456', rol=TipoRol.PROPIETARIO.value, nombre=self.data_factory.name(), apellidos=self.data_factory.name(), correo=self.data_factory.email(), celular=self.data_factory.phone_number())

        db.session.add(self.datos_usuario_admin)
        db.session.add(self.datos_usuario_propietario)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()

    def actuar(self, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get('/propietarios', headers=headers)
        self.respuesta_json = self.respuesta.json
    
    def test_listar_propietarios_retorna_201(self, client):
        token_admin= create_access_token(identity=self.datos_usuario_admin.id)
        self.actuar(client,token_admin)
        assert self.respuesta.status_code == 200

    
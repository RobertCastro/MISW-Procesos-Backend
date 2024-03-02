#corre con pytest -s -k test_vista_propietarios.py
import json
from faker import Faker
from flask_jwt_extended import create_access_token
from modelos import Usuario, db,TipoRol


class TestListarPropietarios:

    def setup_method(self):
        self.data_factory = Faker()
        self.datos_usuario_admin = Usuario(usuario='test_admin', contrasena='123456', rol=TipoRol.ADMINISTRADOR.value)
        self.datos_usuario_propietario_1 = Usuario(usuario='test_propietario_1', contrasena='123456', rol=TipoRol.PROPIETARIO.value, nombre=self.data_factory.name(), apellidos=self.data_factory.name(), correo=self.data_factory.email(), celular=self.data_factory.phone_number())
        self.datos_usuario_propietario_2 = Usuario(usuario='test_propietario_2', contrasena='123456', rol=TipoRol.PROPIETARIO.value, nombre=self.data_factory.name(), apellidos=self.data_factory.name(), correo=self.data_factory.email(), celular=self.data_factory.phone_number())
        self.datos_usuario_propietario_sin_cel = Usuario(usuario='test_propietario_3', contrasena='123456', rol=TipoRol.PROPIETARIO.value, nombre=self.data_factory.name(), apellidos=self.data_factory.name(), correo=self.data_factory.email(), celular='')

        db.session.add(self.datos_usuario_admin)
        db.session.add(self.datos_usuario_propietario_1)
        db.session.add(self.datos_usuario_propietario_2)
        db.session.add(self.datos_usuario_propietario_sin_cel)
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

    def test_listar_propietarios_retorna_lista_de_propietarios_con_cel(self, client):
        token_admin= create_access_token(identity=self.datos_usuario_admin.id)
        self.actuar(client,token_admin)
        assert len(self.respuesta_json) == 2
        
        propietarios_nombres=[propietario["nombre"] for propietario in self.respuesta_json]
        assert self.datos_usuario_propietario_1.nombre in propietarios_nombres
        assert self.datos_usuario_propietario_2.nombre in propietarios_nombres

    def test_dar_propietarios_sin_permisos_retorna_400(self, client):
        token_propietario= create_access_token(identity=self.datos_usuario_propietario_1.id)
        self.actuar(client,token_propietario)
        assert self.respuesta.status_code == 400
        assert self.respuesta_json['mensaje'] == 'No tiene permisos para listar usuarios'
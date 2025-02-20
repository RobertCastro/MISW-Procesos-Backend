import json
from faker import Faker
from flask_jwt_extended import create_access_token
from modelos import Usuario, db


class TestCrearUsuario:

    def setup_method(self):
        self.data_factory = Faker()
        self.datos_nuevo_usuario = {
            'usuario': self.data_factory.name(),
            'contrasena': self.data_factory.word(),
            'rol': 'ADMINISTRADOR'
        }

        self.datos_nuevo_usuario_propietario = {
            'usuario': self.data_factory.name(),
            'contrasena': self.data_factory.word(),
            'rol': 'PROPIETARIO',
            'nombre': self.data_factory.name(),
            'apellidos': self.data_factory.name(),
            'celular': self.data_factory.phone_number(),
            'correo': self.data_factory.email(),
            'tipoIdentificacion': 'CEDULA',
            'identificacion': self.data_factory.random_number()
        }

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()

    def actuar(self, nuevo_usuario_info, client):
        self.respuesta = client.post('/signin', data=json.dumps(nuevo_usuario_info), headers={'Content-Type': 'application/json'})
        self.respuesta_json = self.respuesta.json
    
    def test_crear_usuario_responde_201(self, client):
        self.actuar(self.datos_nuevo_usuario, client)
        assert self.respuesta.status_code == 201

    def test_crear_usuario_mismo_usuario_retorna_400(self, client):
        usuario = Usuario(usuario='usuario_test', contrasena='123456', rol='ADMINISTRADOR')
        db.session.add(usuario)
        db.session.commit()

        self.datos_nuevo_usuario.update({'usuario': 'usuario_test'})
        self.actuar(self.datos_nuevo_usuario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_rol_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario.update({'rol': ''})
        print(self.datos_nuevo_usuario)
        self.actuar(self.datos_nuevo_usuario, client)
        assert self.respuesta.status_code == 400
    
    def test_retorna_campos_esperados(self, client):
        self.actuar(self.datos_nuevo_usuario, client)
        assert 'token' in self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'mensaje' in self.respuesta_json

    def test_crea_usuario_en_db(self, client):
        self.actuar(self.datos_nuevo_usuario, client)
        usuario_db = Usuario.query.filter(Usuario.usuario == self.datos_nuevo_usuario['usuario']).all()
        assert len(usuario_db) == 1

    def test_crear_usuario_propietario(self, client):
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 201

        usuario_db = Usuario.query.filter(Usuario.usuario == self.datos_nuevo_usuario_propietario['usuario']).all()
        assert len(usuario_db) == 1
        
        assert usuario_db[0].nombre == self.datos_nuevo_usuario_propietario['nombre']
        assert usuario_db[0].apellidos == self.datos_nuevo_usuario_propietario['apellidos']
        assert str(usuario_db[0].celular) == str(self.datos_nuevo_usuario_propietario['celular'])
        assert usuario_db[0].correo == self.datos_nuevo_usuario_propietario['correo']
        assert usuario_db[0].tipo_id.name == self.datos_nuevo_usuario_propietario['tipoIdentificacion']
        assert str(usuario_db[0].identificacion) == str(self.datos_nuevo_usuario_propietario['identificacion'])

    def test_crear_usuario_propietario_nombre_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'nombre': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400
    
    def test_crear_usuario_propietario_apellidos_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'apellidos': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_tipo_identificacion_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'tipoIdentificacion': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_correo_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'correo': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_celular_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'celular': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_tipo_identificacion_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'tipoIdentificacion': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_identificacion_vacio_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'identificacion': ''})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_usuario_51_caracteres_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'usuario': 'a'*51})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400
    
    def test_crear_usuario_propietario_nombre_51_caracteres_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'nombre': 'a'*51})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_apellidos_51_caracteres_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'apellidos': 'a'*51})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    def test_crear_usuario_propietario_identificacion_no_numerica_retorna_400(self, client):
        self.datos_nuevo_usuario_propietario.update({'identificacion': 'a'*10})
        self.actuar(self.datos_nuevo_usuario_propietario, client)
        assert self.respuesta.status_code == 400

    
class TestActualizarUsuario:
    
    def setup_method(self):
        self.usuario = Usuario(usuario='test_user', contrasena='123456')
        db.session.add(self.usuario)
        db.session.commit()

        self.usuario_token = create_access_token(identity=self.usuario.id)
        self.usuario_info = {
            'usuario': 'usuario_cambiado',
            'contrasena': 'nueva_contrasena'
        }

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()

    def actuar(self, client, usuario_info=None, usuario_id=None, token=None):
        usuario_info = usuario_info or self.usuario_info
        usuario_id = usuario_id or self.usuario.id
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})

        self.respuesta = client.put(f'/signin/{usuario_id}', data=json.dumps(usuario_info), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_actualizar_usuario_solo_actualiza_contrasena(self, client):
        self.actuar(client, token=self.usuario_token)
        usuario_db = Usuario.query.filter(Usuario.id == self.usuario.id).first()
        assert usuario_db.usuario != 'usuario_cambiado'
        assert usuario_db.usuario == 'test_user'
        assert usuario_db.contrasena == 'nueva_contrasena'

    def test_retorna_400_si_token_usuario_no_coincide_con_usuario_id_en_url(self, client):
        self.actuar(client, usuario_id=1234, token=self.usuario_token)
        assert self.respuesta.status_code == 400
        assert self.respuesta_json == {"mensaje": "Peticion invalida"}

    def test_retorna_401_si_token_no_es_enviado(self, client):
        self.actuar(client)
        assert self.respuesta.status_code == 401

    def test_retorna_200_si_actualizacion_exitosa(self, client):
        self.actuar(client, token=self.usuario_token)
        assert self.respuesta.status_code == 200

    def test_retorna_campos_esperados(self, client):
        self.actuar(client, token=self.usuario_token)
        assert 'usuario' in self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'propiedades' in self.respuesta_json

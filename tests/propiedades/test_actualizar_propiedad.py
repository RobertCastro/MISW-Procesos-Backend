# se corre con pytest -k test_actualizar_propiedad.py
import json

from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Banco, db


class TestActualizarPropiedad:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456',rol='PROPIETARIO',nombre="nombre1",celular='1234567')
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456',rol='PROPIETARIO',nombre="nombre2",celular='7654321')
        self.usuario_3 = Usuario(usuario='usuario_3', contrasena='123456',rol='ADMINISTRADOR')
        self.usuario_propietario_cel_vacio = Usuario(usuario='usuario_propietario_cel_vacio', contrasena='123456',rol='PROPIETARIO',nombre="usuario_propietario_cel_vacio",celular='')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.add(self.usuario_3)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='nombre1', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()
        
    def actuar(self, datos_propiedad, propiedad_id, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.put(f'/propiedades/{propiedad_id}', data=json.dumps(datos_propiedad), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_al_actualizar_propiedad(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propiedad': 'nombre actualizado',
                'direccion': 'nueva direccion'
                
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        assert self.respuesta.status_code == 200

    def test_retorna_401_no_token(self, client):
        self.actuar(
            {
                'nombre_propiedad': 'nombre actualizado',
                'direccion': 'nueva direccion'
            },
            self.propiedad_1_usu_1.id,
            client,
        )
        assert self.respuesta.status_code == 401

    def test_actualiza_solo_campos_enviados(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propiedad': 'nombre actualizado',
                'direccion': 'nueva direccion'
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        propiedad_db = Propiedad.query.filter(Propiedad.id == self.propiedad_1_usu_1.id).first()
        assert propiedad_db.nombre_propiedad == 'nombre actualizado'
        assert propiedad_db.direccion == 'nueva direccion'
        assert propiedad_db.ciudad == 'Boyaca'
        assert propiedad_db.municipio == 'Paipa'

    def test_retorna_404_si_usuario_no_administrador(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id) 
        self.actuar(
            {
                'nombre_propiedad': 'nombre actualizado',
                'direccion': 'nueva direccion'
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_1
        )
        assert self.respuesta.status_code == 404
        assert self.respuesta_json == {"mensaje": "usuario no es administrador no puede editar propiedad"}

    def test_actualizar_nombre_propietario_y_contacto(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propietario': self.usuario_2.nombre
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        propiedad_db = Propiedad.query.filter(Propiedad.id == self.propiedad_1_usu_1.id).first()
        
        assert propiedad_db.nombre_propietario == self.usuario_2.nombre

        #al actualizar el nombre de propietario el metodo debe actualizar automaticamente el contacto
        assert str(propiedad_db.numero_contacto) == str(self.usuario_2.celular)

    def test_retorna_400_al_actualizar_propiedad_nombrepropietario_no_listado(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propietario': 'nombre no listado'
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        assert self.respuesta.status_code == 400

    def test_retorna_400_al_actualizar_propiedad_nombre_propietario_vacio(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propietario': ''
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        assert self.respuesta.status_code == 400
    
    def test_retorna_400_al_actualizar_propiedad_celular_propietario_vacio(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id) 
        self.actuar(
            {
                'nombre_propietario': self.usuario_propietario_cel_vacio.nombre
            },
            self.propiedad_1_usu_1.id,
            client,
            token_usuario_3
        )
        assert self.respuesta.status_code == 400
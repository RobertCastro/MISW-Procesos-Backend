import json
from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Mantenimiento, MantenimientoSchema, TipoMantenimiento, Banco, db, Periodicidad


class TestCrearMantenimiento:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456',rol='ADMINISTRADOR')
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456',rol='ADMINISTRADOR')
        self.usuario_3 = Usuario(usuario='usuario_3', contrasena='123456',rol='PROPIETARIO')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.add(self.usuario_3)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        self.propiedad_2_usu_1 = Propiedad(nombre_propiedad='Apto edificio Alto', ciudad='Bogota',
                              direccion='cra 100#7-21 apto 1302', nombre_propietario='Carlos Julio', numero_contacto='666777999', banco=Banco.NEQUI,
                              numero_cuenta='3122589635', id_usuario=self.usuario_1.id)
        self.propiedad_3_usu_3 = Propiedad(nombre_propiedad='Casa Playa Hermosa', ciudad='Guanacaste',
                        direccion='playa Hermosa', nombre_propietario='Carlos Julio', numero_contacto='666777999', banco=Banco.NEQUI,
                        numero_cuenta='3122589635', id_usuario=self.usuario_3.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.add(self.propiedad_2_usu_1)
        db.session.add(self.propiedad_3_usu_3)
        db.session.commit()

        self.mantenimiento_1 = Mantenimiento(costo=56800, tipo_mantenimiento=TipoMantenimiento.LIMPIEZA.value, id_propiedad=self.propiedad_1_usu_1.id, id_usuario=self.usuario_1.id, periodicidad=Periodicidad.MENSUAL.value, estado=True) 
        
        db.session.add(self.mantenimiento_1)
        db.session.commit()

        self.datos_mantenimiento = {
            'id_propiedad' : self.propiedad_1_usu_1.id,
            'id_usuario' : self.usuario_1.id,
            'costo' : 123,
            'periodicidad' : Periodicidad.SEMANAL.value,
            'tipo_mantenimiento': TipoMantenimiento.ARREGLO.value,
            'estado': True
        }

    def teardown_method(self):
        db.session.rollback()
        Propiedad.query.delete()
        Usuario.query.delete()
        Mantenimiento.query.delete()

    def actuar(self, client, id_propiedad, datos_mantenimiento=None, token=None):
        datos_mantenimiento = datos_mantenimiento or self.datos_mantenimiento
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.post(f'/propiedades/{id_propiedad}/mantenimientos', data=json.dumps(datos_mantenimiento), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_201(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert self.respuesta.status_code == 201

    def test_retorna_mantenimiento_creado(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'periodicidad' in self.respuesta_json
        assert 'costo' in self.respuesta_json
        assert 'tipo_mantenimiento' in self.respuesta_json
        assert 'id_usuario' in self.respuesta_json
        assert 'id_propiedad' in self.respuesta_json
        assert 'estado' in self.respuesta_json

    def test_crea_registro_db(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert Mantenimiento.query.filter(Mantenimiento.id == self.respuesta_json['id'],
                                       Mantenimiento.id_propiedad == self.propiedad_1_usu_1.id).one_or_none()

    def test_retorna_201_crear_mantenimiento_propiedad_otro_usuario(self, client):
        token_usuario_2 = create_access_token(identity=self.usuario_2.id)
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_2)
        assert self.respuesta.status_code == 201

    def test_crea_mantenimiento_propiedad_enviada_url(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.datos_mantenimiento.update({'id_propiedad': 123})
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert Mantenimiento.query.filter(Mantenimiento.id == self.respuesta_json['id'],
                                       Mantenimiento.id_propiedad == self.propiedad_1_usu_1.id).one_or_none()

    def test_retorna_400_crear_mantenimiento_usuario_propietario(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id)
        self.actuar(client, self.propiedad_3_usu_3.id, token=token_usuario_3)
        assert self.respuesta.status_code == 400

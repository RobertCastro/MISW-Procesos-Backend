from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Banco, db


class TestEliminarPropiedad:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456',rol='PROPIETARIO')
        self.usuario_2 = Usuario(usuario='usuario_2', contrasena='123456',rol='PROPIETARIO')
        self.usuario_3 = Usuario(usuario='usuario_3', contrasena='123456',rol='ADMINISTRADOR')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.add(self.usuario_3)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()

    def actuar(self, propiedad_id, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.delete(f'/propiedades/{propiedad_id}', headers=headers)

    def test_eliminar_propiedad_admin_retorna_204(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id)
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_3)
        assert self.respuesta.status_code == 204
    
    def test_eliminar_propiedad_propietario_retorna_400(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_1)
        assert self.respuesta.status_code == 400  

    def test_eliminar_propiedad_elimina_registro_db(self, client):
        token_usuario_3 = create_access_token(identity=self.usuario_3.id)
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_3)
        assert Propiedad.query.filter(Propiedad.id == self.propiedad_1_usu_1.id).first() is None
        
    def test_eliminar_propiedad_sin_token_retorna_401(self, client):
        self.actuar(self.propiedad_1_usu_1.id, client)
        assert self.respuesta.status_code == 401
    
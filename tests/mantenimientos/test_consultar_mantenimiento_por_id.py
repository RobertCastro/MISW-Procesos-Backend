from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Mantenimiento, MantenimientoSchema, Banco, db
from datetime import datetime

class TestConsultarMantenimientoPorId:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', contrasena='123456', rol='PROPIETARIO')
        db.session.add(self.usuario_1)
        db.session.commit()

        self.propiedad_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1)
        db.session.commit()

        self.mantenimiento_1 = Mantenimiento(
            estado=1,
            costo=1000,
            tipo_mantenimiento='LIMPIEZA',
            periodicidad='SEMANAL',
            id_propiedad=self.propiedad_1.id,
            id_usuario=self.usuario_1.id)
        
        
        db.session.add(self.mantenimiento_1)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Mantenimiento.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()

    def actuar(self, client, id_propiedad, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get(f'/mantenimientos/'+str(self.obtener_un_id_mantenimiento_existente()), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_el_mantenimiento(self, client):
        token_usuario_1 = create_access_token(identity=self.usuario_1.id)
        self.actuar(client, self.propiedad_1.id, token_usuario_1)
        assert self.respuesta.status_code == 200


    def obtener_un_id_mantenimiento_existente(self):
        mantenimiento = Mantenimiento.query.first()
        return mantenimiento.id

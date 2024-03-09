from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Mantenimiento, MantenimientoSchema, Banco, db
from datetime import datetime
import json

class TestEditarMantenimientos:

    def setup_method(self):
        self.usuario_admin = Usuario(usuario='usuario_admin', contrasena='123456', rol='ADMINISTRADOR')
        db.session.add(self.usuario_admin)
        db.session.commit()

        self.usuario_propietario = Usuario(usuario='usuario_prop', contrasena='123456',rol='PROPIETARIO',nombre="nombre_prop",celular='7654321')
        db.session.add(self.usuario_propietario)
        db.session.commit()

        self.propiedad_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario=self.usuario_propietario.nombre, numero_contacto=self.usuario_propietario.celular, banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_propietario.id)
        
        db.session.add(self.propiedad_1)
        db.session.commit()

        self.mantenimiento_1 = Mantenimiento(
            estado=1,
            costo=1000,
            tipo_mantenimiento='LIMPIEZA',
            periodicidad='SEMANAL',
            id_propiedad=self.propiedad_1.id,
            id_usuario=self.usuario_propietario.id)
        
        
        db.session.add(self.mantenimiento_1)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Mantenimiento.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()

    def actuar(self,datos_mantenmiento, client, id_propiedad, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        id_mantenimiento_editar = str(self.obtener_un_id_mantenimiento_existente())
        self.respuesta = client.put(f'/propiedades/{id_propiedad}/mantenimientos/'+id_mantenimiento_editar, data=json.dumps(datos_mantenmiento), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_al_actualizar_mantenimiento(self, client):
        token_usuario_admin = create_access_token(identity=self.usuario_admin.id) 
        self.actuar(datos_mantenmiento=
            {
                'costo': '500',
            },
            client=client,
            id_propiedad=str(self.propiedad_1.id),
            token=token_usuario_admin
        )
        assert self.respuesta.status_code == 200

    def obtener_un_id_mantenimiento_existente(self):
        mantenimiento = Mantenimiento.query.filter_by(id_propiedad=self.propiedad_1.id).first()
        return mantenimiento.id
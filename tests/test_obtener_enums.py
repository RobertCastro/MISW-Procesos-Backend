from flask_jwt_extended import create_access_token
from modelos import Usuario, db

def test_bancos(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456')
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/bancos', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 41


def test_tipo_movimientos(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456')
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/tipo-movimientos', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 2
    assert 'INGRESO' in response_json
    assert 'EGRESO' in response_json

def test_roles(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456')
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/roles', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 2
    assert 'ADMINISTRADOR' in response_json
    assert 'PROPIETARIO' in response_json

def test_tipo_id(client):
    usuario_1 = Usuario(usuario='usuario_1', contrasena='123456')
    db.session.add(usuario_1)
    db.session.commit()

    token_usuario_1 = create_access_token(identity=usuario_1.id)
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token_usuario_1}'}
    response = client.get('/tipo-ids', headers=headers)
    response_json = response.json
    assert isinstance(response_json, list)
    assert len(response_json) == 3
    assert 'CEDULA' in response_json
    assert 'PASAPORTE' in response_json
    assert 'LICENCIA' in response_json
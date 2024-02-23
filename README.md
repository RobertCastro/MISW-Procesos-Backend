# MISW4201-202411-Backend-Grupo23
Espacio de trabajo del grupo 23
 
## Reporte
* Ingrese a [Jenkins](http://157.253.238.75:8080/jenkins-misovirtual/).
* Busque el repositorio MISW4201-202411-Backend-Grupo23.
* En la barra lateral izquierda, ubique los espacios de GitInspector y Coverage report. Al abrirlos, en la parte superior derecha utilice el enlace Zip para descargarlos y visualizarlos correctamente.

## Crear entorno virtual
Es buena practica crear un entorno virtual para aislar la aplicacion, sus dependencias y versiones del resto en su computador.
Para crear un nuevo entorno virtual ejecute:

```bash
python3 -m venv entorno
```

## Activar el entorno
Para activar el entorno virtual ejecute:
```bash
source entorno/bin/activate
```

## Instalar las dependencias (dentro del entorno)
Para instalar las dependencias que requiere el proyecto ejecute:
```bash
pip install -r requirements.txt
```

o

```bash
sudo pip3 install -r requirements.txt
```

## Instalar flask manualmente
Puede ser que no se haya instalado las libs de flask y sqlalchemy de forma automatica. Para solucionar esto ejecute:

```bash
sudo pip3 install flask
sudo pip3 install flask_cors
sudo pip3 install flask_jwt_extended
sudo pip3 install flask_restful
sudo pip3 install sqlalchemy
sudo pip3 install flask_sqlalchemy
sudo pip3 install marshmallow
sudo pip3 install marshmallow_sqlalchemy
```bash

## Iniciar la aplicación
Para iniciar la aplicación ejecute:

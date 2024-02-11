# Documentación Proyecto MISW4201-202411-Backend-Grupo23

## Datos del Equipo

**Proyecto:** Mi Corta Estancia - 
**Grupo**: Grupo 23

| **Nombre** | **Rol** |
|:----------|:-----------------------|
| Jhon Puentes | Scrum Master/Desarrollador
| Daniel Gamez | Representante Product Owner/Desarrollador
| Maria Alas | Desarrollador
| Robert Castro | Desarrollador / Devops

## Contexto

El propósito de mi Corta Estancia es permitir la administración por un tercero de propiedades que se ofrecen para rentas de corta estancia en diferentes plataformas como AirBnB y Booking, además de permitir a los dueños de las propiedades ver la información de sus respectivas propiedades. En la aplicación el administrador puede gestionar propiedades, reservas, los gastos e ingresos de cada propiedad, así como gestionar sus mantenimientos. Además, el administrador puede generar un resumen de los ingresos y egresos de la propiedad. Por otro lado, los propietarios podrán visualizar sus propiedades, los movimientos relacionados a las mismas y generar reportes. 

<details>
  <summary><h2>Requerimientos</h2></summary>

[Backlog en Jira](proyecto-de-jira)
  
Código | Nombre | Detalle
-- | -- | --
PA-8 | Ver listado de propiedades | Como usuario quisiera ver la lista propiedades por nombre con las debidas opciones de ver, editar o eliminar al lado de la propiedad. Para poder ver todas las propiedades registradas en corta estancia
PA-9 | Ver detalle de propiedades | Como usuario quisiera darle click a ver detalles de una propiedad [desde el listado de propiedades] y que se despliegue al lado derecho de la misma página la información de la propiedad para poder ver el nombre de la propiedad, la ciudad, el municipio, la dirección, el nombre del propietario, el número de contacto, el banco y el número de cuenta.
PA-11 | Crear propiedad single page | Como usuario quiero que al darle click a crear una nueva propiedad [desde el listado de propiedades] se despliegue al lado derecho un formulario para llenar la información, este debe solicitar el nombre de la propiedad, la cuidad, el municipio, la dirección, el nombre del propietario, el número de contacto, el banco y el número de cuenta.
PA-12 | Registrar Propietario | Yo como propietario y dueño de inmuebles registrados en la plataforma de corta estancia quiero poder registrarme en la plataforma para poder consultar información relacionada a mis propiedades que tengo administradas en la plataforma.
PA-13 | Iniciar sesión como propietario | Yo como propietario y dueño de inmuebles registrados en la plataforma de corta estancia quiero poder iniciar sesión en la aplicación con mi usuario y clave para poder acceder a la información de mis propiedades y estar enterado de la gestión administrativa.
PA-10 | Ver listado de propiedades por rol | Como administrador/propietario quisiera ver la lista de propiedades solamente por nombre y las debidas opciones, ver, editar, eliminar habilitadas o deshabilitadas según el rol del usuario. Para poder ver todas las propiedades registradas en corta estancia según el rol.
PA-15 | Editar propietario en propiedad para rol administrador | Yo como administrador de la plataforma de corta estancia y administrador de los inmuebles registrados en el sistema quiero poder editar el dato de propietario en todos y cada una de las propiedades para mantener actualizada la información en el sistema.
PA-5 | Restringir vista movimientos para rol propietario | Como propietario quisiera ver la lista de movimientos de mis propiedades sin tener posibilidad de crear, editar o eliminar movimientos. Esto para poder informarme de los movimientos de mis propiedades sin tener la posibilidad de realizar cambios en el sistema.
PA-16 | Crear mantenimiento | Como usuario administrador de propiedades quiero poder crear tareas de mantenimiento para las propiedades para que pueda asegurar el buen estado y funcionamiento de las instalaciones para los huéspedes.
PA-14 | Listar mantenimientos | Como usuario de la plataforma de corta estancia quiero ver una lista de los mantenimientos que ha tenido cada propiedad registrada en el sistema para estar informado sobre los mantenimientos realizados y por hacer.
PA-17 | Editar mantenimientos | Como usuario administrador de propiedades quiero poder editar las tareas de mantenimiento existentes para que pueda actualizar la información o reprogramar las tareas según sea necesario.
PA-18 | Eliminar mantenimientos | Como usuario administrador de propiedades quiero poder eliminar tareas de mantenimiento programadas para que pueda gestionar eficientemente los mantenimientos que ya no son necesarios o han sido completados.
PA-6 | Ajustar campos en crear movimientos | Como administrador del sistema, quiero poder crear movimientos con los nuevos campos de categoría y descripción y sin el campo de concepto. Esto para poder hacer una gestión más adecuada de los movimientos.
PA-7 | Ajustar campos en ver movimientos | Como usuario del sistema quiero poder ver los movimientos de una propiedad con los campos de categoría y descripción y sin el campo de concepto. Lo anterior para poder hacer un mejor seguimiento de los movimientos.
</details>

<details>
  <summary><h2>Planificación</h2></summary>
  
![Planificacion Corta Estancia (1)](https://github.com/MISW-4201-ProcesosDesarrolloAgil/MISW4201-202411-Backend-Grupo23/assets/142242801/b79e0dc5-ed97-4a03-9fc7-acd07dc06e67)

  [Link de la planificación](https://miro.com/app/board/uXjVNvXF3-0=/?share_link_id=842970653616)
  
</details>

<details>
  <summary><h2>Control de Cambios</h2></summary>

ID | C1
-- | --
Tipo | Documentación
Cambio | Actualizar los documentos de arquitectura según los nuevos requerimientos
Impacto | Ajuste de los diagramas de arquitectura para eventualmente ajustar el código con base a este nuevo diseño
Decisión | Se ajusto el diagrama de clases con nuevas propiedades y clases y el diagrama de flujos de interfaces con las nuevas pantallas

</details>


## Arquitectura
* [Arquitectura Sprint 1](Arquitectura)
* Arquitectura Sprint 2
* Arquitectura Sprint 3

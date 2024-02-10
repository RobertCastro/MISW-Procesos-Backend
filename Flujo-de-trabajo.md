## Repositorios

| Nombre | Ubicación (url/directorio) | Propósito |
|--------|-----------------------------|-----------|
|MISW4201-202411-Backend-Grupo23|https://github.com/MISW-4201-ProcesosDesarrolloAgil/MISW4201-202411-Backend-Grupo23|Desarrollo del backend del proyecto para el curso: Procesos de desarrollo ágil |
|  MISW4201-202411-Frontend-Grupo23      |            https://github.com/MISW-4201-ProcesosDesarrolloAgil/MISW4201-202411-Frontend-Grupo23                 |   Código Interfaz de usuario      |

## Ramas

| Nombre rama | Propósito |
|-------------|-----------|
|main|La rama principal se utiliza para combinar y desplegar en el entorno de producción el trabajo realizado por todos los miembros del equipo.|
|develop|Esta rama incluye las nuevas funcionalidades que se planean añadir en la próxima versión que será enviada a la rama Main. |
|hotfix| Esta rama contiene la versión de producción que presenta un fallo crítico que necesita corrección inmediata. Tras solucionar el problema, se fusiona con la rama Main y develop para corregir el fallo en todas ellas. |
|release| Esta rama es una réplica de Develop, preparada o casi preparada para el lanzamiento en producción. |
|feature/funcionalidad|Esta rama es una réplica exacta de Develop y se utiliza para el desarrollo de nuevas funcionalidades en un entorno seguro. Una vez que estas funcionalidades están listas para ser lanzadas, se integran en Develop para su inclusión en futuras versiones. |

## Acuerdos

| Acción | Quién | Cuándo | Dónde |
|--------|-------|--------|-------|
|Integrar los cambios en la rama Main | Todos los integrantes | Continuamente durante la etapa de desarrollo. | Repositorio remoto |
|Comentarios de acuerdo a las funcionalidades | Todos los integrantes | Al hacer un commit | En cada rama creada |
|Resolver conflictos | Todos los integrantes | Al identificar un conflicto | Rama feature local |
|Crear rama de acuerdo a la funcionalidad feature/funcionalidad | Todos los integrantes | Al iniciar el desarrollo de cada funcionalidad | En cada rama creada |
|Revisión de código | Todos los integrantes | Antes de fusionar con Main y Develop | En la rama feature |
|Entrega continua | Todos los integrantes | Con cada cambio significativo | En la rama feature|

## URLs ambientes en Heroku

Producción frontend: https://cortaestancia-frontend-grupo23-1a91c70c014c.herokuapp.com/ 

Producción backend: https://cortaestancia-backend-grupo23-b0c55df4af13.herokuapp.com/ 

Desarrollo frontend: en proceso de despliegue con el tutor 

Desarrollo backend: en proceso de despliegue con el tutor 





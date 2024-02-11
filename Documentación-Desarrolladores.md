# Ejecución Angular

para ejecutar angular en el computador local se utiliza el comando 

ng serve

o 

ng s

estos comando por default corren el environment local ubicado en la carpeta de environments del proyecto. Si desea conectar la aplicacion de angular local con los backends de los ambientes de heroku debe correr los siguientes comandos segun corresponda.

ng serve --configuration=production 

ng serve --configuration=development 

ng serve --configuration=test
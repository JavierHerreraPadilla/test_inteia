# README

## INSTALACIÓN
La aplicación se puede ejecutar simplemente creado la imagen de docker y corriendo el container. 
No hay necesidad de instalar paquetes o dependencias. 
Tener Docker instalado en la máquina. Puede descargar Docker en https://www.docker.com/get-started.

### En la terminal, navegando al directurio en dónde se clonó el proyecto, ejecutar:

docker build -t nombre_de_la_imagen .

docker run -d -p 8000:8000 nombre_de_la_imagen


La aplicación correrá automaticamente en http://localhost:8000/


### Para detener y borrar el container

En la termninal:

docker stop <ID_DEL_CONTENEDOR>
docker rm <ID_DEL_CONTENEDOR>


## DOMENTACIÓN
La API está docuemtnada con swagger en <b>http://localhost:8000/docs</b>


## PAQUETES
Utilicé FastAPI como backend framwork y sqlalchemy como ORM.


## CONFIGURACIÓN
La app está configurada para correr en el container de docker.


## RUTAS
Rutas:

* / Método: GET
Función: get_events
Descripción: Esta ruta permite obtener una lista de eventos. Puedes filtrar los eventos por su estado de "checked" y su tipo de evento. Si no se proporciona ningún filtro, se devolverán todos los eventos.
Ruta: /event/{event_id} - Obtener un Evento por ID

* /event/{event_id} Método: GET
Función: get_event
Descripción: Esta ruta permite obtener un evento específico por su ID. Si el evento no existe, devuelve un error 404. Además, si el evento no está marcado como "checked", lo marca como "checked" y actualiza el campo "work" (requiere o no requiere gestión) según su tipo.


Ruta: /create_event - Crear un Evento
* Método: POST
Función: create_event
Descripción: Esta ruta permite crear un nuevo evento. Se espera un objeto JSON que contiene los detalles del evento, como nombre, tipo, descripción y fecha. Luego, el evento se agrega a la base de datos y se devuelve como respuesta.


Ruta: /check-event/{event_id} - Actualizar un Evento
* Método: PATCH
Función: check_event
Descripción: Esta ruta permite actualizar un evento existente. Se espera un objeto JSON con los campos que se desean actualizar. Luego, se aplican las actualizaciones al evento y se devuelve como respuesta.
Ruta: /del/{event_id} - Eliminar un Evento


Ruta: /del/{event_id} - Eliminar un Evento
* Método: DELETE
Función: delete_event
Descripción: Esta ruta permite eliminar un evento por su id. Si el evento no existe, se devuelve un error 404. Si se elimina con éxito, se devuelve un mensaje de confirmación.

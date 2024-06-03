Como seria el user journey? El usuario paga y luego se le entregan las contrasenas.

Podemos hacer una version gratuita? Podriamos hacer una version que solo traiga datos de los ultimos 3 meses y que algunos graficos no se muestren.

Lasc credenciales de los usuarios las podriamos guardar en un google spreadsheet. Cuando el usuario se registra o realiza el pago, agregamos un usuario y una password a ese documento. Luego, el app de streamlit, cuando el usuario intenta loguearse o acceder a la app, consulta ese documento para verificar si el usuario y la password son correctos.

Tiene que haber un tab para que el usuario ingrese la cookie. Tiene que haber un input y algo que diga cuanto tiempo falta para que la cookie se venza. Donde guardamos la cookie? La podemos guardar en el cliente con alguna herramienta como esta https://github.com/ktosiek/streamlit-cookies-manager . U otra opcion es guardarla en el mismo google spreadsheet que las credenciales.

Como le indicamos al usuario cuando fue la ultima vez que se actualizaron los datos? Podemos usar la misma tecnica que con los csv, agregando la fecha en el nombre. Lo unico que cada vez que realicemos una actualizacion vamos a borrar el csv anterior.

Como hacemos con los textos? Hay que encontrar una forma de que solo se actualicen ciertos valores dentro del texto.

Que hacemos con el analisis de la competencia? 
Necesitamos el token de una cuenta de retailer. Como lo podemos obtener? Le podemos preguntar a Luquitas que se le ocurre.
Tal vez el analisis de la competencia pueda ser algo basico, donde mostramos los fullfillment times, la cantidad de reviews y ratings, y la cantidad minima de compra.


- Hacer una request para obtener los page views de una cuenta (done)
- Guardar los resultados en un csv en google cloud storage (done)
- Consumir los resultados desde google cloud storage (done)
- Hacer un grafico con los resultados
- Mostrar de alguna forma el progreso de la request y cuanto falta (done)
- Ver si lo del cambio del nombre no rompio nada (done)

Podemos hacer que el usuario se registre para una version gratuita? En el google spreadsheet guardasmos una tercer columna llamada "plan".


Es la version gratis, asique no esta mal que tenga que carga la cookie cada vez que quiera ingresar
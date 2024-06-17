import pandas as pd
import streamlit as st

from dashboard.data_scripts.get_reviews import get_reviews_data

from dashboard.global_utils import (get_date_from_blob_name)

# tiene sentido que le digamos como priorizar a la gente que no dio una review?
# tal vez podemos hacer la misma request, pero para diferentes montos comprados en total y cantidad de ordenes?
# para cada request tendriamos que traernos la lista de clientes, para que si el usurio los quiere ver pueda 

# esto ultimo parece lo mas facil de hacer. Tal vez no es necesario 

# como hacemos para saber si un cliente ya dio su review o no?

# cuantos clientes de los que no dejaron review pertenecen ademas al top 20%? a esos se les puede mandar un direct message

# como se si las campanas para conseguir reviews tienen algun resultado?

# Lo que podriamos hacer es ver si la gente que deja una review:
# - le mandamos un mensaje directo pidiendole una review => esto tal vez es un poco complicado => habria que ver como funciona el api de los mensajes
# - le mandamos un mail pidiendole por una review

# Tenemos que identificar cual es el segmento que


# Endpoint para obtener los diferentes segments https://www.faire.com/api/v3/crm/b_arceup81f2/segments 

# puedo ver en la orden si el retailer dejo una review o todavia no?
# puedo saber si una orden es la primera que hace el retailer o no => de que me sirve este dato?

# Cada review tiene un brand_order_token, que, entiendo que, lo que hace es conectar la review con una orden especifica

# Parece que por cada orden se puede dejar una review. Hay retailers que han dejado mas de un review

# lo que podemos analizar es por mes la cantidad de ordenes que pertenecen a alguin que compra por primera vez
# que dejaron una review en los siguientes 90 dias.

# =====================================================================================================

# Lo que vamos a hacer es analizar las ordenes que se hicieron por mes y la cantidad
# de esas ordenes que recibieron una review en los siguientes 90 dias

# Tambien podemos analizar que gente ya dejo una review y volvio a comprar para volver a pedirle

# Todos:
# - Bajar todas las reviews (done)

# - Analizar para los ultimos meses que porcentaje de las ordenes se termina haciendo una review

# - Traer desde la tabla de customers quien compro en los ultimos 90 dias, pero todavia no dejo una review
#   Vemos cuantos estan en el top 20% por order volume. A esos les mandamos un mensaje directo pidiendole una review

# - Analizar que retailers realizaron una orden en los ultimos 90 dias, que ya dejaron una review y podrian volver a dejar otra.
#   Mostramos la lista con los nombres

def create_review_optimization_section(selected_client):

    df_reviews, blob_name = get_reviews_data(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_reviews is None or df_reviews.empty:
        st.write("No reviews data available. Go to the 'Account' section to update it.")

    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_reviews.empty:
        st.dataframe(df_reviews)
        st.markdown("""
                    #### Recommendations:
                    """)
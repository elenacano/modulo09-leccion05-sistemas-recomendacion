# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd

# Para visualización de datos
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

def get_index_from_title(title, dataframe):
    """
    Obtiene el índice de un dataframe basado en el título de una película.

    Parameters:
    ----------
    title : str
        El título de la película a buscar.
    dataframe : pd.DataFrame
        El dataframe que contiene la información, con una columna 'title'.

    Returns:
    -------
    int
        El índice correspondiente al título de la película en el dataframe.
    """
    return dataframe[dataframe.name == title].index[0]


def get_title_from_index(index, dataframe):
    """
    Obtiene el título de una película basado en su índice en un dataframe.

    Parameters:
    ----------
    index : int
        El índice de la película a buscar.
    dataframe : pd.DataFrame
        El dataframe que contiene la información, con una columna 'title'.

    Returns:
    -------
    str
        El título de la película correspondiente al índice proporcionado.
    """
    return dataframe[dataframe.index == index]["name"].values[0]


def plot(peli1, peli2, dataframe):
    """
    Genera un gráfico de dispersión que compara dos películas en un espacio de características.

    Parameters:
    ----------
    peli1 : str
        Nombre de la primera película a comparar.
    peli2 : str
        Nombre de la segunda película a comparar.
    dataframe : pd.DataFrame
        Un dataframe transpuesto donde las columnas representan películas y las filas características.

    Returns:
    -------
    None
        Muestra un gráfico de dispersión con anotaciones para cada película.
    """
    x = dataframe.T[peli1]     
    y = dataframe.T[peli2]

    n = list(dataframe.columns)    

    plt.figure(figsize=(10, 5))

    plt.scatter(x, y, s=0)      

    plt.title('Espacio para {} VS. {}'.format(peli1, peli2), fontsize=14)
    plt.xlabel(peli1, fontsize=14)
    plt.ylabel(peli2, fontsize=14)

    for i, e in enumerate(n):
        plt.annotate(e, (x[i], y[i]), fontsize=12)  

    plt.show();



def recomendacion_videojuego(similarity, df):
    try:
        juego = input("Intruduzca el último juego al que ha jugado:")
        index = get_index_from_title(juego, df)
    except:
        print("El videojuego introducido no existe.")
    
    similar_games = list(enumerate(similarity[index]))

    # ordenamos los resultados
    peli_similares_ordenadas = sorted(similar_games, key=lambda x:x[1],reverse=True)[1:11]

    # buscamos el top 10 de los videojuegos más relacionados
    top_simiar_movies = {}
    for i in peli_similares_ordenadas:
        top_simiar_movies[get_title_from_index(i[0], df)] = round(float(i[1]),2)

    # visualizamos los resultados
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    # Crear gráfico de barras
    sns.barplot(
        x=list(top_simiar_movies.values()), 
        y=list(top_simiar_movies.keys()), 
        palette="mako"
    )

    # Añadir etiquetas y título
    plt.title(f"Top Videojuegos Similares a {juego} Basado en Contenido", fontsize=16, pad=20)
    plt.xlabel("Similitud", fontsize=12)
    plt.ylabel("Videojuegos", fontsize=12)

    # Añadir valores al final de cada barra
    # for i, value in enumerate(top_simiar_movies.values()):
    #     plt.text(value + 0.02, i, f"{value:.2f}", va='center', fontsize=10)

    plt.tight_layout()


def recomendacion_popularidad(df):

    genero = input("Introduzca el género deseado:")

    if genero not in df["genre"].unique():
        print("Género no válido")
        return

    aux = input("Desea obtener recomendaciones por: \n A-Puntuación\n B- Número de reviews")
    if aux.lower() == "a":
        metrica1 = "overall_player_rating"
        metrica2 = "number_of_english_reviews"

    elif aux.lower() == "b":
        metrica1 = "number_of_english_reviews"
        metrica2 = "overall_player_rating"
    else:
        print("Opción no válida")
        return

    df_filtered = df[df["genre"] == genero]
    top = df_filtered.sort_values(by=[metrica1, metrica2], ascending=False)[:10]
    print(f"Las 10 películas más recomendadas en base a {metrica1} para el género {genero} son:")
    display(top["game_name"].reset_index().drop(columns=["index"]))

    return

        
    
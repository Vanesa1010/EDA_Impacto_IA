import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import variables as v


def cargar_csv(ruta):
    """Lee un CSV y devuelve un DataFrame. Avisa con un error claro si el archivo no existe."""
    if not os.path.exists(ruta):
        print(f"No se encuentra el archivo: {ruta}")
    return pd.read_csv(ruta)


def crear_tramos(df, columna, etiquetas):
    """Divide una columna numérica en grupos del mismo tamaño aproximado (cuantiles).

    El número de grupos es el número de etiquetas que se le pasan.
    Devuelve una Serie con el tramo de cada fila.
    """
    return pd.qcut(df[columna], q=len(etiquetas), labels=etiquetas)


def crear_grafico(datos, tipo, titulo, xlabel="", ylabel="", colores=None,
                  mostrar_valores=True, formato=".2f", mascara=None,
                  etiqueta_barra="", titulo_leyenda=None, figsize=(8, 4), ax=None):
    
    """Crea un gráfico y devuelve (fig, ax).

    Parámetros:
        datos: Serie o DataFrame ya agrupado (el índice son las categorías del eje X).
        tipo: "barras", "barras_horizontales", "barras_apiladas", "lineas" o "mapa_calor".
        titulo, xlabel, ylabel: textos del gráfico.
        colores: color o lista de colores (opcional).
        mostrar_valores: escribe el valor en cada barra o punto (en el mapa de calor siempre se escribe).
        formato: formato de los valores, por ejemplo ".1f" (un decimal).
        mascara: solo mapa de calor. DataFrame de True/False, las celdas True se ocultan.
        etiqueta_barra: solo mapa de calor. Texto de la barra de color.
        titulo_leyenda: título de la leyenda (si hay varias series).
        figsize: tamaño en pulgadas.
        ax: eje donde dibujar. Si no se pasa, se crea una figura nueva. Sirve para hacer
        figuras con varios gráficos (por ejemplo, dos paneles).
    """

   
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure


    if tipo in ("barras", "barras_horizontales", "barras_apiladas"):
        apilado = tipo == "barras_apiladas"
        datos.plot(kind="barh" if tipo == "barras_horizontales" else "bar",
                   stacked=apilado, color=colores, ax=ax, rot=0, legend=False)
        
        if mostrar_valores:
            for contenedor in ax.containers:
                ax.bar_label(contenedor, fmt="{:" + formato + "}",
                             label_type="center" if apilado else "edge")
                
            if not apilado:
                ax.margins(x=0.1) if tipo == "barras_horizontales" else ax.margins(y=0.1)

    elif tipo == "lineas":
        datos = datos.to_frame() if isinstance(datos, pd.Series) else datos
        posiciones = list(range(len(datos)))

        for columna in datos.columns:
            ax.plot(posiciones, datos[columna], marker="o", label=columna)
        
            if mostrar_valores:
                for x, y in zip(posiciones, datos[columna]):
                    ax.annotate(format(y, formato), (x, y), textcoords="offset points",
                                xytext=(0, 8), ha="center")
        ax.set_xticks(posiciones)
        ax.set_xticklabels(datos.index)
        ax.margins(y=0.2)

    elif tipo == "mapa_calor":
        sns.heatmap(datos, annot=True, fmt=formato, mask=mascara, cmap="Blues",
                    cbar_kws={"label": etiqueta_barra}, ax=ax)
        ax.tick_params(axis="y", rotation=0)
        ax.grid(False)

    else:
        print(f"Tipo de gráfico no reconocido: {tipo}")

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if isinstance(datos, pd.DataFrame) and tipo != "mapa_calor" and len(datos.columns) > 1:
        manijas, nombres = ax.get_legend_handles_labels()
        ax.legend(manijas, nombres, title=titulo_leyenda, bbox_to_anchor=(1.02, 1), loc="upper left")
    return fig, ax


def guardar_grafico(fig, nombre, carpeta=v.ruta_imagenes, dpi=150):
    """Guarda una figura como imagen en la carpeta indicada (la crea si no existe).

    Devuelve la ruta del archivo guardado.
    """
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta

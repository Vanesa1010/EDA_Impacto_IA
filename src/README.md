# El impacto de la IA: ¿somos realmente más productivos?

Análisis exploratorio de datos (EDA) sobre el impacto de la IA en la productividad, el bienestar y el aprendizaje, con datos de empleados y de estudiantes. Proyecto individual del módulo Data Analysis del bootcamp.

## Pregunta e hipótesis

**¿Usar IA nos hace más productivos? ¿A qué precio?**

1. Quien usa más IA es más productivo.
2. El uso excesivo de la IA tiene efectos negativos en el bienestar.
3. Los estudiantes que usan más IA sacan mejores notas, pero retienen menos lo aprendido.

## Datos

Tres ficheros de Kaggle que forman dos datasets (todos **sintéticos**, es decir, generados artificialmente):

- **Empleados** (4.500 filas): `ai_productivity_features.csv` y `ai_productivity_targets.csv`, unidos por `Employee_ID`. Uso de IA, hábitos de trabajo, productividad y burnout.
- **Estudiantes** (50.000 filas): `ai_student_impact_dataset.csv`. Uso de IA, notas, retención de habilidades, ansiedad y burnout.

## Resultados principales

| Hipótesis | Resultado |
|---|---|
| 1. Más IA, más productividad | **Se cumple.** La productividad sube de 55,9 a 74,6 entre los que menos y más la usan, con un coste: un 37 % más de errores. |
| 2. Uso excesivo, peor bienestar | **Se cumple solo en estudiantes.** Su burnout alto pasa del 9 % al 56 %. En empleados el burnout depende de la presión de plazos, no de la IA. |
| 3. Mejores notas, pero menos retención | **Se cumple a medias.** El uso alto se asocia con menos retención, pero la nota no mejora con más uso. Importa más cómo se usa la IA que cuánto. |

Al ser datos simulados, los resultados describen un escenario simulado, no evidencia sobre personas reales.

## Tecnologías

Python · pandas · matplotlib · seaborn · Jupyter Notebook

## Estructura del repositorio

```
.
├── README.md
├── presentacion/            # presentación del proyecto
└── src/
    ├── data/                # datasets (CSV)
    ├── img/                 # gráficos generados
    ├── notebooks/
    │   ├── EDA_Impacto_de_la_IA_limpieza.ipynb
    │   ├── EDA_Impacto_de_la_IA_analisis.ipynb
    │   └── EDA_Impacto_de_la_IA_visualizaciones.ipynb
    ├── utils/
    │   ├── funciones.py     # cargar datos, crear tramos, crear y guardar gráficos
    │   ├── variables.py     # rutas y constantes
    │   └── main.py          # genera los gráficos
    └── memoria.ipynb        # resumen de todos los pasos del análisis
```

## Cómo ejecutarlo


- Para leer el proyecto completo, abrir `src/memoria.ipynb` (se ejecuta desde la carpeta `src/`).
- Para regenerar los gráficos: `cd src/utils` y `python main.py`.
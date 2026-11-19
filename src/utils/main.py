import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import funciones as f
import variables as v


sns.set_theme(style="whitegrid")

# --- 1. Cargar y preparar los datos ---
df_empleados = pd.merge(f.cargar_csv(v.ruta_df_features), f.cargar_csv(v.ruta_df_targets), on= v.columna_id)
df_empleados["tramo_ia"] = f.crear_tramos(df_empleados, "ai_tool_usage_hours_per_week", v.tramos)

df_estudiantes = f.cargar_csv(v.ruta_df_estudiantes)
df_estudiantes["tramo_ia"] = f.crear_tramos(df_estudiantes, "Weekly_GenAI_Hours", v.tramos)
df_estudiantes["mejora_nota"] = df_estudiantes["Post_Semester_GPA"] - df_estudiantes["Pre_Semester_GPA"]


# --- 2. H1: productividad por tramo de uso de IA ---
medias = df_empleados.groupby("tramo_ia", observed=True)[["productivity_score", "error_rate_percent"]].mean()

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

f.crear_grafico(medias["productivity_score"], "barras", "Productividad media",
                "Horas de IA a la semana (tramo)", "Puntuación (0-100)", formato=".1f", ax=axes[0])

f.crear_grafico(medias["error_rate_percent"], "barras", "Porcentaje medio de errores",
                "Horas de IA a la semana (tramo)", "Errores (%)", colores="tab:orange", formato=".2f", ax=axes[1])

fig.suptitle("Más horas de IA: más productividad, pero también más errores", fontsize=13)

fig.tight_layout()

f.guardar_grafico(fig, "h1_productividad_errores.png")


# --- 3. H1: mapa de calor por puesto (se ocultan las celdas con menos de 30 personas) ---

pivot = df_empleados.pivot_table(index="job_role", columns="tramo_ia",
                                 values="productivity_score", aggfunc="mean", observed=True)

conteo = pd.crosstab(df_empleados["job_role"], df_empleados["tramo_ia"]).reindex_like(pivot)

fig, _ = f.crear_grafico(pivot, "mapa_calor", "Productividad media por puesto y tramo de horas de IA",
                       "Horas de IA a la semana (tramo)", "Puesto", formato=".1f",
                       mascara=conteo < 30, etiqueta_barra="Productividad media (0-100)", figsize=(8, 5))

f.guardar_grafico(fig, "h1_heatmap_puesto.png")


# --- 4. H2: burnout en empleados, según horas de IA y según presión de plazos (2 paneles) ---

por_tramo = df_empleados.groupby("tramo_ia", observed=True)["burnout_risk_score"].mean()
por_presion = df_empleados.groupby("deadline_pressure_level")["burnout_risk_score"].mean().reindex(["Low", "Medium", "High"])
por_presion.index = ["Baja", "Media", "Alta"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)

f.crear_grafico(por_tramo, "barras", "Según las horas de IA",
                "Tramo de horas de IA", "Burnout medio (0-10)", ax=axes[0])

f.crear_grafico(por_presion, "barras", "Según la presión de plazos",
                "Presión de plazos", colores="tab:red", ax=axes[1])

axes[0].set_ylim(0, 10)

fig.suptitle("En empleados, el burnout cambia con los plazos, no con la IA", fontsize=13)
fig.tight_layout()

f.guardar_grafico(fig, "h2_burnout_empleados.png")


# --- 5. H2: burnout en estudiantes por tramo de uso de IA ---

burnout = pd.crosstab(df_estudiantes["tramo_ia"], df_estudiantes["Burnout_Risk_Level"],
                          normalize="index")[["Low", "Medium", "High"]] * 100

burnout = burnout[["Low", "Medium", "High"]]
burnout.columns = ["Bajo", "Medio", "Alto"]

fig, _ = f.crear_grafico(burnout, "barras_apiladas", "En estudiantes, más horas de IA se asocian a más burnout",
                       "Horas de IA a la semana (tramo)", "% de estudiantes",
                       colores=["tab:green", "gold", "tab:red"], mostrar_valores=False, 
                       titulo_leyenda="Nivel de Burnout", figsize=(8, 4.5))

f.guardar_grafico(fig, "h2_burnout_estudiantes.png")


# --- 6. H3: mejora de nota y retención por tramo de uso de IA (2 paneles)  ---

medias_estudiantes = df_estudiantes.groupby("tramo_ia", observed=True)[["mejora_nota", "Skill_Retention_Score"]].mean()

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

f.crear_grafico(medias_estudiantes["mejora_nota"], "lineas",  "Mejora de nota media (puntos)",
                       "Horas de IA a la semana (tramo)", formato=".3f", ax=axes[0])

f.crear_grafico(medias_estudiantes["Skill_Retention_Score"], "lineas", "Retención de habilidades media",
                "Horas de IA a la semana (tramo)", formato=".1f", ax=axes[1])

fig.suptitle("Con uso alto de IA, la nota no mejora más y cae la retención de habilidades", fontsize=13)
fig.tight_layout()

f.guardar_grafico(fig, "h3_mejora_retencion.png")


# --- 7. H3: mejora de nota según el uso principal de la IA ---

mejora_uso = df_estudiantes.groupby("Primary_Use_Case")["mejora_nota"].mean().sort_values()

fig, _ = f.crear_grafico(mejora_uso, "barras_horizontales", "Pedir respuestas directas a la IA es el uso que menos mejora la nota",
                       "Mejora media de nota (puntos de GPA)", "Tipo de uso principal", formato=".3f")

f.guardar_grafico(fig, "h3_mejora_por_uso.png")

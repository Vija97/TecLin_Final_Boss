# Análisis de los datos

Conclusiones del análisis de datos (hito "Análisis"). Sirven para decidir la limpieza (#7) y las estrategias (#23)
y pasan al notebook final. Cada sección enlaza al notebook donde están las cifras y las gráficas.

> Estas decisiones salen de mirar todo train: la validación cruzada de las variantes que las usen será algo optimista.

## Etiquetas (#20) · [notebook](notebooks/20_vija97_eda_etiquetas.ipynb)

**Hallazgos**

- **No van de 10 en 10** (contra lo que dice el enunciado): el 99 % son enteros de 0 a 100 y solo el ~16 % son múltiplos de 10.
- **No vienen de una única escala:** hay picos fuertes (50, 85, 15, 35…), y 119 usuarios (9 %) tienen los 5 rasgos
  en múltiplos de 5, frente a ~4 que saldrían por azar. Probablemente salen de tests distintos.
- **Distribuciones desplazadas:** apertura hacia arriba (media 63); extraversión, responsabilidad y amabilidad
  hacia abajo (37-43); neuroticismo repartido. Ninguna es uniforme.
- **Rasgos poco relacionados entre sí:** como mucho ±0,26 (neuroticismo frente a responsabilidad y extraversión).
- **Etiquetas vacías:** 35 usuarios, casi siempre un solo rasgo (la mitad de apertura), sin patrón.
- **Referencia:** predecir la media da 30,38; un 50 fijo empeora 1,6 puntos.
- **Las variantes base captan poca señal:** la correlación entre predicción y valor real es de 0,21 a 0,35 (TF-IDF).
  Las predicciones son "tímidas" (±8 frente a ±30), pero es lo óptimo con tan poca señal: recalibrar
  (pendiente ≈ 0,99) o mezclar con la media según el volumen de texto no mejoran.
- **El volumen de texto afecta a la calidad, no al valor:** con >200 posts el error baja claramente, y con 0-50 posts
  (~20 % de los usuarios) TF-IDF no supera a la media. El nº de posts no se relaciona con ningún rasgo.
- **TF-IDF y SBERT fallan en los mismos usuarios** (correlación de errores 0,89); su media simple es peor que TF-IDF sola.

**Implicaciones para la estrategia**

1. Hace falta **señal más fuerte y distinta**, no más de lo mismo: combinar modelos parecidos o estirar las predicciones no ayuda.
2. **Averiguar de dónde salen las etiquetas:** buscar en los posts menciones explícitas de puntuaciones, tests o tipos MBTI (#22). Es la apuesta con más potencial.
3. **Más texto por usuario** (≥ 500 posts) en todas las variantes, sobre todo en SBERT. Para quien escribe poco, solo ayudarán señales explícitas.
4. **Un modelo por rasgo**, con su propio centro y recortado a [0, 100]. No hace falta transformar el objetivo.
5. **Prioridad baja:** modelo conjunto de 5 salidas y tratar las etiquetas vacías.

## Texto: volumen, calidad y ruido (#21)

_Pendiente (IagoVarelaR)._

## Relaciones entre el texto y los rasgos (#22) · [notebook](notebooks/22_vija97_eda_relaciones.ipynb)

**Hallazgos**

- **Tipos MBTI: la señal más fuerte del dataset.** El 23 % de train y el 20 % de test se autoidentifican
  ("I'm an INFJ"), casi siempre con el mismo tipo. Con cualquier mención: 41 % de train y 34 % de test.
- **Cada letra coincide con su rasgo, con diferencias enormes:** extraversión 72,5 (E) frente a 24,3 (I);
  apertura (N/S), amabilidad (F/T) y responsabilidad (J/P) se separan 28-32 puntos; neuroticismo,
  28,5 según el sufijo -T/-A (solo 68 usuarios).
- **Estimación sin trampa:** para los 290 usuarios de train que se autoidentifican, la media del grupo de su letra
  da un RMSE de 25,3 en los 4 rasgos con letra, frente a 29,6 de la media y 27,4 de TF-IDF.
- **Puntuaciones Big Five escritas:** solo el 6-7 % de los usuarios escribe un número junto a un rasgo
  y solo el 11 % coincide con la etiqueta. Las etiquetas no aparecen tal cual en el texto.
- **Palabras asociadas:** débiles (≤ 0,16) pero con sentido psicológico (amabilidad ↔ love/thank frente a palabrotas;
  apertura ↔ philosophy/arguments/artistic; responsabilidad ↔ job/office; extraversión ↔ we/our;
  neuroticismo ↔ anxiety/sorry/terrified). Aparece jerga MBTI.
- **Estilo:** débil (≤ 0,14) pero coherente: "we" con extraversión, "I" y emociones negativas con neuroticismo,
  palabrotas en contra y emociones positivas a favor de la amabilidad.

**Implicaciones para la estrategia**

1. **Prioridad 1: variante MBTI.** Extraer el tipo (autoidentificación y quizá menciones repetidas), sus letras y el
   sufijo -T/-A como features, combinadas con el modelo de texto.
2. **La limpieza (#7) debe conservar las menciones MBTI.**
3. **Features de estilo (#8):** débiles pero coherentes; suman poco y explican mucho (presentación).
4. **Palabras asociadas:** TF-IDF ya las aprovecha, así que no justifican una variante aparte.
5. **Prioridad baja:** extraer puntuaciones Big Five escritas.

## Decisión de estrategias (#23)

_Pendiente: tabla estrategia · evidencia · ganancia esperada · coste · responsable · prioridad._

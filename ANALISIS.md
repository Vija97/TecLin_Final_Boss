# Análisis de los datos

Conclusiones del análisis de datos (hito "Análisis"). Sirven para decidir la limpieza (#7) y las estrategias (#23)
y pasan al notebook final. Cada sección enlaza al notebook donde están las cifras y las gráficas.

> Estas decisiones salen de mirar todo train: la validación cruzada de las variantes que las usen será algo optimista.

## Etiquetas (#20) · [notebook](notebooks/20_vija97_eda_etiquetas.ipynb)

**Hallazgos**

- **No van de 10 en 10** (contra lo que dice el enunciado): el 99 % son enteros de 0 a 100 y solo el ~16 % son múltiplos de 10.
- **No vienen de una única escala:** hay picos fuertes (50, 85, 15, 35…), y 117 usuarios (9 %) tienen los 5 rasgos
  presentes y en múltiplos de 5, frente a ~4 que saldrían por azar. Probablemente salen de tests distintos.
- **Distribuciones desplazadas:** apertura hacia arriba (media 63); extraversión, responsabilidad y amabilidad
  hacia abajo (37-43); neuroticismo repartido. Ninguna es uniforme.
- **Rasgos poco relacionados entre sí:** como mucho ±0,26 (neuroticismo frente a responsabilidad y extraversión).
- **Etiquetas vacías:** 35 usuarios, casi siempre un solo rasgo (la mitad de apertura), sin patrón.
- **Referencia:** predecir la media da 30,38; un 50 fijo empeora 1,6 puntos.
- **Las variantes base captan poca señal:** la correlación entre predicción y valor real es de 0,21 a 0,35 (TF-IDF).
  Las predicciones son "tímidas" (±8 frente a ±30), pero es lo óptimo con tan poca señal: recalibrar
  (pendiente ≈ 0,99, ajustada fuera de cada fold) o mezclar con la media del train de cada fold según el volumen
  de texto no mejoran (comparación de varios `k` exploratoria).
- ⚠️ Las cifras de TF-IDF salen de la PR #19 (commit `c995684`), aún sin fusionar y con cambios pedidos:
  hay que reejecutar el paso 5 del notebook cuando entre la #19 corregida.
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
  apertura (N/S), amabilidad (F/T) y responsabilidad (J/P) se separan 28-32 puntos. El sufijo -T/-A
  (neuroticismo) solo aparece en 9 autoidentificaciones: demasiado pocas para concluir.
- **Estimación sin trampa:** para los 290 usuarios de train que se autoidentifican, la media del grupo de su letra
  da un RMSE de 25,3 en los 4 rasgos con letra, frente a 29,6 de la media y 27,4 de TF-IDF
  (⚠️ esta última, con las predicciones de la PR #19, commit `c995684`; se actualizará cuando entre corregida).
- **Puntuaciones Big Five escritas:** solo el 6-7 % de los usuarios escribe un número junto a un rasgo
  y solo el 11 % coincide con la etiqueta. Las etiquetas no aparecen tal cual en el texto.
- **Palabras asociadas:** débiles (≤ 0,16) pero con sentido psicológico (amabilidad ↔ love/thank frente a palabrotas;
  apertura ↔ philosophy/arguments/artistic; responsabilidad ↔ job/office; extraversión ↔ we/our;
  neuroticismo ↔ anxiety/sorry/terrified). Aparece jerga MBTI.
- **Estilo:** débil (≤ 0,14) pero coherente: "we" con extraversión, "I" y emociones negativas con neuroticismo,
  palabrotas en contra y emociones positivas a favor de la amabilidad.

**Implicaciones para la estrategia**

1. **Prioridad 1: variante MBTI.** Extraer el tipo (autoidentificación y quizá menciones repetidas) y sus 4 letras
   como features, combinadas con el modelo de texto. El sufijo -T/-A, solo si hay suficientes casos.
2. **La limpieza (#7) debe conservar las menciones MBTI.**
3. **Features de estilo (#8):** débiles pero coherentes; suman poco y explican mucho (presentación).
4. **Palabras asociadas:** TF-IDF ya las aprovecha, así que no justifican una variante aparte.
5. **Prioridad baja:** extraer puntuaciones Big Five escritas.

## Decisión de estrategias (#23)

> **Propuesta de Vija97, ajustada con los comentarios de IagoVarelaR (26 nov); pendiente de su aprobación en la PR.** Sale de las secciones #20, #21 (PR #27)
> y #22. Las ganancias son estimaciones exploratorias sobre los mismos folds; la cifra buena será la de cada variante.

**Punto de partida:** TF-IDF word+char 29,18 (validación cruzada) · media 30,41. La señal del texto es débil
(correlación predicción-real 0,2-0,35) y los modelos actuales fallan en los mismos usuarios.

| Prio | Estrategia | Evidencia | Ganancia esperada | Coste | Quién | Issue |
|---|---|---|---|---|---|---|
| **1** | **Variante MBTI:** extraer el tipo autoidentificado (y el más mencionado) y usar sus 4 letras como features junto al TF-IDF | #22: E/I +48 puntos; 20-23 % de usuarios; en ellos 29,6 → 25,3 | **Medida: 29,20 → 28,41 (−0,79)**, mejora en los 5 folds (PR #33) | Bajo (regex + Ridge, sin GPU) | Vija97 | #32 · hecho |
| **2** | **Limpieza (#7):** quitar vacíos y `[deleted]`/`[removed]`, deduplicar dentro de cada usuario, URLs → `URL`, decodificar HTML y normalizar markdown, **conservar menciones MBTI** | #21 (impacto de cada regla) | **Medida en MBTI + TF-IDF: no mejora** (28,41 → 28,44-28,46, ruido; PR #34). No se aplica en TF-IDF; **se prueba en SBERT** | Bajo (ya en `src/limpieza.py`) | IagoVarelaR + Vija97 | #7 |
| **2** | **SBERT con más texto:** primero una prueba de coste con 500 posts por usuario; después, comparar con los 50 de la #5 en los mismos folds (y probar ahí la limpieza) | #20: el error baja con el volumen; la #5 usó 50 posts | Media para SBERT | Medio (GPU) | IagoVarelaR | nueva |
| **2** | **Elegir `alpha` sin trampa** (validación interna) en TF-IDF | Revisión de la #19 | Ninguna; cifra fiable | Bajo | Jesusrf21 | #4 / PR #19 |
| **3** | **Features de estilo y léxicos (#8)** añadidas al modelo de texto | #22: señales ≤ 0,14 pero coherentes | Pequeña; mucho valor para explicar | Bajo (CPU) | Jesusrf21 | #8 |
| **3** | **Combinar variantes (#11)** cuando haya MBTI y estilo | #20: errores actuales correlación 0,89 | Pequeña ahora; más con señales distintas | Bajo (CPU) | Jesusrf21 | #11 |
| 4 | Fine-tuning de un Transformer (#10) | Señal de texto débil; caro | Incierta | Alto (GPU) | IagoVarelaR | #10: solo si sobra tiempo |
| 4 | Cuestionarios + SBERT (#9) | Sin evidencia directa en el análisis | Incierta | Medio | Vija97 | #9: se sustituye por la variante MBTI |
| — | LLM (#13) | — | Incierta | Alto | Vija97 | #13: opcional |

**Descartadas (los datos ya dicen que no ayudan):** estirar o recalibrar las predicciones y mezclarlas con la media
(#20); modelo conjunto de 5 salidas (#20: rasgos poco correlacionados); extraer puntuaciones Big Five escritas
(#22: 6 % de usuarios y ruido); sufijo -T/-A como feature (#22: 9 usuarios); quitar idiomas o posibles bots (#21); quitar citas de otros usuarios
(#34: el dataset no tiene saltos de línea, así que no se puede saber dónde termina una cita).

**Orden de trabajo hasta el envío 2 (1 dic):** MBTI (hecho) y limpieza (medida); SBERT con más texto y `alpha` sin trampa
en paralelo; después, estilo y combinación.

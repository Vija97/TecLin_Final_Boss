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

## Texto: volumen, calidad y ruido (#21) · [notebook](notebooks/21_iago_eda_texto.ipynb)

**Hallazgos**

- **Volumen desigual.** La mediana es de 394 posts por usuario en train y 402 en test. Hay 39 usuarios sin posts (29 en train y 10 en test). El 19,8 % de train y el 22,3 % de test tienen 50 posts o menos.
- **Duplicados.** Hay 306.819 copias extra dentro del mismo usuario (9,82 % de los posts útiles), repartidas entre 1.033 usuarios. Hay también 15.730 textos repetidos entre usuarios, en su mayoría cortos. Una tasa alta de duplicación merece revisión, pero no basta para identificar bots.
- **Ruido de formato.** Hay 53 posts vacíos o con solo espacios, 27 `[deleted]` y 18 `[removed]`. Las URLs aparecen en 166.359 posts (5,32 %) de 1.353 usuarios. El Markdown explícito aparece en 117.436 posts (3,76 %) de 1.088 usuarios.
- **Citas.** El análisis del texto sin decodificar encontró 173 posts de 106 usuarios con una línea que empieza por `&gt;`. En total, 14.897 posts contienen `&gt;` en alguna posición. La segunda cifra mide presencia de la entidad HTML, no citas confirmadas. Falta comprobar la detección tras decodificar el HTML.
- **Idioma.** En una muestra reproducible de 14.967 posts de 1.565 usuarios, el detector clasificó el 97,24 % como inglés, el 1,80 % como no inglés y el 0,96 % como incierto. Son estimaciones sobre la muestra.
- **Volumen y rasgos.** En train, las correlaciones de Spearman entre volumen de texto y rasgos están entre −0,027 y 0,026. El volumen sirve para comparar errores por tramo, pero aquí no muestra una relación monotónica clara con las etiquetas.

**Propuestas para la limpieza (#7)**

1. Quitar posts vacíos y marcadores `[deleted]` y `[removed]`. Probar la deduplicación exacta dentro de cada usuario y medir su efecto, conservando los textos que coincidan entre autores.
2. Probar la sustitución de URLs por un marcador y normalizar HTML y Markdown conservando el texto. Antes de retirar citas, verificar la detección tras decodificar y eliminar solo las líneas identificadas como citas. Conservar las autoidentificaciones MBTI (#22).
3. Mantener por ahora los posts en otros idiomas y los usuarios con tasas altas de duplicación. Aplicar las mismas reglas a train y test.

**Implicaciones para la estrategia (#23)**

- Comparar el error por tramos de volumen y medir el coste de limitar o muestrear posts por usuario.
- Dejar en prioridad baja la mezcla con la media según volumen. La prueba exploratoria del #20 no mejoró TF-IDF. Para los usuarios sin posts, usar la media del train de cada fold como referencia al evaluar alternativas, sin dar por hecho que mejora el modelo.
## Relaciones entre el texto y los rasgos (#22)

_Pendiente (Vija97)._

## Decisión de estrategias (#23)

_Pendiente: tabla estrategia · evidencia · ganancia esperada · coste · responsable · prioridad._

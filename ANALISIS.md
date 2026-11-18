\# Análisis de datos y decisiones



Documento vivo que resume los análisis de #20, #21 y #22 para decidir

la limpieza (#7) y las estrategias (#23).



Las decisiones derivadas de estos análisis se han pensado observando todo

train. Esto puede hacer que la validación posterior sea algo optimista;

debe declararse al evaluar las variantes.



\## #21 · Volumen, calidad y ruido del texto



Notebook: `notebooks/21\_iago\_eda\_texto.ipynb`.



\### Volumen



\- 1.288 usuarios de train y 323 de test.

\- 3.125.358 posts.

\- 39 usuarios sin posts: 29 de train y 10 de test.

\- Mediana de posts: 394 en train y 402 en test.

\- Mediana de caracteres: 83.142 en train y 79.401 en test.

\- Máximo: 66.354 posts y 15.800.496 caracteres en un usuario.

\- Hasta 50 posts: 255 usuarios de train (19,8 %) y 72 de test (22,3 %).

\- Hasta 100 posts: 364 de train (28,3 %) y 105 de test (32,5 %).



Train y test tienen un volumen central parecido. Test contiene algo más

de usuarios con poco texto y train tiene una cola más extrema.



\### Calidad y ruido



| Señal | Posts afectados | Usuarios afectados | Conclusión |

|---|---:|---:|---|

| Vacíos o solo espacios | 53 | 28 | Eliminar |

| `\[deleted]` | 27 | 16 | Eliminar |

| `\[removed]` | 18 | 11 | Eliminar |

| URLs | 166.359 (5,32 %) | 1.353 | Sustituir URL y conservar texto |

| Markdown explícito | 117.436 (3,76 %) | 1.088 | Normalizar marcas y conservar texto |

| Citas que empiezan por `\&gt;` | 173 | 106 | Decodificar HTML y eliminar solo la línea citada |

| Copias exactas extra dentro del usuario | 306.819 (9,82 % de posts útiles) | 1.033 | Deduplicar dentro del usuario |



Los duplicados internos aparecen en todos los tamaños: más de la mitad

de las copias extra supera 50 caracteres y 7.374 superan 1.000. No son

solo respuestas breves.



No se recomienda deduplicar entre usuarios: casi todos los textos

compartidos por personas distintas tienen 25 caracteres o menos y

parecen respuestas genéricas legítimas.



La duplicación está concentrada. La mediana por usuario es 0,58 %, pero

253 usuarios superan el 10 %, 101 superan el 25 % y cinco superan el

50 %. Estos últimos son posibles casos automatizados, aunque la

duplicación por sí sola no demuestra que sean bots.



\### Idioma



Se analizaron 14.967 posts, con hasta 10 textos de al menos 50 caracteres

por usuario:



\- 97,24 %: inglés seguro.

\- 1,80 %: no inglés seguro.

\- 0,96 %: incierto.

\- 16 usuarios parecen escribir principalmente en otro idioma.

\- 46 usuarios no tienen una muestra suficientemente larga.



Es una estimación muestral con `langdetect`. No se recomienda eliminar

texto o usuarios por idioma.



\### Volumen frente a rasgos



Las correlaciones de Spearman entre `log(posts + 1)` o

`log(caracteres + 1)` y los cinco rasgos están entre -0,027 y 0,026.

Todos los valores p exploratorios son superiores a 0,33.



No hay evidencia de que el volumen indique si un rasgo debe predecirse

más alto o más bajo. Puede servir como medida de confianza.



\### Reglas propuestas para #7



1\. Eliminar vacíos, `\[deleted]` y `\[removed]`.

2\. Deduplicar textos exactos dentro de cada usuario, conservando una copia.

3\. No deduplicar automáticamente entre usuarios.

4\. Sustituir URLs por un token `URL`.

5\. Decodificar entidades HTML y normalizar markdown conservando el texto.

6\. Eliminar únicamente líneas citadas que comiencen por `>`.

7\. Conservar textos no ingleses.

8\. No eliminar posibles bots sin evidencia adicional; deduplicar reduce su peso.

9\. Aplicar exactamente la misma limpieza a train y test.



\### Implicaciones candidatas para #23



| Evidencia | Estrategia sugerida | Coste | Prioridad provisional |

|---|---|---:|---|

| 39 usuarios sin posts | Predicción de respaldo basada en la media | Bajo | Alta |

| 20–22 % tiene como máximo 50 posts | Mezclar con la media según volumen | Bajo | Alta |

| Volumen sin correlación con rasgos | Usarlo como confianza, no como dirección | Bajo | Alta |

| Cola de hasta 66.354 posts | Comparar límites de posts por usuario | Medio | Alta |

| 9,82 % de copias exactas internas | Evaluar modelos tras deduplicación | Medio | Alta |

| URLs y markdown frecuentes | Comparar texto normalizado frente a original | Medio | Media |

| Solo 1,80 % no inglés en la muestra | Mantener inglés como enfoque principal | Bajo | Media |

| Cinco usuarios con >50 % duplicado | Análisis de sensibilidad, sin excluirlos directamente | Bajo | Media |



\### Limitaciones



\- El idioma se estimó con una muestra, no con todos los posts.

\- Los posibles bots se identificaron únicamente mediante repetición exacta.

\- No se imprimieron textos completos ni nombres reales en el notebook.

\- Las propuestas deben confirmarse con la validación cruzada común.

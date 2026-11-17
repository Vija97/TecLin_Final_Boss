Closes #<!-- número de la Issue -->

## Qué cambia

<!-- Una o dos frases. -->

## Tipo

- [ ] Experimento (notebook propio + `EXPERIMENTOS.md` + `predicciones/`): lo puede fusionar el autor
- [ ] Código común (`src/`, `AGENTS.md`, skills, `.github/`): **necesita la aprobación de otra persona**
- [ ] Envío (`submissions/`)

## Resultado

<!-- RMSE medio de validación cruzada y diferencia con la mejor variante, o "no aplica". -->

## Comprobaciones

- [ ] La cifra sale de `validacion_cruzada` y coincide con `EXPERIMENTOS.md`
- [ ] Sin fuga de etiquetas; ajustes sin etiquetas con textos de val/test declarados
- [ ] Predicciones guardadas con `guardar_predicciones` (si es una variante)
- [ ] Notebook ejecutado de arriba abajo y guardado con salidas
- [ ] Sin datos, parquet, embeddings ni claves en el commit

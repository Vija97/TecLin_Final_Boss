# Origen

- Fuente: https://github.com/K-Dense-AI/scientific-agent-skills/tree/ec59a29/skills/scikit-learn
- Commit: `ec59a29` (copiado el 2026-11-17)
- Licencia: MIT del repositorio (`LICENSE.md`); la skill declara además la suya en el frontmatter.
- Cambios respecto al original:
  - Añadida la cabecera "Reglas de TecLin" al principio de `SKILL.md`.
  - Quitado `allowed-tools` del frontmatter (no concede permisos extra a los agentes).
  - No se copian `scripts/` (ejemplos con datos sintéticos que no hacen falta aquí).
- Revisado: sin código que haga peticiones de red, ejecute comandos ocultos ni texto oculto.
  Solo aparece `push_to_hub` como documentación, prohibido por la cabecera.

Para actualizarla: volver a copiar desde un commit nuevo, revisar el diff y mantener estos cambios.

---
name: plazos-digemid
description: Calcula el día cero y la fecha límite para notificar sospechas de reacciones adversas a DIGEMID (Perú) y revisa si una lista de casos se notificó a tiempo. Úsala cuando el usuario pregunte "hasta cuándo tengo para notificar", "día cero", "plazo de notificación", "caso grave en 24 horas", o suba una lista de casos para verificar cumplimiento de plazos.
---

# Plazos de notificación a DIGEMID

## Reglas que aplica

- **Día cero:** fecha en que cualquier persona de la organización recibe un caso con la información
  mínima: un notificador identificable, un paciente identificable (iniciales, edad o sexo bastan),
  un medicamento sospechoso y una reacción adversa.
- **Graves:** dentro de las 24 horas de conocido el caso. Es grave si produce muerte, amenaza la vida,
  requiere o prolonga la hospitalización, causa discapacidad o incapacidad persistente o significativa,
  anomalía congénita, o es médicamente importante.
- **Leves o moderadas (no graves):** hasta 20 días calendario.

Estos valores vienen del instructivo del formato de notificación de DIGEMID para titulares de registro
sanitario. Son parámetros del script (`--horas-grave`, `--dias-no-grave`): si el usuario cita otra
norma o un plazo distinto para su tipo de establecimiento, usa el suyo.

## Calcular

Desde la carpeta de esta skill:

```bash
python3 scripts/plazos.py --dia-cero "2026-10-20 15:30" --grave si
python3 scripts/plazos.py --csv casos.csv     # caso_id, dia_cero, grave[, fecha_notificacion]
```

## Entregar

1. Primero determina el día cero con el usuario si no está claro (el día en que se tuvo la información
   mínima, no el día en que se completó el formulario).
2. Clasifica la gravedad con los criterios de arriba y di en una línea por qué.
3. Muestra la fecha y hora límite, y si ya venció.
4. Para listas: tabla con el estado de cada caso y un conteo de a tiempo, tardíos y pendientes.

Recuerda que una notificación tardía igual debe enviarse, documentando la causa del retraso.

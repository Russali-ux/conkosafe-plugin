---
name: detectar-senales
description: Detecta señales de farmacovigilancia por desproporcionalidad (PRR, ROR, IC/BCPNN) en una base de notificaciones espontáneas o en una tabla 2x2. Úsala cuando el usuario suba un CSV o Excel de notificaciones de RAM/ICSR, pida "buscar señales", "calcular PRR o ROR", "análisis de desproporcionalidad", o quiera saber si un par medicamento-evento se notifica más de lo esperado.
---

# Detectar señales por desproporcionalidad

## Preparar los datos

El script necesita un CSV con **una fila por par fármaco-evento de cada caso** y las columnas
`caso_id`, `farmaco`, `evento`. Si el usuario trae otro formato (Excel, una fila por caso con varios
fármacos separados por comas, columnas con otros nombres), conviértelo primero a ese formato con un
script corto y muestra al usuario cuántos casos y pares quedaron. Unifica la escritura de fármacos
(principio activo, sin marca) y de eventos (término preferido MedDRA si lo tiene) antes de contar.

## Calcular

Desde la carpeta de esta skill:

```bash
python3 scripts/desproporcionalidad.py --csv icsr.csv --min-a 3 --salida resultados.csv
python3 scripts/desproporcionalidad.py --a 20 --b 380 --c 200 --d 9400      # tabla 2x2 ya contada
python3 scripts/desproporcionalidad.py --csv icsr.csv --verdad verdad.csv    # medir desempeño
```

| Método | Criterio de señal |
|---|---|
| PRR (Evans 2001) | a ≥ 3, PRR ≥ 2 y χ² con Yates ≥ 4 |
| ROR | a ≥ 3 y límite inferior del IC 95 % > 1 |
| IC / BCPNN (aproximación de Norén 2013) | IC025 > 0 |

`a` = casos con el fármaco y el evento; `b` = con el fármaco y otro evento; `c` = con el evento y otro
fármaco; `d` = el resto.

## Entregar

1. Tabla de pares con señal en al menos un método, ordenada por número de métodos y por IC025.
2. Para cada señal: `a`, esperado, los tres estimadores con su intervalo y una línea de lectura.
3. Advertencias que apliquen: pocos casos (`a` < 5), notoriedad o efecto de estimulación (noticias,
   alertas), confusión por indicación, duplicados, enmascaramiento por un fármaco muy notificado.
4. Si se usó `--verdad`, la tabla de sensibilidad, especificidad y VPP por método.

Termina siempre recordando que una señal estadística es una hipótesis que requiere evaluación clínica
(revisión de casos, plausibilidad, literatura) antes de cualquier acción regulatoria.

---
name: laboratorio-ram
description: Laboratorio de farmacovigilancia con datos simulados y verdad conocida - genera una cohorte sintética, siembra un riesgo relativo para un par fármaco-evento, simula la subnotificación y mide si los métodos de señal lo recuperan. Úsala para formación, para practicar detección de señales, o cuando el usuario pida "simular casos de RAM", "datos de prueba de farmacovigilancia", "validar un algoritmo de señales" o "ver cuánto afecta la subnotificación".
---

# Laboratorio de RAM con verdad conocida

Todo lo que produce esta skill es **ficticio**. Etiqueta cada tabla, gráfico o archivo que entregues con
**DATOS SIMULADOS** y no lo presentes como evidencia sobre productos reales.

## Correr una simulación

Desde la carpeta de esta skill:

```bash
python3 scripts/simular.py --salida salidas/corrida1 --semilla 42
```

Parámetros principales (todos opcionales):

| Parámetro | Por defecto | Qué controla |
|---|---|---|
| `--n` | 100 000 | Personas en la cohorte |
| `--rr` | 4 | RR sembrado para FAR-01 → EVT-01 (el resto tiene RR 1: controles negativos) |
| `--tasa-objetivo` | 300 | Tasa basal del evento objetivo por 100 000 personas-año |
| `--tasa-fondo` | 3 000 | Tasa basal de los demás eventos |
| `--prob-exposicion` | 0,30 | Probabilidad de recibir cada fármaco |
| `--duracion` / `--ventana` | 60 / 30 | Días de tratamiento y de riesgo posterior |
| `--fraccion-notificada` / `--fraccion-notificada-grave` | 0,20 / 0,40 | Subnotificación |
| `--semilla` | 42 | Reproducibilidad: misma semilla, mismos datos |

El script escribe `icsr.csv` (base de notificaciones), `verdad.csv` (lo sembrado), `cohorte.csv`
(IRR de la cohorte completa) y `LEEME.txt` (parámetros).

## Medir si las señales se recuperan

Usa el script de la skill `detectar-senales` del mismo plugin (carpeta hermana de esta):

```bash
python3 ../detectar-senales/scripts/desproporcionalidad.py \
  --csv salidas/corrida1/icsr.csv --verdad salidas/corrida1/verdad.csv --solo-senales
```

## Ejercicios sugeridos

- **Subnotificación:** repetir con `--fraccion-notificada 0.05` y comparar sensibilidad.
- **Tamaño del efecto:** variar `--rr` entre 1,5 y 6 y ver desde qué valor aparece la señal.
- **Variabilidad:** correr 5–20 semillas y resumir cuántas veces cada método detecta el par sembrado
  y cuántos falsos positivos da (VPP).
- **Cohorte frente a notificación:** comparar el IRR de `cohorte.csv` con el PRR/ROR de las
  notificaciones.

## Entregar

Resumen de parámetros, tabla del IRR de la cohorte, tabla de desempeño por método y 2–3 conclusiones.
Advierte que el laboratorio mide la capacidad de recuperar su propio modelo (circularidad): para validar
un algoritmo para uso real hace falta además validación externa con datos reales y protocolo aprobado.

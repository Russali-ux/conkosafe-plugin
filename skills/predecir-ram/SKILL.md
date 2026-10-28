---
name: predecir-ram
description: Proyecta cuántas reacciones adversas y cuántas notificaciones cabe esperar en un periodo futuro, con intervalo de confianza, a partir de los eventos observados y la exposición (modelo Gamma-Poisson). Úsala cuando el usuario pregunte "cuántas RAM esperamos el próximo año", "proyectar notificaciones", "tasa de RAM por pacientes expuestos" o quiera planificar la carga de trabajo de farmacovigilancia.
---

# Predecir RAM futuras

## Datos que necesitas

- **Eventos observados** (x) y la **exposición** en la que ocurrieron (pacientes-año, pacientes-mes,
  tratamientos, unidades vendidas convertidas a pacientes). Pide la unidad si no está clara.
- **Exposición futura** esperada en la misma unidad (p. ej., ventas proyectadas).
- Opcional: **fracción notificada** (q) si quieren proyectar notificaciones y no eventos. Como referencia
  publicada, Hazell y Shakir (2006) estiman una mediana de subnotificación de ~94 % (q ≈ 0,06); si el
  usuario tiene un dato propio, usa el suyo.

## Calcular

Desde la carpeta de esta skill:

```bash
python3 scripts/prediccion.py --eventos 12 --exposicion 8000 --exposicion-futura 10000 \
  --fraccion-notificada 0.06 --unidad "pacientes-año"
```

El modelo usa una previa Gamma vaga (α0 = 0,5, β0 = 0); con x eventos en E la tasa tiene posterior
Gamma(α0 + x, β0 + E) y los eventos futuros siguen una binomial negativa. Con `--alfa0` y `--beta0` se
puede incorporar una tasa previa de la literatura (β0 = exposición equivalente, α0 = tasa × β0).

## Entregar

Tabla con media, mediana e IC 95 % para eventos totales y, si aplica, notificaciones esperadas; la tasa
por 1 000 unidades; y los supuestos (tasa constante, exposición futura conocida, sin cambios de
indicación ni de población). Con pocos eventos (x < 5) advierte que el intervalo es muy ancho.

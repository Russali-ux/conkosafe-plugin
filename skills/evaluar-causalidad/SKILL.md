---
name: evaluar-causalidad
description: Evalúa la causalidad de una sospecha de reacción adversa a medicamento (RAM) con el algoritmo de Naranjo y los criterios OMS-UMC. Úsala cuando el usuario describa un caso de RAM, pregunte si un medicamento causó un evento, pida "aplicar Naranjo", "evaluar causalidad", "imputabilidad" o clasificar un caso como probable, posible o dudoso.
---

# Evaluar causalidad de una sospecha de RAM

## Flujo

1. **Reúne los datos del caso** que el usuario dio: medicamento(s) sospechoso(s) y concomitantes, evento,
   fechas de inicio del tratamiento y del evento, retirada (dechallenge), reexposición (rechallenge),
   causas alternativas (enfermedad de base, otros fármacos), pruebas objetivas y antecedentes.
   Si falta información clave para varias preguntas, pregunta una sola vez por lo que falte; lo que no se
   sepa se responde "nose" (0 puntos), nunca se inventa.
2. **Responde las 10 preguntas de Naranjo** con `si`, `no` o `nose`, justificando cada respuesta con un
   dato del caso.
3. **Calcula** con el script de esta skill (no sumes a mano):

   ```bash
   python3 scripts/naranjo.py --respuestas si,si,nose,nose,no,nose,nose,nose,nose,si
   ```

   El script está en la carpeta de esta skill. Devuelve la tabla con puntos por pregunta, el total y la
   categoría (≥ 9 definida · 5–8 probable · 1–4 posible · ≤ 0 dudosa).
4. **Contrasta con OMS-UMC** (cierta, probable, posible, improbable, condicional/no clasificada,
   inevaluable) y explica en una línea si ambas escalas coinciden o por qué difieren.
5. **Entrega**: tabla de Naranjo, categoría OMS-UMC, los datos que cambiarían la conclusión
   (p. ej., "una reexposición positiva subiría el caso a definida") y la recomendación de revisión
   por el profesional responsable de farmacovigilancia.

## Criterios OMS-UMC (resumen)

| Categoría | Relación temporal | Otras causas | Retirada | Reexposición |
|---|---|---|---|---|
| Cierta | Plausible | Descartadas | Respuesta plausible | Positiva (si procede) |
| Probable | Razonable | Improbables | Respuesta clínica razonable | No necesaria |
| Posible | Razonable | Podrían explicarlo | Falta o no clara | — |
| Improbable | Improbable | Explicación más plausible | — | — |
| Condicional | Se necesitan más datos | | | |
| Inevaluable | Información insuficiente o contradictoria | | | |

## Límites

- La evaluación es una ayuda para el profesional; no reemplaza el juicio clínico ni la evaluación oficial
  del titular o de la autoridad.
- Nunca pidas ni registres nombres, documentos de identidad u otros datos que identifiquen al paciente:
  usa iniciales, edad y sexo.

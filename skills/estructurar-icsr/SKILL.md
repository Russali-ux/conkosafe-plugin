---
name: estructurar-icsr
description: Ordena la información de una sospecha de reacción adversa en la estructura de un ICSR (campos clave de ICH E2B(R3)), verifica los cuatro criterios mínimos de un caso válido y redacta la narrativa clínica. Úsala cuando el usuario pegue un correo, llamada, nota o formulario con un caso de RAM y pida "armar el caso", "redactar la narrativa", "qué falta para notificar" o "llenar el reporte".
---

# Estructurar un ICSR y su narrativa

## 1. Validez del caso

Confirma los cuatro criterios mínimos y di cuál falta, si alguno:

1. Notificador identificable (profesión o contacto; no hace falta el nombre completo).
2. Paciente identificable (iniciales, edad o grupo etario, o sexo).
3. Al menos un medicamento sospechoso.
4. Al menos una reacción o evento adverso.

Sin los cuatro no hay día cero: indica qué pedir al notificador.

## 2. Campos del caso

Llena esta tabla solo con datos dados por el usuario; deja "No informado" donde no haya dato.

| Sección (E2B(R3)) | Campo |
|---|---|
| C. Identificación | Tipo de notificación, fecha de recepción inicial (día cero), fecha de la información más reciente |
| C.2 Notificador | Profesión, país |
| D. Paciente | Iniciales, edad, sexo, peso, talla, antecedentes relevantes |
| E. Reacción | Término informado, término MedDRA (PT) si se conoce, inicio, fin, desenlace, criterios de gravedad |
| F. Pruebas | Resultados con fecha y unidades |
| G. Medicamentos | Rol (sospechoso, concomitante, interactuante), principio activo, dosis, vía, inicio, fin, indicación, lote, acción tomada (retirada, reducción, sin cambio) |
| H. Narrativa | Texto clínico y comentarios del evaluador |

No inventes códigos MedDRA: si el usuario no tiene licencia o no da el término, deja el término
informado y marca "Codificación MedDRA pendiente".

## 3. Narrativa

Redacta en tercera persona, orden cronológico y en un solo bloque:

> Paciente [sexo] de [edad] años, con antecedente de [...], que recibió [medicamento, dosis, vía] desde
> [fecha] por [indicación]. El [fecha / día N de tratamiento] presentó [reacción], con [hallazgos]. Se
> [acción con el medicamento]. Evolución: [desenlace y fecha]. Medicación concomitante: [...].

Termina con un párrafo separado "Comentario del evaluador" solo si el usuario pide valoración; para
causalidad usa la skill `evaluar-causalidad` del mismo plugin y para el plazo `plazos-digemid`.

## Privacidad

Usa solo iniciales del paciente. Si el texto pegado trae nombres completos, DNI, direcciones o
teléfonos del paciente, reemplázalos por iniciales y avisa al usuario que los quitaste.

# ConkoSafe Farmacovigilancia

Herramientas de farmacovigilancia en español para profesionales de la salud, responsables de
farmacovigilancia de laboratorios y droguerías, y docentes. Pensado para el marco peruano (DIGEMID),
útil en cualquier país de habla hispana.

*Spanish-language pharmacovigilance toolkit: Naranjo causality, disproportionality signal detection
(PRR, ROR, IC), Peruvian DIGEMID reporting deadlines, ICSR structuring and a simulated adverse-reaction
lab with known ground truth. Everything runs locally with the Python standard library.*

## Qué incluye

| Skill | Para qué sirve |
|---|---|
| `evaluar-causalidad` | Algoritmo de Naranjo y criterios OMS-UMC para una sospecha de RAM |
| `detectar-senales` | PRR, ROR e IC/BCPNN sobre una base de notificaciones o una tabla 2x2 |
| `plazos-digemid` | Día cero y fecha límite de notificación (graves 24 h, no graves 20 días calendario) |
| `estructurar-icsr` | Criterios mínimos, campos clave de ICH E2B(R3) y narrativa clínica |
| `laboratorio-ram` | Cohorte simulada con riesgo sembrado y subnotificación, para formación y validación |
| `predecir-ram` | Proyección Gamma-Poisson de eventos y notificaciones futuras con IC 95 % |

## Instalación

Desde el directorio de Claude (claude.ai → Directorio → Plugins), o en Claude Code:

```
/plugin install conkosafe --marketplace Russali-ux/conkosafe-plugin   # o: /plugin marketplace add Russali-ux/conkosafe-plugin
```

## Cómo usarlo

Pídele a Claude cosas como:

- "Aplica Naranjo a este caso: …"
- "Busca señales en este CSV de notificaciones."
- "Recibimos un caso grave ayer a las 4 p. m., ¿hasta cuándo tengo para notificar?"
- "Arma el ICSR y la narrativa de este correo."
- "Simula 100 000 pacientes con un RR de 3 y dime si el PRR lo detecta."
- "Con 12 casos en 8 000 pacientes-año, ¿cuántos esperamos el próximo año?"

Los cálculos los hacen scripts de Python incluidos en cada skill (`skills/<skill>/scripts/`), con la
librería estándar, sin dependencias que instalar.

## Datos y privacidad

- El plugin **no se conecta a ningún servidor, no llama a APIs externas y no guarda datos**. Los scripts
  leen los archivos que el usuario les da y escriben los resultados en la carpeta que indique.
- No incluye conectores MCP ni hooks.
- Las skills piden usar solo iniciales del paciente y quitan identificadores si aparecen.
- Todo lo que genera `laboratorio-ram` es ficticio y va marcado como **DATOS SIMULADOS**.

## Límites

Es una ayuda para el trabajo profesional, no un sistema validado (GAMP 5) ni sustituye la evaluación
del responsable de farmacovigilancia ni la normativa vigente. Los plazos de notificación son
parámetros: verifícalos contra la norma que aplique a tu establecimiento. Una señal estadística es una
hipótesis que requiere evaluación clínica.

## Referencias

Naranjo CA et al. Clin Pharmacol Ther 1981;30:239-45 · Evans SJW et al. Pharmacoepidemiol Drug Saf
2001;10:483-6 · Bate A et al. Eur J Clin Pharmacol 1998;54:315-21 · Norén GN et al. Stat Methods Med
Res 2013;22:57-69 · Hazell L, Shakir SAW. Drug Saf 2006;29:385-96 · ICH E2B(R3).

## Licencia y autor

MIT. Desarrollado por Conkomerco S.A.C. (Lima, Perú) como parte de ConkoSafe IA.

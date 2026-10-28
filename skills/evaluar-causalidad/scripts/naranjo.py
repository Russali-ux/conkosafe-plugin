#!/usr/bin/env python3
"""Algoritmo de Naranjo (Naranjo et al., Clin Pharmacol Ther 1981;30:239-245).

Uso:
  python3 naranjo.py --respuestas si,si,nose,no,no,nose,nose,nose,nose,si
  python3 naranjo.py --json respuestas.json      # {"1": "si", "2": "no", ...}

Cada respuesta es: si | no | nose (no se sabe / no aplica).
Solo usa la librería estándar. No envía datos a ningún lado.
"""
import argparse
import json
import sys

PREGUNTAS = [
    # (texto, puntos si, puntos no, puntos no se sabe)
    ("¿Existen notificaciones concluyentes previas sobre esta reacción?", 1, 0, 0),
    ("¿La reacción apareció después de administrar el medicamento sospechoso?", 2, -1, 0),
    ("¿La reacción mejoró al suspender el medicamento o al dar un antagonista específico?", 1, 0, 0),
    ("¿La reacción reapareció al readministrar el medicamento?", 2, -1, 0),
    ("¿Existen causas alternativas (distintas del medicamento) que puedan explicar la reacción?", -1, 2, 0),
    ("¿La reacción reapareció al administrar un placebo?", -1, 1, 0),
    ("¿Se detectó el medicamento en sangre u otros fluidos en concentraciones tóxicas?", 1, 0, 0),
    ("¿La reacción fue más intensa al aumentar la dosis o menos al disminuirla?", 1, 0, 0),
    ("¿El paciente tuvo una reacción similar con el mismo medicamento o uno parecido?", 1, 0, 0),
    ("¿Se confirmó el acontecimiento adverso con alguna evidencia objetiva?", 1, 0, 0),
]

NORMALIZA = {
    "si": "si", "sí": "si", "s": "si", "yes": "si", "y": "si", "1": "si",
    "no": "no", "n": "no", "0": "no",
    "nose": "nose", "no se": "nose", "no sé": "nose", "ns": "nose", "na": "nose",
    "no aplica": "nose", "desconocido": "nose", "?": "nose", "": "nose",
}


def categoria(puntaje: int) -> str:
    if puntaje >= 9:
        return "Definida"
    if puntaje >= 5:
        return "Probable"
    if puntaje >= 1:
        return "Posible"
    return "Dudosa"


def evaluar(respuestas):
    if len(respuestas) != 10:
        raise ValueError(f"Se esperaban 10 respuestas y llegaron {len(respuestas)}.")
    detalle, total = [], 0
    for i, (r, (texto, p_si, p_no, p_ns)) in enumerate(zip(respuestas, PREGUNTAS), start=1):
        clave = NORMALIZA.get(str(r).strip().lower())
        if clave is None:
            raise ValueError(f"Respuesta no reconocida en la pregunta {i}: {r!r} (usa si / no / nose)")
        puntos = {"si": p_si, "no": p_no, "nose": p_ns}[clave]
        total += puntos
        detalle.append({"n": i, "pregunta": texto, "respuesta": clave, "puntos": puntos})
    return {"puntaje": total, "categoria": categoria(total), "detalle": detalle}


def main():
    ap = argparse.ArgumentParser(description="Algoritmo de Naranjo")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--respuestas", help="10 respuestas separadas por coma: si,no,nose,...")
    g.add_argument("--json", help="Archivo JSON con las respuestas (lista o dict 1..10)")
    ap.add_argument("--formato", choices=["texto", "json"], default="texto")
    a = ap.parse_args()

    if a.respuestas:
        resp = [x for x in a.respuestas.split(",")]
    else:
        with open(a.json, encoding="utf-8") as f:
            datos = json.load(f)
        resp = [datos[str(i)] for i in range(1, 11)] if isinstance(datos, dict) else datos

    try:
        res = evaluar(resp)
    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    if a.formato == "json":
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print("| # | Pregunta | Respuesta | Puntos |")
    print("|---|---|---|---|")
    for d in res["detalle"]:
        print(f"| {d['n']} | {d['pregunta']} | {d['respuesta']} | {d['puntos']:+d} |")
    print(f"\nPuntaje total: {res['puntaje']}  →  Categoría: {res['categoria']}")
    print("Escala: ≥9 definida · 5–8 probable · 1–4 posible · ≤0 dudosa")


if __name__ == "__main__":
    main()

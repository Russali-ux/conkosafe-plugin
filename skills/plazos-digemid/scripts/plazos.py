#!/usr/bin/env python3
"""Calcula la fecha límite de notificación de una sospecha de RAM a partir del día cero.

Plazos por defecto (instructivo del formato de notificación de DIGEMID para titulares de
registro sanitario): graves dentro de 24 horas de conocido el caso; leves o moderadas
dentro de 20 días calendario. Son parámetros: verifícalos contra la norma vigente.

Uso:
  python3 plazos.py --dia-cero "2026-10-20 15:30" --grave si
  python3 plazos.py --dia-cero 2026-10-20 --grave no --hoy 2026-11-12
  python3 plazos.py --csv casos.csv     # columnas: caso_id, dia_cero, grave [, fecha_notificacion]

Solo usa la librería estándar. No envía datos a ningún lado.
"""
import argparse
import csv
import sys
from datetime import datetime, timedelta

SI = {"si", "sí", "s", "yes", "y", "1", "true", "grave"}


def leer_fecha(texto: str) -> datetime:
    texto = texto.strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            pass
    raise ValueError(f"Fecha no reconocida: {texto!r} (usa AAAA-MM-DD [HH:MM] o DD/MM/AAAA)")


def limite(dia_cero: datetime, grave: bool, horas_grave: int, dias_no_grave: int,
           con_hora: bool) -> datetime:
    if grave:
        return dia_cero + timedelta(hours=horas_grave)
    fin = dia_cero + timedelta(days=dias_no_grave)
    # Plazo en días calendario: vence al terminar el día.
    return fin.replace(hour=23, minute=59) if not con_hora else fin


def estado(lim: datetime, notificado: datetime | None, hoy: datetime) -> str:
    if notificado:
        return "A tiempo" if notificado <= lim else f"Tardía ({fmt_delta(notificado - lim)} después)"
    if hoy > lim:
        return f"VENCIDO hace {fmt_delta(hoy - lim)}"
    return f"Pendiente: quedan {fmt_delta(lim - hoy)}"


def fmt_delta(d: timedelta) -> str:
    horas = int(d.total_seconds() // 3600)
    return f"{horas} h" if horas < 48 else f"{horas // 24} d {horas % 24} h"


def main():
    ap = argparse.ArgumentParser(description="Plazos de notificación de RAM (DIGEMID)")
    ap.add_argument("--dia-cero", help="Fecha (y hora) en que se conoció el caso con la información mínima")
    ap.add_argument("--grave", help="si / no")
    ap.add_argument("--notificado", help="Fecha en que se notificó (opcional)")
    ap.add_argument("--csv", help="CSV con caso_id, dia_cero, grave [, fecha_notificacion]")
    ap.add_argument("--hoy", help="Fecha de referencia (por defecto, ahora)")
    ap.add_argument("--horas-grave", type=int, default=24)
    ap.add_argument("--dias-no-grave", type=int, default=20)
    a = ap.parse_args()

    hoy = leer_fecha(a.hoy) if a.hoy else datetime.now()
    filas = []
    try:
        if a.csv:
            with open(a.csv, encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    filas.append((r.get("caso_id", ""), r["dia_cero"], r["grave"],
                                  r.get("fecha_notificacion") or None))
        elif a.dia_cero and a.grave:
            filas.append(("caso", a.dia_cero, a.grave, a.notificado))
        else:
            ap.error("Indica --dia-cero y --grave, o --csv")

        print("| Caso | Día cero | Gravedad | Fecha límite | Estado |")
        print("|---|---|---|---|---|")
        for caso, dc, gr, notif in filas:
            d0 = leer_fecha(dc)
            grave = gr.strip().lower() in SI
            con_hora = ":" in dc
            lim = limite(d0, grave, a.horas_grave, a.dias_no_grave, con_hora)
            n = leer_fecha(notif) if notif else None
            print(f"| {caso} | {d0:%Y-%m-%d %H:%M} | {'Grave' if grave else 'No grave'} | "
                  f"{lim:%Y-%m-%d %H:%M} | {estado(lim, n, hoy)} |")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"\nPlazos usados: graves {a.horas_grave} h; no graves {a.dias_no_grave} días calendario. "
          "Verificar contra la norma DIGEMID vigente.")


if __name__ == "__main__":
    main()

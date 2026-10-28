#!/usr/bin/env python3
"""Laboratorio de RAM con verdad conocida (DATOS SIMULADOS).

Genera una cohorte sintética, expone a cada persona a varios fármacos, produce eventos de
fondo y siembra un riesgo relativo (RR) conocido para un par fármaco-evento. Luego simula
la notificación espontánea (subnotificación) y escribe:

  icsr.csv     caso_id, farmaco, evento, grave, fecha       (base de notificaciones)
  verdad.csv   farmaco, evento, rr                          (lo que se sembró)
  cohorte.csv  farmaco, evento, eventos_expuestos, pt_expuesto_anios,
               eventos_no_expuestos, pt_no_expuesto_anios, irr   (cohorte completa)

Uso:
  python3 simular.py --salida salidas/corrida1 --semilla 42
  python3 simular.py --n 50000 --rr 4 --tasa-objetivo 50 --fraccion-notificada 0.2 --salida ...

Solo usa la librería estándar. No envía datos a ningún lado. Todo lo que produce es ficticio.
"""
import argparse
import csv
import math
import os
import random

AVISO = "DATOS SIMULADOS — no representan pacientes ni productos reales"


def poisson(rng, lam):
    if lam <= 0:
        return 0
    if lam > 30:  # aproximación normal para tasas altas
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    l, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= l:
            return k
        k += 1


def main():
    ap = argparse.ArgumentParser(description="Simulador de RAM con verdad conocida")
    ap.add_argument("--salida", required=True, help="Carpeta donde escribir los CSV")
    ap.add_argument("--semilla", type=int, default=42)
    ap.add_argument("--n", type=int, default=100000, help="Personas en la cohorte")
    ap.add_argument("--dias", type=int, default=365, help="Días de seguimiento")
    ap.add_argument("--farmacos", type=int, default=6, help="Fármacos (FAR-01 es el estudiado)")
    ap.add_argument("--eventos", type=int, default=6, help="Eventos (EVT-01 es el objetivo)")
    ap.add_argument("--prob-exposicion", type=float, default=0.30)
    ap.add_argument("--duracion", type=int, default=60, help="Días de tratamiento")
    ap.add_argument("--ventana", type=int, default=30, help="Días de riesgo tras terminar")
    ap.add_argument("--rr", type=float, default=4.0, help="RR sembrado para FAR-01 → EVT-01")
    ap.add_argument("--tasa-objetivo", type=float, default=300.0,
                    help="Tasa basal del evento objetivo por 100 000 personas-año")
    ap.add_argument("--tasa-fondo", type=float, default=3000.0,
                    help="Tasa basal de los demás eventos por 100 000 personas-año")
    ap.add_argument("--fraccion-notificada", type=float, default=0.20,
                    help="Fracción de eventos no graves que se notifican")
    ap.add_argument("--fraccion-notificada-grave", type=float, default=0.40)
    ap.add_argument("--prob-grave", type=float, default=0.2)
    a = ap.parse_args()

    rng = random.Random(a.semilla)
    farmacos = [f"FAR-{i + 1:02d}" for i in range(a.farmacos)]
    eventos = [f"EVT-{j + 1:02d}" for j in range(a.eventos)]
    tasa = {ev: (a.tasa_objetivo if j == 0 else a.tasa_fondo * (0.5 + j / a.eventos))
            / 100000 / 365 for j, ev in enumerate(eventos)}
    rr = {(farmacos[0], eventos[0]): a.rr}

    eventos_exp = {(f, e): 0 for f in farmacos for e in eventos}
    eventos_tot = {e: 0 for e in eventos}
    pt_exp = {f: 0.0 for f in farmacos}
    icsr, caso_n = [], 0

    for _ in range(a.n):
        # Ventanas de riesgo de cada fármaco: [inicio, inicio + duración + ventana)
        ventanas = {}
        for f in farmacos:
            if rng.random() < a.prob_exposicion:
                ini = rng.randrange(0, max(1, a.dias - a.duracion))
                fin = min(a.dias, ini + a.duracion + a.ventana)
                ventanas[f] = (ini, fin)
                pt_exp[f] += fin - ini
        cortes = sorted({0, a.dias, *[x for v in ventanas.values() for x in v]})
        for t0, t1 in zip(cortes, cortes[1:]):
            activos = [f for f, (i, fn) in ventanas.items() if i <= t0 < fn]
            for e in eventos:
                mult = 1.0
                for f in activos:
                    mult *= rr.get((f, e), 1.0)
                for _k in range(poisson(rng, tasa[e] * mult * (t1 - t0))):
                    dia = rng.uniform(t0, t1)
                    eventos_tot[e] += 1
                    for f in activos:
                        eventos_exp[(f, e)] += 1
                    grave = rng.random() < a.prob_grave
                    p_not = a.fraccion_notificada_grave if grave else a.fraccion_notificada
                    if activos and rng.random() < p_not:
                        caso_n += 1
                        for f in activos:
                            icsr.append({"caso_id": f"SIM-{caso_n:06d}", "farmaco": f, "evento": e,
                                         "grave": "si" if grave else "no", "dia": int(dia)})

    os.makedirs(a.salida, exist_ok=True)
    with open(os.path.join(a.salida, "icsr.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["caso_id", "farmaco", "evento", "grave", "dia"])
        w.writeheader()
        w.writerows(icsr)
    with open(os.path.join(a.salida, "verdad.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["farmaco", "evento", "rr"])
        for f in farmacos:
            for e in eventos:
                w.writerow([f, e, rr.get((f, e), 1.0)])

    pt_total = a.n * a.dias
    print(f"# {AVISO}\n")
    print(f"Cohorte: {a.n} personas · {a.dias} días · semilla {a.semilla}")
    print(f"Sembrado: {farmacos[0]} → {eventos[0]} con RR {a.rr}; el resto RR 1 (controles negativos)")
    print(f"Notificaciones generadas: {caso_n} casos ({len(icsr)} filas fármaco-evento)\n")
    print("## Cohorte completa (IRR crudo, solo el evento objetivo)\n")
    print("| Fármaco | RR sembrado | Eventos expuestos | PT expuesto (años) | IRR crudo (IC95) |")
    print("|---|---|---|---|---|")
    filas = []
    for f in farmacos:
        for e in eventos:
            x1 = eventos_exp[(f, e)]
            t1 = pt_exp[f] / 365
            x0 = eventos_tot[e] - x1
            t0 = (pt_total - pt_exp[f]) / 365
            irr = (x1 / t1) / (x0 / t0) if x1 and x0 and t1 and t0 else float("nan")
            se = math.sqrt(1 / x1 + 1 / x0) if x1 and x0 else float("nan")
            lo, hi = (irr * math.exp(-1.96 * se), irr * math.exp(1.96 * se)) if x1 and x0 else (
                float("nan"), float("nan"))
            filas.append([f, e, x1, round(t1, 1), x0, round(t0, 1), round(irr, 3)])
            if e == eventos[0]:
                print(f"| {f} | {rr.get((f, e), 1.0)} | {x1} | {t1:.0f} | "
                      f"{irr:.2f} ({lo:.2f}–{hi:.2f}) |")
    with open(os.path.join(a.salida, "cohorte.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["farmaco", "evento", "eventos_expuestos", "pt_expuesto_anios",
                    "eventos_no_expuestos", "pt_no_expuesto_anios", "irr"])
        w.writerows(filas)
    with open(os.path.join(a.salida, "LEEME.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"{AVISO}\nParámetros: {vars(a)}\n")
    print(f"\nArchivos en {a.salida}: icsr.csv, verdad.csv, cohorte.csv, LEEME.txt")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Desproporcionalidad en una base de notificaciones espontáneas (ICSR).

Métodos:
  PRR  (Evans 2001): señal si a ≥ 3, PRR ≥ 2 y χ² (Yates) ≥ 4
  ROR  con IC 95 %: señal si a ≥ 3 y límite inferior > 1
  IC   (BCPNN, aproximación de Norén 2013): señal si IC025 > 0

Entrada:
  --csv icsr.csv        una fila por par fármaco-evento de cada caso: caso_id, farmaco, evento
  --a --b --c --d       una tabla 2x2 ya contada (a = fármaco y evento; b = fármaco sin el evento;
                        c = evento sin el fármaco; d = ninguno)
  --verdad verdad.csv   opcional: farmaco, evento, rr (rr > 1 = asociación real) para medir
                        sensibilidad, especificidad y VPP de cada método

Solo usa la librería estándar. No envía datos a ningún lado.
"""
import argparse
import csv
import math
import sys
from collections import defaultdict


def metricas(a, b, c, d):
    n = a + b + c + d
    esperado = (a + b) * (a + c) / n if n else 0.0
    # Corrección de Haldane si hay celdas en cero (solo para PRR/ROR)
    aa, bb, cc, dd = (x + 0.5 for x in (a, b, c, d)) if 0 in (a, b, c, d) else (a, b, c, d)
    prr = (aa / (aa + bb)) / (cc / (cc + dd))
    se_prr = math.sqrt(max(1 / aa - 1 / (aa + bb) + 1 / cc - 1 / (cc + dd), 0))
    ror = (aa * dd) / (bb * cc)
    se_ror = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    # χ² con corrección de Yates
    num = n * max(abs(a * d - b * c) - n / 2, 0) ** 2
    den = (a + b) * (c + d) * (a + c) * (b + d)
    chi2 = num / den if den else 0.0
    ic = math.log2((a + 0.5) / (esperado + 0.5))
    ic025 = ic - 3.3 * (a + 0.5) ** -0.5 - 2 * (a + 0.5) ** -1.5
    ic975 = ic + 2.4 * (a + 0.5) ** -0.5 - 0.5 * (a + 0.5) ** -1.5
    r = {
        "a": a, "b": b, "c": c, "d": d, "esperado": esperado,
        "prr": prr, "prr_inf": math.exp(math.log(prr) - 1.96 * se_prr),
        "prr_sup": math.exp(math.log(prr) + 1.96 * se_prr), "chi2": chi2,
        "ror": ror, "ror_inf": math.exp(math.log(ror) - 1.96 * se_ror),
        "ror_sup": math.exp(math.log(ror) + 1.96 * se_ror),
        "ic": ic, "ic025": ic025, "ic975": ic975,
    }
    r["senal_prr"] = a >= 3 and prr >= 2 and chi2 >= 4
    r["senal_ror"] = a >= 3 and r["ror_inf"] > 1
    r["senal_ic"] = ic025 > 0
    return r


def tablas_desde_csv(ruta, min_a):
    casos_f = defaultdict(set)   # farmaco -> casos
    casos_e = defaultdict(set)   # evento -> casos
    pares = defaultdict(set)     # (farmaco, evento) -> casos
    todos = set()
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            c, fa, ev = r["caso_id"].strip(), r["farmaco"].strip(), r["evento"].strip()
            if not (c and fa and ev):
                continue
            todos.add(c)
            casos_f[fa].add(c)
            casos_e[ev].add(c)
            pares[(fa, ev)].add(c)
    n = len(todos)
    salida = []
    for (fa, ev), cs in pares.items():
        a = len(cs)
        if a < min_a:
            continue
        b = len(casos_f[fa]) - a
        c = len(casos_e[ev]) - a
        d = n - a - b - c
        salida.append((fa, ev, metricas(a, b, c, d)))
    return salida, n, list(casos_f), list(casos_e)


def evaluar_contra_verdad(resultados, ruta_verdad, farmacos, eventos):
    verdad = {}
    with open(ruta_verdad, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            verdad[(r["farmaco"].strip(), r["evento"].strip())] = float(r["rr"]) > 1
    calc = {(fa, ev): m for fa, ev, m in resultados}
    universo = [(fa, ev) for fa in farmacos for ev in eventos]
    print("\n## Desempeño contra la verdad conocida\n")
    print("| Método | VP | FP | FN | VN | Sensibilidad | Especificidad | VPP |")
    print("|---|---|---|---|---|---|---|---|")
    for metodo in ("prr", "ror", "ic"):
        vp = fp = fn = vn = 0
        for par in universo:
            real = verdad.get(par, False)
            pred = bool(calc.get(par, {}).get(f"senal_{metodo}", False))
            vp += real and pred
            fp += (not real) and pred
            fn += real and not pred
            vn += (not real) and not pred
        sens = vp / (vp + fn) if vp + fn else float("nan")
        esp = vn / (vn + fp) if vn + fp else float("nan")
        vpp = vp / (vp + fp) if vp + fp else float("nan")
        print(f"| {metodo.upper()} | {vp} | {fp} | {fn} | {vn} | {sens:.2f} | {esp:.2f} | {vpp:.2f} |")


def main():
    ap = argparse.ArgumentParser(description="Desproporcionalidad: PRR, ROR, IC")
    ap.add_argument("--csv")
    ap.add_argument("--a", type=int)
    ap.add_argument("--b", type=int)
    ap.add_argument("--c", type=int)
    ap.add_argument("--d", type=int)
    ap.add_argument("--min-a", type=int, default=1, help="Mostrar solo pares con al menos a casos")
    ap.add_argument("--solo-senales", action="store_true")
    ap.add_argument("--salida", help="Guardar todos los resultados en este CSV")
    ap.add_argument("--verdad", help="CSV farmaco, evento, rr para medir el desempeño")
    a = ap.parse_args()

    try:
        if a.csv:
            res, n, farmacos, eventos = tablas_desde_csv(a.csv, a.min_a)
            print(f"Casos analizados: {n} · pares fármaco-evento: {len(res)}\n")
        elif None not in (a.a, a.b, a.c, a.d):
            res, farmacos, eventos = [("fármaco", "evento", metricas(a.a, a.b, a.c, a.d))], [], []
        else:
            ap.error("Indica --csv o los cuatro valores --a --b --c --d")
    except (OSError, KeyError) as e:
        print(f"Error leyendo la entrada: {e} (columnas esperadas: caso_id, farmaco, evento)",
              file=sys.stderr)
        sys.exit(2)

    res.sort(key=lambda x: (-int(x[2]["senal_prr"] + x[2]["senal_ror"] + x[2]["senal_ic"]),
                            -x[2]["ic025"]))
    print("| Fármaco | Evento | a | Esperado | PRR (IC95) | χ² | ROR (IC95) | IC (IC025) | Señal |")
    print("|---|---|---|---|---|---|---|---|---|")
    for fa, ev, m in res:
        marcas = [k.upper() for k in ("prr", "ror", "ic") if m[f"senal_{k}"]]
        if a.solo_senales and not marcas:
            continue
        print(f"| {fa} | {ev} | {m['a']} | {m['esperado']:.1f} | "
              f"{m['prr']:.2f} ({m['prr_inf']:.2f}–{m['prr_sup']:.2f}) | {m['chi2']:.1f} | "
              f"{m['ror']:.2f} ({m['ror_inf']:.2f}–{m['ror_sup']:.2f}) | "
              f"{m['ic']:.2f} ({m['ic025']:.2f}) | {', '.join(marcas) or '—'} |")

    if a.salida:
        campos = ["farmaco", "evento"] + list(res[0][2].keys()) if res else ["farmaco", "evento"]
        with open(a.salida, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            for fa, ev, m in res:
                w.writerow({"farmaco": fa, "evento": ev, **m})
        print(f"\nResultados guardados en {a.salida}")

    if a.verdad and a.csv:
        evaluar_contra_verdad(res, a.verdad, farmacos, eventos)

    print("\nUna señal estadística es una hipótesis para evaluar, no una confirmación de causalidad.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Predicción de RAM futuras con un modelo Gamma-Poisson (predictiva binomial negativa).

Con x eventos observados en una exposición E (personas-año, pacientes-mes, unidades vendidas…),
la tasa tiene posterior Gamma(α0 + x, β0 + E). Para una exposición futura Ef, el número de
eventos sigue una binomial negativa. Si solo se notifica una fracción q, los notificados
siguen otra binomial negativa con exposición Ef·q.

Uso:
  python3 prediccion.py --eventos 12 --exposicion 8000 --exposicion-futura 10000
  python3 prediccion.py --eventos 12 --exposicion 8000 --exposicion-futura 10000 \
      --fraccion-notificada 0.06 --unidad "pacientes-año"

Solo usa la librería estándar. No envía datos a ningún lado.
"""
import argparse
import math
import sys


def cuantiles_nb(r, p, probs, max_k=10_000_000):
    """Cuantiles de una binomial negativa: P(K=k) = C(k+r-1,k) p^r (1-p)^k."""
    objetivo = sorted(probs)
    salida, i = {}, 0
    pk = math.exp(r * math.log(p))
    acum, k = pk, 0
    while i < len(objetivo) and k < max_k:
        while i < len(objetivo) and acum >= objetivo[i]:
            salida[objetivo[i]] = k
            i += 1
        pk *= (k + r) / (k + 1) * (1 - p)
        k += 1
        acum += pk
    for q in objetivo[i:]:
        salida[q] = k
    return [salida[q] for q in probs]


def predecir(alfa, beta, ef):
    p = beta / (beta + ef)
    media = alfa * ef / beta
    lo, med, hi = cuantiles_nb(alfa, p, [0.025, 0.5, 0.975])
    return media, med, lo, hi


def main():
    ap = argparse.ArgumentParser(description="Predicción Gamma-Poisson de RAM")
    ap.add_argument("--eventos", type=float, required=True, help="Eventos observados")
    ap.add_argument("--exposicion", type=float, required=True, help="Exposición observada")
    ap.add_argument("--exposicion-futura", type=float, required=True)
    ap.add_argument("--fraccion-notificada", type=float, default=None,
                    help="Fracción de eventos que se notifica (0-1), opcional")
    ap.add_argument("--alfa0", type=float, default=0.5, help="Previa Gamma: forma")
    ap.add_argument("--beta0", type=float, default=0.0, help="Previa Gamma: tasa (0 = vaga)")
    ap.add_argument("--unidad", default="unidades de exposición")
    a = ap.parse_args()

    if a.exposicion <= 0 or a.exposicion_futura <= 0 or a.eventos < 0:
        print("Error: exposición > 0 y eventos ≥ 0", file=sys.stderr)
        sys.exit(2)
    if a.fraccion_notificada is not None and not 0 < a.fraccion_notificada <= 1:
        print("Error: la fracción notificada debe estar entre 0 y 1", file=sys.stderr)
        sys.exit(2)

    alfa, beta = a.alfa0 + a.eventos, a.beta0 + a.exposicion
    tasa = alfa / beta
    print(f"Tasa estimada: {tasa * 1000:.3f} por 1 000 {a.unidad} "
          f"(posterior Gamma α={alfa:g}, β={beta:g})\n")
    print("| Predicción | Media | Mediana | IC 95 % |")
    print("|---|---|---|---|")
    m, md, lo, hi = predecir(alfa, beta, a.exposicion_futura)
    print(f"| Eventos totales en {a.exposicion_futura:g} {a.unidad} | {m:.1f} | {md} | {lo}–{hi} |")
    if a.fraccion_notificada is not None:
        m2, md2, lo2, hi2 = predecir(alfa, beta, a.exposicion_futura * a.fraccion_notificada)
        print(f"| Notificaciones esperadas (q={a.fraccion_notificada:g}) | {m2:.1f} | {md2} | "
              f"{lo2}–{hi2} |")
    print("\nSupuestos: tasa constante en el tiempo, exposición futura conocida, eventos "
          "independientes. Es una proyección, no un umbral regulatorio.")


if __name__ == "__main__":
    main()

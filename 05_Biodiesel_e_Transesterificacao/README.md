# 05 — Biodiesel e Transesterificação

## Escopo

Processo de produção de biodiesel, catalisadores heterogêneos, condições operacionais, substratos lipídicos e álcoois, balanços de massa e termodinâmica da reação.

## Relevância para o Projeto

Fundamenta as escolhas de condições operacionais da simulação (T, P, razão molar, concentrações iniciais) e a termoquímica da reação (ΔH_rxn para a Source Term de energia).

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| — | A preencher | — | — | — | 🔲 | Adicionar refs de catalisadores heterogêneos |
| — | A preencher | — | — | — | 🔲 | Adicionar refs de termoquímica da transesterificação |

## Dados Operacionais de Referência (Literatura Bath)

```
Substrato:          Óleo de canola (triolein como componente modelo)
Álcool:             Metanol (MeOH)
Razão molar:        6:1 (MeOH:óleo)  — mínimo estequiométrico é 3:1
Temperatura:        120 °C (393 K)
Pressão:            8 bar (necessária para manter MeOH líquido acima de 64°C)
Catalisador:        SrO washcoatado (19.6 wt%) ou Zn-prolina
Conversão típica:   > 90% (condições ótimas)
```

## Estequiometria Global

```
Triglicerídeo  +  3 MeOH  →  3 FAME  +  Glicerol
   (TG)                       (biodiesel)

ΔHrxn ≈ +XX kJ/mol  (endotérmica — confirmar na literatura)
```

## Propriedades Físicas Relevantes (para o CFD)

```
Mistura óleo/metanol (T = 120°C):
  ρ_óleo      ≈ 860–880 kg/m³
  μ_óleo      ≈ 5–8 × 10⁻³ Pa·s
  Cp_óleo     ≈ 2000 J/kg/K
  λ_óleo      ≈ 0.17 W/m/K
  D_TG/MeOH   ≈ 1–5 × 10⁻¹⁰ m²/s  (difusividade mútua, baixa!)

⚠️ A baixa difusividade molecular (Sc >> 1) significa que o transporte
de massa até a parede é potencialmente a etapa limitante — isso justifica
a análise do número de Damköhler na dissertação.
```

## Número de Damköhler (Da) — Diagnóstico de Regime

```
Da = τ_transporte / τ_reação = (Dh² / D_AB) / (C₀ / r_max)

Da << 1  → regime cinético  (reação é a etapa lenta)
Da >> 1  → regime difusivo  (transporte de massa é a etapa lenta)
Da ≈ 1   → regime misto     (acoplamento real — o mais interessante!)
```

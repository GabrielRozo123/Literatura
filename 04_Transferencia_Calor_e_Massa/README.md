# 04 — Transferência de Calor e Massa

## Escopo

Transferência de calor conjugada (CHT), difusão de massa em escoamento laminar confinado, números adimensionais (Nu, Sh, Pr, Sc, Le), correlações para canais e interface fluido-sólido (washcoat).

## Relevância para o Projeto

A **Fase 2** do modelo acopla:

1. **Transferência de massa** — transporte de TG e MeOH até a parede (washcoat), onde ocorre a reação
2. **Transferência de calor conjugada (CHT)** — a reação é endotérmica; haverá gradiente de temperatura axial no canal
3. **Acoplamento** — a taxa de reação LHHW depende de T, que por sua vez depende da conversão → sistema fortemente acoplado

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| — | A preencher | — | — | — | 🔲 | Adicionar refs de CHT em microcanais |
| — | A preencher | — | — | — | 🔲 | Correlações Nu para canal laminar (Nu = 7.54 plano) |

## Números Adimensionais Relevantes

```
Número de Prandtl:    Pr = Cp·μ / λ          (relação difus. momento / calor)
Número de Schmidt:    Sc = μ / (ρ·D_AB)      (relação difus. momento / massa)
Número de Lewis:      Le = Sc / Pr = λ / (ρ·Cp·D_AB)
Número de Nusselt:    Nu = h·Dh / λ          (transf. calor convectiva/condutiva)
Número de Sherwood:   Sh = k_m·Dh / D_AB     (análogo de Nu para massa)

Para escoamento laminar plenamente desenvolvido em canal plano:
  Nu_T = 7.54   (fluxo de calor uniforme na parede)
  Nu_H = 8.23   (temperatura uniforme na parede)
  Sh   ≈ 7.54   (por analogia com Nu, condição de concentração uniforme)
```

## Equações Governantes — Fase 2

```
Continuidade:     ∇·u = 0
Momento:          ρ(u·∇)u = -∇P + μ∇²u
Energia:          ρ·Cp(u·∇T) = λ∇²T + Q_rxn    [Q_rxn < 0, endotérmica]
Espécie i:        (u·∇)Ci = D_i·∇²Ci + Ri

Condição de contorno na parede (washcoat):
  -D_i·(∂Ci/∂n)|_wall = r_LHHW(Ci_wall, T_wall)   [mol/m²/s]
  -λ·(∂T/∂n)|_wall    = ΔHrxn · r_LHHW             [W/m²]
```

## Configuração no Star-CCM+ (Fase 2)

| Modelo | Caminho na árvore |
|--------|-------------------|
| CHT (Conjugate Heat Transfer) | Physics → Energy → Fluid Temperature |
| Difusão de espécies | Physics → Species → Multi-Component Liquid |
| Surface Reaction | Physics → Chemistry → Surface Reactions |
| Acoplamento parede | Boundaries → Wall → Thermal → Coupled Wall |

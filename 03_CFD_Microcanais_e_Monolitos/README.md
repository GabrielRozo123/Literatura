# 03 — CFD em Microcanais e Monolitos

## Escopo

Simulações numéricas (CFD) em microcanais e canais de reatores monolíticos. Escoamento laminar, perfis de velocidade, queda de pressão, mistura difusiva e acoplamento com reação química.

## Relevância para o Projeto

Esta pasta sustenta diretamente a **metodologia CFD** da dissertação, especialmente:

- Justificativa da geometria 2D simplificada (canal retangular)
- Validação do regime laminar (Re << 2300, tipicamente Re ~ 1–10)
- Benchmark de ΔP para a Fase 1 (hidrodinâmica a frio)
- Estado da arte para comparação de resultados

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| 1 | Pinheiro & Larimi | CFD Modeling: FBR vs PBMR for Biodiesel (Sci. Rep.) | 2024 | [Sci. Reports](https://doi.org/10.1038/s41598-024-XXXXX) | 🔲 Na fila | 2D, ácido tungstofosfórico, 180°C, razão 15:1, conv. 99,94% |
| 2 | MDPI Energies | Microchannel Reactor Technologies for Biodiesel | 2024 | [MDPI](https://www.mdpi.com) | 🔲 Na fila | Revisão recente, T-junction, geometrias, CFD comparativo |
| 3 | Chem. Eng. Process. | Numerical Simulations in Microchannels with Obstructions | 2015 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila | Alta razão área/volume, transferência de massa |
| 4 | IntechOpen | Mixing Performance in Microchannel | 2019 | [IntechOpen](https://www.intechopen.com) | 🔲 Na fila | Regime viscoso dominante, mistura por difusão molecular |

## Conceitos-Chave

### Número de Reynolds em Microcanais

```
Re = ρ·u·Dh / μ

Para o reator monolítico (valores típicos):
  Dh  ≈ 1.1 × 10⁻³ m
  u   ≈ 1–5 × 10⁻³ m/s  (escoamento lento)
  ρ   ≈ 880 kg/m³  (mistura óleo/metanol)
  μ   ≈ 5–10 × 10⁻³ Pa·s

→ Re ≈ 0.1 – 1.0  (escoamento laminar desenvolvido, regime de Stokes)
```

### Perfil de Velocidade de Poiseuille (2D)

```
u(y) = u_max · [1 - (2y/H)²]

u_max = (3/2) · u_média   (canal plano)

Onde H = largura do canal
```

### Queda de Pressão (Hagen-Poiseuille para canal plano)

```
ΔP = 12·μ·L·u_média / H²

Para H ≈ 1 mm, L ≈ 50 mm, u ≈ 1 mm/s:
ΔP ≈ 0.6 Pa  → praticamente nulo ✓
```

## Checklist de Validação — Fase 1 (Star-CCM+)

- [ ] Perfil de velocidade parabólico desenvolvido
- [ ] u_max / u_média ≈ 1.5 (Poiseuille 2D)
- [ ] ΔP calculado ≈ ΔP analítico (erro < 1%)
- [ ] Comprimento de entrada hidrodinâmico: L_ent ≈ 0.05 · Re · Dh
- [ ] Número de Mach << 0.3 (confirmação de incompressibilidade)

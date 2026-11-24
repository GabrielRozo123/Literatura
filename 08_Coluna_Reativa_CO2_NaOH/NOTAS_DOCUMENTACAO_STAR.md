# Coluna reativa CO₂/NaOH: notas da documentação do STAR-CCM+ 2602

Caso escolhido: benchmark de Darmana et al. (2007). Coluna pseudo-2D de 0,2 × 0,03 m com 1,0 m de líquido; CO₂ puro em NaOH; validação pelo pH em função do tempo. Comparação com Krauß & Rzehak (2018) e Liu et al. (2021). Depois, aplicação a uma coluna de escala industrial.

Este arquivo registra o que cada página da documentação oferece ao nosso caso.

## Lote 1: tutorial "Eulerian: Aeration Tank Degassing"

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Visão geral | Tanque 0,5 × 0,1 × 0,3 m, cheio de água. Ar entra a 5 m/s por placa perfurada (4 % de área aberta), modelado como velocity inlet com α_ar = 0,04. Topo modelado como **phase-permeable wall** (degassing): só o gás sai. Monitores de *phase mass flow*. | **Topo da coluna como degassing boundary.** Evita simular a superfície livre e o espaço de gás. É a condição usual em Euler–Euler de colunas (abordagem do HZDR). |
| Selecting the Physics Models | 3D; Multiphase + Multiphase Interaction; EMP; Gradients; **Steady**; Turbulent; Mixture Turbulence; K-Epsilon (Realizable Two-Layer, All y+); Gravity. | Mesmo conjunto, mas **Implicit Unsteady**: o pH evolui no tempo. |
| Creating the Water and Air Phases | Fases Water (Liquid, densidade constante) e Air (Gas, densidade constante). | A água precisa ser **multicomponente** (CO₂, OH⁻, HCO₃⁻, CO₃²⁻, Na⁺, H₂O) e o gás é CO₂. **Falta a página das fases multicomponentes.** |
| Setting Up the Phase Interactions | Water–Air contínua-dispersa; Virtual Mass; Turbulent Dispersion; comprimento de interação constante (1 mm); arrasto de Tomiyama (σ = 0,072 N/m automático). | Igual. O diâmetro deve vir do experimento, pois as bolhas de CO₂ puro **encolhem**: diâmetro variável ou constante por trechos. Falta lift (temos do caso anterior). |
| Specifying Initial Conditions and Gravity | α_água = 1; g = [0, −9,81, 0]; ρ_ref = 997,561 kg/m³ (fase contínua). | Igual. Acrescentar a condição inicial das espécies: [NaOH] do experimento. |

**Ainda falta, no lote 1:** transferência de massa entre as fases, espécies e reação. Esse tutorial não as usa.

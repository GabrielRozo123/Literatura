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

## Lote 2: "Aeration Tank": condições de contorno; tutorial "Eulerian: Hibiki's Bubble Column"

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Setting the Boundary Conditions (aeration tank) | Degassing Outlet: em *Phase Conditions > Air*, **Type = Phase Permeable** (o gás sai, a água vê parede). Velocidade tangencial opcional (no tutorial, para induzir circulação). Gas Inlet com *phase conditions*: água 0 m/s e α = 0,96; ar 5 m/s e α = 0,04. O STAR garante que a vazão de gás que entra é igual à que sai. | **Topo = Phase Permeable para o CO₂**, sem velocidade tangencial. Aspersor: velocity inlet com α_gás < 1 (entrada diluída, como na coluna anterior, para não divergir). A vazão de CO₂ vem do experimento. |
| Hibiki: visão geral | Coluna de 3,06 m × 50,8 mm, axissimétrica, bolhas de 3 mm. Parte 2: **S-Gamma** para a distribuição de tamanhos (quebra e coalescência), com o **diâmetro de Sauter alimentando o Interaction Length Scale**. Há seção de validação. | O S-Gamma é o candidato natural para o **encolhimento das bolhas de CO₂**, desde que aceite um termo de perda de massa por dissolução. A confirmar na teoria do S-Gamma. |
| Hibiki: Selecting the Physics Models | Axisymmetric; Steady; EMP; **Phasic Turbulence**; Gravity. | Usamos **Mixture Turbulence** (validado na coluna anterior, mais robusto). Phasic Turbulence fica como teste de sensibilidade. |
| Hibiki: Defining the Phases | Água: Realizable k-ε Two-Layer, All y+, ρ = 1000 kg/m³, μ = 1e-3 Pa·s. Ar: **Turbulence Response (Issa)**, ρ = 1 kg/m³, μ = 1,8e-5 Pa·s. | Gás = CO₂ (ρ ≈ 1,8 kg/m³ a 1 atm e 25 °C; μ ≈ 1,5e-5 Pa·s). Issa só com Phasic Turbulence. |
| Hibiki: Setting up the Phase Interactions | Desativar *Auto-select*; Continuous-Dispersed; Drag (Tomiyama); **Lift constante = −0,05**; Virtual Mass; Turbulent Dispersion; Interaction Length Scale constante de 3 mm. | Mesmo conjunto. Na coluna anterior usamos lift de Tomiyama; para d ≈ 3–5 mm com CO₂ puro, testar as duas opções. |

**Ainda falta, nos lotes 1–2:** multicomponente na fase líquida, transferência de massa entre fases, reação e a teoria do S-Gamma com transferência de massa.

## Lote 3: tutorial Hibiki, parte 2 (S-Gamma) e execução

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Setting Boundary Conditions (Hibiki) | Inlet com mistura (água 1,23 m/s, α = 0,8; ar 1,61 m/s, α = 0,2); turbulência por *Intensity + Length Scale* (5 mm); outlet padrão; eixo como *Axis*. | Nosso líquido não escoa (batelada): só o gás entra pelo aspersor. |
| Running the Simulation | Sub-relaxação: Phase Coupled Velocity 0,4; Pressure 0,5; Volume Fraction 0,3; k-ε 0,8. 2000 iterações em regime permanente; export de line probes em CSV. | Mesmos valores **na inicialização em regime permanente da hidrodinâmica**, antes de ligar o transiente reativo. |
| Specifying the Particle Size Distribution | Na fase gás: *Particle Size Distribution > S-Gamma > Discrete Quadrature S-Gamma*, **Two Equation** (momentos S0 e S2: densidade numérica e área interfacial). Condição inicial de d32 (3 mm). | **Candidato para o diâmetro variável das bolhas de CO₂.** Ainda falta confirmar se a transferência de massa entre fases entra como fonte nos momentos (encolhimento por dissolução). |
| Modifying the Phase Interaction | Ativar S-Gamma Breakup (Cg = 5,0; We_crit = 0,23) e S-Gamma Coalescence (Cg = 0,1). *Interaction Length Scale* passa para **Sauter Mean Diameter**. d32 imposto no inlet. σ = 0,072 N/m. | Igual. d32 no aspersor vem do experimento. |
| Validating the S-Gamma Model | **Área interfacial a = π·S₂**: field function `$SecondSizeDistributionMomentAir*3.14` (dimensão comprimento⁻¹). d32 de 1,9 a 6,2 mm, boa concordância com o experimento; a fração de vazio fica subestimada perto da parede. | **Essa é a área a do nosso k_L·a·E.** Com S-Gamma: `a = π·$SecondSizeDistributionMomentCO2`. Sem S-Gamma: `a = 6·α_G/d`. Nome interno a conferir na tabela *Reference* da field function. |

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

## Lote 4: teoria de escoamento reativo (Reacting Flow)

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Reacting Flow Applications | Mapa de *workflows*. Polimerização multifásica: "use o modelo *dentro de uma fase líquida multicomponente* do Multiphase". | Confirma que **reação dentro de uma fase Euleriana multicomponente** é suportada. |
| Reacting Flow General Workflow | Material = **Multiphase** nos *workflows* Eulerian/Multiphase Complex Chemistry. **Multiphase Complex Chemistry exige Implicit Unsteady** e EMP ou MMP (não VOF). Reaction Regime = Reacting (na fase). Sub-relaxação de espécies igual à de energia. Inicializar o transiente a partir do regime permanente. | Nosso caso já é transiente. Lista de *workflows* que ainda precisamos ler: *Reacting Species Transport (intraphase)*, *Multiphase Complex Chemistry*, *Interphase Reactions: Multiphase*. |
| Reaction Mechanism Formats | Formato Chemkin (ELEMENTS, SPECIES, REACTIONS com A, β, Ea). **Arquivo de química multifásica**: seções `GAS/_Phase/`, `LIQUID/_Phase/` e `SOLID/_Phase/`. Palavras-chave REV (taxa reversa explícita), FORD/RORD (ordens), unidades de Ea (`KELVINS`, `JOULES/MOLE`…). | Podemos escrever o **mecanismo do CO₂/NaOH como arquivo**: CO₂ no gás e CO₂(aq), OH⁻, HCO₃⁻, CO₃²⁻, Na⁺, H₂O no líquido. Reações reversíveis com **REV** (Arrhenius reverso explícito), sem precisar de dados termodinâmicos. |
| Reacting Model Reference | Reações com Arrhenius (A, β, Ea); *Reversible* com reversa **por constante de equilíbrio** (exige h, s, cp) **ou por Arrhenius reverso** (não exige). **Interphase Area Density Multiplier** (só com Multiphase Complex Chemistry): a **densidade de área interfacial entra na taxa** (Eq. 3423). Solver CVODE (rígido). Fontes definidas pelo usuário em C, com acesso a field functions. | **Duas rotas para a absorção:** (A) transferência de massa entre fases do EMP, com k_L·E em field function (falta a documentação); (B) **absorção escrita como "reação interfacial" reversível** CO₂(G) ⇌ CO₂(L) com multiplicador de área: k_f = k_L·E/He e k_r = k_L·E, o que dá N·a = k_L·E·a·(C_G/He − C_L). A rota B embute a lei de Henry na reversibilidade. **Reações no líquido** (CO₂ + OH⁻ ⇌ HCO₃⁻; HCO₃⁻ + OH⁻ ⇌ CO₃²⁻ + H₂O) com Arrhenius direto e reverso; o CVODE trata a rigidez. |
| User-Defined Reaction Rate Source Terms | Funções C (`wdotCalculate`, `wdotModify`, `reactionRateModify`), compiladas como biblioteca de usuário (`uclib`). Recomenda Jacobiano numérico. `UserAccessibleData` dá acesso a pressão, Δt, volume e **field functions** (`_fieldFunctionsData._ffVal[i]`). | **Último recurso** (exige compilador C). Serviria para um **E variável com o pH** na rota B: `reactionRateModify` multiplica a taxa interfacial por E(Ha, Ei) lido de uma field function. Começamos sem código: E constante, ou E por field function na rota A. |

**Faltam, para fechar a rota:**
1. *Multiphase Complex Chemistry Workflow* e a teoria da Eq. 3423 (como a área interfacial entra na taxa e em que unidades).
2. *Reacting Species Transport Workflow* (reação intrafase numa fase Euleriana).
3. *Interphase Mass Transfer* do EMP (rota A): modelos disponíveis e se aceitam field function.
4. *Defining Chemical Reactions Manually* ou *Importing Species and Reactions* (unidades de A para espécies em solução).

## Lote 5: Reacting Species Transport, Complex Chemistry e EMP

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Reacting Species Transport (teoria) | Transporte das frações mássicas de todas as espécies, com um solver químico separado (CVODE). **Complex Chemistry** = cinética finita geral. Opções de interação turbulência–química: **Laminar Flame Concept** (LFC: taxa avaliada no estado médio da célula; para reações lentas ou transientes), EDC e TFC. O modelo de polimerização roda numa **fase líquida multicomponente do EMP**. | Reação na fase líquida via Complex Chemistry + LFC. EDC e TFC são para chamas. |
| Reacting Species Transport Workflow | "Para reações **líquido–líquido** limitadas por cinética finita: **Complex Chemistry**." Reações simples e rápidas com mistura lenta: Eddy Contact Micromixing. Mecanismo importado no nó Complex Chemistry ou criado em *Reacting > Reactions*. *Relax to Chemical Equilibrium* opcional. | **Rota intrafase:** fase líquida = Multi-Component Liquid + Reacting + Reacting Species Transport + Complex Chemistry + LFC. |
| Chemistry Acceleration | **Clustering ativo por padrão**, com variáveis de agrupamento de **combustão**: razão de equivalência, temperatura, fração mássica de OH. Alternativas: ISAT (até ~40 espécies, ideal em regime permanente) e DMR. | ⚠️ **Desligar o Clustering** (ou trocar as variáveis por frações de OH⁻/CO₂). Nosso sistema é isotérmico e sem "combustível": o agrupamento padrão juntaria células com químicas diferentes. São só 6 espécies e a malha é pequena, então o CVODE puro é barato. |
| Multiphase Complex Chemistry Workflow | Continuum: EMP ou MMP, **3D**, **Implicit Unsteady**, *Multiphase Complex Chemistry*. Importa **mecanismo multifásico + arquivo termodinâmico** (com fases G, L e S), **sem arquivo de transporte**. As espécies povoam as fases automaticamente. Nas fases: *Reaction Regime* = **Non-reacting** (a química fica no nível do continuum). | **Rota multifásica:** absorção (CO₂ G→L) e reações num único mecanismo. **Exige arquivo termodinâmico** com polinômios NASA também para os íons (dá para usar cp constante: o caso é isotérmico e as reversas são por **REV**, sem equilíbrio termodinâmico). **3D obrigatório**, o que serve à coluna de Darmana (pseudo-2D, mas com espessura de 3 cm). |
| Modeling Eulerian Multiphase Flow | Fases podem ser **Multi-Component Liquid/Gas**. Condições iniciais por fração mássica ou molar de cada componente. Fontes de massa por região/fase. Relatório *Normalized Phase Mass Conservation Error*. *Adaptive Time-Step* disponível. A interação entre fases inclui "**models for the rates of interphase transfer of mass**". | Água multicomponente. Monitorar o erro de conservação de massa da fase, que é crítico porque o gás perde massa ao dissolver. Falta a página de transferência de massa entre fases. |

### Constantes cinéticas a 25 °C (força iônica desprezada; a conferir com Darmana / Krauß & Rzehak)

| Reação | k direta | K_eq | k reversa | Tempo característico a [OH⁻] = 0,0316 M |
|---|---|---|---|---|
| R1: CO₂ + OH⁻ ⇌ HCO₃⁻ | 8,05×10³ L/(mol·s) = **8,05×10⁶ cm³/(mol·s)** (Pohorecki & Moniuk) | 4,47×10⁷ L/mol | **1,8×10⁻⁴ s⁻¹** | 3,9 ms |
| R2: HCO₃⁻ + OH⁻ ⇌ CO₃²⁻ + H₂O | ~6×10⁹ L/(mol·s) (ordem de grandeza; conferir) | 4,68×10³ L/mol | 1,28×10⁶ s⁻¹, ou seja, **A_rev = 2,3×10⁷ cm³/(mol·s)** se a reversa incluir [H₂O] = 55,5 M (ou RORD H₂O 0) | 5×10⁻⁹ s (equilíbrio instantâneo) |

As unidades Chemkin são mol, cm³ e s. A R2 é ~10⁶ vezes mais rápida que a R1, então o sistema é rígido e o CVODE é obrigatório. Íons como pseudo-espécies neutras (OHM, HCO3M, CO3MM, NAP): as reações ficam balanceadas em elementos sem o elétron, pois a carga se conserva em cada reação.

## Lote 6: transferência de massa entre fases no EMP

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Modeling Bubbly and Droplet Flows | Na fase: Material **Multi-Component Liquid/Gas** ("para reações, cada fase multicomponente"); *Reaction Regime* = **Reacting**, com Reacting Species Models; **para reação intrafase, Energy = Segregated Fluid Enthalpy é obrigatório em cada fase que reage**. Opcionais: S-Gamma, AMUSIG (distribuição de tamanhos). **Tipos de transferência de massa:** Boiling, **Dissolution**, Droplet Evaporation, **Interphase Reaction** (as duas fases multicomponentes) e **User-Defined Interphase Mass Flux** (com *Interphase Mass Transfer*; supõe efeito desprezível nas temperaturas). | **O User-Defined Interphase Mass Flux é a rota preferida**: o fluxo k_L·E·(C_G/He − C_L) entra por field function, com E calculado localmente a partir do pH. Falta a página dele. A energia (Segregated Fluid Enthalpy) é exigida na fase líquida reativa; o caso continua praticamente isotérmico (ΔT < 1 K a [NaOH] = 0,03 M). |
| Modeling a Multi-Component Mixture | Componentes vêm do banco de materiais (Standard), com propriedades constantes por padrão. É possível criar pastas de mistura e substituir ou reordenar componentes. | Os íons não estão no banco padrão: serão criados pelo **import do mecanismo** (Complex Chemistry) ou como materiais de usuário (cópia de H₂O renomeada, com a massa molar certa). |
| Modeling Dissolution Mass Transfer | Interação: *Interphase Mass Transfer* > **Dissolution** (Eq. 2108). Escolher os componentes transferidos (*Phase 0 Components*); Sherwood das fases contínua e dispersa; coeficiente de equilíbrio por componente. Com modelos de energia, as fontes de energia de cada fase devem ser dadas por field function. | Rota **mais simples** e sem field functions de fluxo, mas com limitações (abaixo). |
| Sherwood Number Properties | Métodos: **Ranz–Marshall** (Eq. 2008) e **Armenante–Kirwan** (Eq. 2368; turbulento; expoentes e **fator de calibração** ajustáveis). | ⚠️ Ranz–Marshall vale para **esfera rígida** e subestima o k_L de bolhas limpas (Higbie) por um fator de ~3–4. O fator de calibração de Armenante–Kirwan permite embutir um **E constante**, mas não um E variável com o pH. |
| Equilibrium Coefficient Properties | Gás–líquido: razão de **frações molares** (Eq. 2104); **Henry's Law** (Eq. 2106) ou Raoult. Para líquido–líquido: constante ou field function. | Henry do CO₂: converter kH = 0,034 mol/(L·atm) para a forma em fração molar da Eq. 2106 (falta a página da teoria). |

### Decisão provisória de rota

1. **Hidrodinâmica:** EMP + Mixture k-ε + Tomiyama + lift + VM + TD; topo *degassing*; S-Gamma opcional.
2. **Química no líquido (intrafase):** Multi-Component Liquid + Reacting + Complex Chemistry + LFC + Segregated Fluid Enthalpy; mecanismo Chemkin com R1 e R2 reversíveis (REV); **Clustering desligado**.
3. **Absorção:** **User-Defined Interphase Mass Flux**, com fluxo = M_CO₂·k_L·E·(C_G/He − C_L). Plano B: Dissolution com Armenante–Kirwan e E constante no fator de calibração.
4. **E local em field function, pela fórmula explícita de DeCoursey (1974):** E = −Ha²/[2(Ei−1)] + √{Ha⁴/[4(Ei−1)²] + Ei·Ha²/(Ei−1) + 1}, com Ha = √(k₁[OH⁻]D_CO₂)/k_L e Ei = 1 + D_OH[OH⁻]/(2D_CO₂C*). **Conferida contra van Krevelen–Hoftijzer** (`cinetica_projeto.fator_aumento`): diferença de 1–5 % entre Ha = 0,3 e 10 e Ei = 1,2 e 50. É a mesma família de modelos comparada por Krauß & Rzehak (2017).

**Páginas que faltam:** *User-Defined Interphase Mass Flux* (unidades, como se escolhe a espécie, se a área a entra automaticamente); *Modeling Interphase Reactions*; teoria das Eqs. 2104, 2106 e 2108 (Henry e taxa de dissolução).

## Lote 7: Interphase Reaction (EMP), que fecha a rota da absorção

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Modeling Interphase Reactions | Continuum: **Phase Coupled Fluid Energy**. Interação: Energy (Segregated Fluid Enthalpy ou Temperature), **Reaction Regime = Reacting**, *Interphase Mass Transfer > Interphase Reaction*. Reações criadas no GUI (reagentes e produtos, coeficiente estequiométrico, **expoente de taxa**) e coeficiente da taxa em *Properties > Reaction Coefficient*. | Duas "reações" interfaciais irreversíveis: **(I1) CO₂(G) → CO₂(L)** e **(I2) CO₂(L) → CO₂(G)**, cada uma com expoente 1 no reagente. |
| Interphase Reaction Model Reference (EMP) | Exige as duas fases **multicomponentes** e energia por fase (Segregated Fluid Enthalpy ou Temperature). Métodos: *Diffusion Limited User Reaction Rate* (mín. entre cinética e difusão), First/Half/Second-Order Combined Rate (partícula–gás) e **User Reaction Coefficient, que funciona como *scalar profile*** (portanto aceita field function). | **User Reaction Coefficient por field function**, sem código C. |
| Interphase Reactions (teoria) | **Eq. 3569: ω = k·Π[X_j]^{r_j}·a_cd**. O termo k·Π[X]^r deve estar em **kmol/(m²·s)**, e a densidade de área interfacial a_cd (*Interaction Area Density*) é multiplicada **automaticamente**. Se a taxa for por volume, dividir por `$InteractionAreaDensityPhaseInteraction1`. Diffusion-limited (Eqs. 3571–3574): K_D = Sh·D/L, ω = mín(R, F·ρ·K_D·Y·A). | Com expoente 1 e [X] em kmol/m³, **k tem unidade de m/s**: I1: k = **k_L·E/He**; I2: k = **k_L·E**. Assim ω_líq = k_L·E·a·(C_G/He − C_L), exatamente o fluxo do modelo 0D, com E local de DeCoursey. |

### Rota definida (documentação do STAR completa no essencial)

1. **Continuum:** 3D; Implicit Unsteady; Multiphase; EMP; Mixture Turbulence (Realizable k-ε Two-Layer); Gravity; **Phase Coupled Fluid Energy**.
2. **Fase gás (dispersa):** Multi-Component Gas: CO₂ (+ N₂ inerte opcional, para evitar fração mássica unitária); Segregated Fluid Enthalpy; Non-reacting; densidade constante (≈ 1,8 kg/m³).
3. **Fase líquida (contínua):** Multi-Component Liquid: H₂O, CO₂(aq), OH⁻, HCO₃⁻, CO₃²⁻, Na⁺; Segregated Fluid Enthalpy; **Reacting > Reacting Species Transport > Complex Chemistry + Laminar Flame Concept**. R1 e R2 reversíveis (Arrhenius direto e reverso). **Clustering desligado**.
4. **Interação Água–CO₂:** Tomiyama (drag), lift, VM, TD; *Interaction Length Scale* constante ou S-Gamma; **Interphase Mass Transfer > Interphase Reaction**: I1 e I2 com *User Reaction Coefficient* por field function.
5. **Field functions:**
   - u_rel = |u_G − u_L|;
   - k_L (Higbie) = 2·√(D_CO₂·u_rel/(π·d));
   - [OH⁻] = ρ_L·Y_OH/M_OH;
   - C_G = ρ_G·Y_CO₂/M_CO₂ e C* = C_G/He;
   - Ha = √(k₁·[OH⁻]·D_CO₂)/k_L;
   - Ei = 1 + D_OH·[OH⁻]/(2·D_CO₂·C*);
   - E (DeCoursey);
   - pH a partir do balanço de cargas, ou −log₁₀(K_w/[OH⁻]) enquanto pH > 9.
6. **Contornos:** aspersor = velocity inlet (entrada diluída); topo = Phase Permeable para o gás; paredes sem escorregamento.

**Nota de modelagem.** O E aplicado à transferência mais a reação no seio não contam a reação em dobro. O filme é submalha: E corrige o fluxo e a reação no seio consome o CO₂ que chega, preservando a estequiometria. Essa é a formulação de Krauß & Rzehak (2017, 2018). Diferença conhecida: o modelo 0D usava k_L(E·C* − C_L); aqui fica k_L·E·(C* − C_L). As duas coincidem quando C_L ≪ C*.

**Páginas opcionais, se aparecerem:** *Interaction Area Density Model Reference* (fórmula de a_cd, em especial com S-Gamma); *Complex Chemistry Model Reference* (tolerâncias do CVODE, onde desligar o Clustering); *Defining Chemical Reactions Manually* (as R1 e R2 podem ser criadas no GUI, sem arquivo Chemkin, e os dados de componente como entalpia de formação e cp entram no próprio GUI).

## Lote 8: área interfacial, transporte de espécies, propriedades de mistura e escalares passivos

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Interaction Area Density (teoria e referência) | Métodos: *Field Function*; *Spherical Particle* a = 6α_d/l (**obsoleto no 2602**); **Symmetric (padrão): a = 6·α_c·α_d/l**. Transferência de calor e massa usa a diretamente; o arrasto usa a/4 como área projetada. Field function: `Interaction Area Density of [interação]`. | ⚠️ **O padrão do STAR é a = 6·α_L·α_G/d, menor que o 6·α_G/d da literatura e dos nossos cálculos 0D** pelo fator α_L ≈ 0,9–0,95. Para comparar com Krauß & Rzehak: manter Symmetric (o arrasto foi validado assim na coluna anterior) e **dividir o coeficiente das reações interfaciais por α_L** quando quisermos 6α_G/d exato. Registrar no relatório como sensibilidade (5–10 %). |
| Species Transport | Eq. 1814: transporte de Y_i com difusão molecular (Fick, D_{i,m}) + turbulenta (μ_t/σ_t) + fonte S_Y (reação ou fonte de região). Difusão multicomponente (Maxwell–Stefan), Soret e migração de espécies carregadas (Nernst–Planck) são opcionais. O STAR garante ΣY_i = 1. | **Fick com D_{i,m} constante por componente:** D_CO₂ = 1,92e-9, D_OH = 5,27e-9, D_HCO₃ ≈ 1,2e-9, D_CO₃ ≈ 0,92e-9, D_Na ≈ 1,33e-9 m²/s. Na prática domina a difusão turbulenta (Sc_t = 0,9). Migração elétrica desligada: hipótese de eletroneutralidade. |
| Multi-Component Mixture Material Properties | Propriedades da mistura por média mássica (Eq. 1829); difusividade por coeficientes binários, Schmidt ou teoria cinética; massa molar pela regra da mistura (Eq. 1840). | Densidade e viscosidade do líquido ≈ água (solução diluída): constantes. Massa molar por mistura, que entra na conversão Y ↔ C das field functions. |
| Passive Scalars Transport | Escalar passivo sem efeito nas propriedades; o exemplo inclui "dissolução de gás num líquido". | Útil numa **etapa intermediária de verificação**: idade do líquido ou traçador para medir a mistura (D_L) antes de ligar a química. |

## Lote 9: S-Gamma (teoria e referência)

| Página | O que traz | Uso no nosso caso |
|---|---|---|
| Transport Equations (S-Gamma) | **Eq. 2130 (S₀):** fontes de breakup, coalescência, nucleação Ṅ₀, usuário e **s_diss**. A dissolução retira partículas quando Ṁ < 0: s_diss = (d32/d30 − 1)·máx(0, −Ṁ/ρ)·S₀/α_d (Eq. 2131, com o sinal conforme o texto). **Eq. 2137/2139 (S₂):** termo **s_m de transferência de massa**: Ṡ₂ = (4Ṁ/πρ)·(πS₀/6α_d)^{1/3} (Eq. 2142), mais o efeito de densidade variável. | ✅ **O S-Gamma encolhe as bolhas pela transferência de massa entre fases.** Exige o modo **Two Equation**, para que S₀ tenha o termo de dissolução. A confirmar na primeira rodada: se o Ṁ do *Interphase Reaction* alimenta esse termo (o texto fala no "interphase mass transfer rate" genérico). |
| Moments and Mean Particle Diameters | d32 = 6α/(πS₂); d30 = (6α/πS₀)^{1/3}; distribuição log-normal; condição de realizabilidade d32 ≥ d30. | Com S-Gamma, a área simétrica do STAR fica a = 6α_Lα_G/d32 = α_L·π·S₂. |
| S-Gamma Models Reference | Discrete Quadrature ou Pre-Integrated; **Minimum/Maximum Diameter**; One/Two Equation; convecção de 1ª/2ª ordem; Prandtl turbulento do S-Gamma; condição inicial e de contorno: d32 (± variância); fontes de usuário S₀/S₂; relaxação igual à da fração volumétrica (padrão 0,5). Field functions: `SauterMeanDiameter`, `SecondSizeDistributionMoment`, `ZerothSizeDistributionMoment`, `ThreeZeroDiameter`, `ParticleSizeVariance` (sufixo `of [fase]`). | **Minimum Diameter ≈ 0,1 mm**, para evitar colapso numérico quando a bolha dissolve quase toda. d32 no aspersor = valor medido por Darmana. |
| Discrete Quadrature S-Gamma Phase Interaction | Breakup: constante, field function, Coulaloglou–Eskin (Cg 1, We_c 0,5), Power Law, Coulaloglou–Tavlarides (Cg 0,25, We_c 1), Kocamustafaogullari. Fragmentos: n_f = 2, σ = 0,025. Colisão turbulenta (Cg 0,3655); eficiência de coalescência Luo, O'Rourke ou Coulaloglou–Tsouris. Field functions das taxas. | Hibiki usou breakup Cg 5 / We_c 0,23 e colisão Cg 0,1. |
| S-Gamma Phase Interactions (teoria) | Formulações de breakup (viscoso e inercial; d_cr de Hinze/de Bruijn; tempo de Chesters) e de coalescência (drenagem de filme de Chesters; interface móvel/imóvel; Hamaker). O breakup e a coalescência conservam o volume da fase dispersa. | Na coluna de Darmana (α_G baixo, bolhas de 3–5 mm) o efeito dominante deve ser a **dissolução**. |

### Estratégia para o tamanho de bolha

1. **Rodada base:** S-Gamma Two Equation, **sem** breakup nem coalescência. Só a dissolução muda d32. Comparar d32(z) com o **perfil axial de diâmetro medido por Darmana** e com o 0D (número de bolhas conservado: d(z) = d₀·[F(z)/F₀]^{1/3}).
2. **Sensibilidade:** ligar breakup e coalescência com as constantes do Hibiki.
3. **Plano B** (se o Ṁ da Interphase Reaction não entrar no S-Gamma): fonte de usuário em S₂ via field function, s_u = Ṡ₂ da Eq. 2142 com Ṁ calculado pelas nossas field functions, e s_diss correspondente em S₀; ou diâmetro constante por trechos.

**Conclusão: a documentação do STAR necessária está completa.** Faltam só os artigos (Krauß & Rzehak 2018; Darmana et al. 2007).

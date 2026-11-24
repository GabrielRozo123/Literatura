# Coluna de bolhas reativa CO₂/NaOH no STAR-CCM+ 2602: guia de setup

Caso de validação: experimento de **Darmana et al. (2007)**. Referência Euler–Euler: **Krauß & Rzehak (2018)**, que chamamos de K&R.
Modelo de apoio, programado e validado antes do CFD: `Programacao/coluna_reativa_darmana/modelo_pontual.py`.
Geometria: `Programacao/coluna_reativa_darmana/geometria/coluna_darmana_200x1000x30.step`.
Notas da documentação do STAR: `NOTAS_DOCUMENTACAO_STAR.md`, nesta pasta.

---

## 0. Experimento e roteiro de rodadas

| Item | Valor (Darmana 2007; K&R 2018) |
|---|---|
| Coluna | 200 mm (largura) × 30 mm (profundidade) × 1500 mm; **líquido até 1000 mm** |
| Aspersor | 21 agulhas (Ø_int 1 mm) em malha 7 × 3, passo de 5 mm, no centro do fundo → retângulo de **30 × 10 mm** |
| Gás | N₂ até o escoamento ficar estatisticamente estacionário; depois **CO₂ puro**. **U_G = 7 mm/s** (2,2 mL/s por agulha) |
| Bolhas na saída das agulhas | **d₀ = 5,5 mm** |
| Líquido | NaOH, **pH₀ = 12,5** ([OH⁻] = [Na⁺] = 0,0312 kmol/m³); T não informada → 25 °C |
| Sensor de pH | (x, y, z) = **(0, 980, 0) mm** |
| PIV | ponto (−50, 500, 0) mm (oscilação da pluma); perfis em y = 750 mm |
| α_G integral | **2,3 % (N₂)**, **1,2 % (CO₂)** |
| Frequência da pluma | **0,17 Hz (N₂)**, **0,10 Hz (CO₂)** |

**Dados digitalizados**, extraídos dos vetores do PDF e não lidos "no olho" (pasta `dados_literatura/`):
- `pH_experimento_E2.csv`: pH × t, 238 pontos (Fig. 5 de Darmana);
- `pH_simulacao_DBM_S2.csv`: simulação Euler–Lagrange de Darmana;
- `d32_axial_experimento_E2.csv`: d32/d₀ × z/H com desvio padrão (Fig. 13). Abaixo de z/H ≈ 0,4 os autores consideram os dados pouco confiáveis.

**Modelo pontual** (a abordagem de K&R 2016, com a química do apêndice de K&R 2018; α_G = 1,2 %, d = 3,5 mm, u_rel = 0,23 m/s):

| | t (pH 10) | t (pH 8) | RMSE do pH |
|---|---|---|---|
| Experimento E2 | 109 s | 162 s | — |
| **K&R completo (E_a ajustado + reação com água)** | **107 s** | **167 s** | **0,15** |
| Sem a reação com água | 107 s | 178 s | 0,31 |
| E_a aproximado de Darmana | 118 s | 178 s | 0,41 |

**Leitura:** a química implementada reproduz o experimento quando a hidrodinâmica é imposta. Quando o CFD errar, a diferença vem da hidrodinâmica. Foi essa a conclusão de K&R, que tiveram cerca de 20 % de atraso com Euler–Euler/RANS.

**Rodadas**

| Etapa | O que roda | Valida contra |
|---|---|---|
| **A** | Hidrodinâmica com N₂ (sem espécies reativas), 0–80 s | α_G = 2,3 %; f_pluma = 0,17 Hz |
| **B** | A + CO₂ a partir de t = 20 s, química de Darmana (R_I + R_II), E constante = 1,4 | pH(t), d32(z), α_G = 1,2 % |
| **C** | B com E local (DeCoursey + E_a de K&R) e reação com água (R_III + R_W) | idem; comparar com a B |
| **D** | Sensibilidades: k_L (Brauer × Higbie), área (simétrica × 6α/d), breakup/coalescência no S-Gamma, malha | — |
| **E** | Aplicação a uma coluna de escala industrial | equações de projeto do seminário |

---

## 1. Geometria e malha

1. **File > Import > Import CAD Model**: `coluna_darmana_200x1000x30.step` (unidades **mm**). As faces já vêm nomeadas: `Aspersor`, `Fundo`, `Topo`, `Parede_Frente`, `Parede_Tras`, `Parede_Esq`, `Parede_Dir`.
   - Origem no centro do fundo; **y é a vertical**; x é a largura; z é a profundidade.
2. **Assign Parts to Regions**: uma região, com **um boundary por superfície**.
3. **Malha (Automated Mesh)**:
   - **Trimmed Cell Mesher**, Base Size **5 mm**, sem prism layer (K&R usam função de parede). Dá ≈ 40 × 200 × 6 ≈ 48 mil células.
   - Alternativa fiel a K&R: **Directed Mesh** 29 × 75 × 9 (≈ 20 mil células, 6,9 × 13,3 × 3,3 mm).
   - Refinar a região do aspersor (bloco 40 × 60 × 30 mm acima do fundo, 2,5 mm) ajuda a pluma.

---

## 2. Continuum: modelos (Physics 1)

| Grupo | Modelo |
|---|---|
| Space | Three Dimensional |
| Time | **Implicit Unsteady** |
| Material | **Multiphase** (Multiphase Interaction automático) |
| Multiphase Model | **Eulerian Multiphase (EMP)** |
| Viscous Regime | Turbulent |
| EMP Turbulence | **Mixture Turbulence** (Realizable k-ε Two-Layer, All y+) |
| Optional | **Gravity**; **Phase Coupled Fluid Energy** (exigido pela Interphase Reaction) |

**Reference Values:** Gravity = [0, −9,81, 0] m/s²; Reference Density = 997,05 kg/m³; Reference Pressure = 101325 Pa.

---

## 3. Fases

### 3.1 Água (contínua): `Agua`

| Grupo | Modelo |
|---|---|
| Material | **Multi-Component Liquid** |
| Reaction Regime | **Reacting** → Reacting Species Transport → **Complex Chemistry**; turbulência–química: **Laminar Flame Concept** |
| Equation of State | Constant Density |
| Energy | **Segregated Fluid Enthalpy** (exigido para reação intrafase) |

**Componentes.** Os íons não existem no banco Standard. Crie cada um copiando H₂O em *Material Databases* e renomeando. Ajuste a massa molar e a difusividade molecular. Densidade de todos = 997,05 kg/m³ (solução diluída).

| Componente | M (kg/kmol) | D_mol (m²/s), K&R Ap. A | Y inicial |
|---|---|---|---|
| H2O | 18,015 | — | 1 − ΣY |
| CO2L | 44,01 | 1,918e-9 | 1e-12 |
| OHM | 17,007 | 5,291e-9 | **5,328e-4** |
| HCO3M | 61,017 | 1,102e-9 | 1e-12 |
| CO3MM | 60,009 | 0,803e-9 | 1e-12 |
| NAP | 22,99 | 1,333e-9 | **7,203e-4** |
| HP (só na etapa C) | 1,008 | 9,31e-9 | 1e-15 |

**Entalpia:** cp = 4182 J/(kg·K) e entalpia de formação igual para todos os componentes. Com isso o calor de reação é nulo e o caso fica isotérmico. A hipótese é justificada: com [NaOH] = 0,03 M, o ΔT real é menor que 1 K. Turbulent Schmidt = 1, como em K&R.

### 3.2 Gás (disperso): `Gas`

| Grupo | Modelo |
|---|---|
| Material | **Multi-Component Gas**: **N2** e **CO2** |
| Reaction Regime | Non-reacting |
| Equation of State | Constant Density (N₂ 1,145; CO₂ 1,799 kg/m³) |
| Energy | Segregated Fluid Enthalpy |
| Optional | **Particle Size Distribution > S-Gamma**: Discrete Quadrature, **Two Equation**; Minimum Diameter **0,5 mm**; Maximum 10 mm |

Condição inicial: α_G = 0; Y_N2 = 1; d32 = 5,5 mm.

---

## 4. Interação Agua–Gas (Continuous-Dispersed)

Desative *Auto-select* e selecione:

| Modelo | Ajuste |
|---|---|
| Drag | **Tomiyama** (σ = 0,072 N/m) |
| Lift | **Tomiyama** (validado na coluna anterior) |
| Virtual Mass | coeficiente 0,5 |
| Turbulent Dispersion | Burns (padrão) |
| Wall Lubrication | Antal ou Hosokawa, se disponível. Faz parte do conjunto base de Rzehak; útil nesta coluna fina |
| Interaction Length Scale | **Sauter Mean Diameter** (S-Gamma) |
| Interaction Area Density | **Symmetric** (padrão; a = 6·α_L·α_G/d32) |
| S-Gamma Breakup / Coalescence | **desligados na base** (efeito dominante: dissolução); ligar na etapa D |
| Optional | **Interphase Mass Transfer > Interphase Reaction**; Reaction Regime = Reacting; Energy (Segregated Fluid Enthalpy) |

### 4.1 Reações interfaciais (absorção e dessorção do CO₂)

| Reação | Reagente (expoente) | Produto | Método | Coeficiente |
|---|---|---|---|---|
| **I1 Absorcao** | CO2 do Gas (1) | CO2L da Agua | User Reaction Coefficient | `${k_abs}` (m/s) |
| **I2 Dessorcao** | CO2L da Agua (1) | CO2 do Gas | User Reaction Coefficient | `${k_des}` (m/s) |

O STAR calcula ω = k·[X]·a_cd (Eq. 3569). Com isso, a taxa líquida fica **E·k_L·a·(He·C_G − C_L)**, idêntica à Eq. (9) de K&R. As field functions estão na seção 7.

---

## 5. Química no líquido (Complex Chemistry)

Crie as reações manualmente em *Agua > Models > Reacting > Reactions* (são poucas). Em todas: Arrhenius com **β = 0 e Ea = 0** (caso isotérmico), **Reversible** ativado e reversa por **Arrhenius Coefficients For Reverse Reaction**. A H2O entra com **expoente 0** (solvente em excesso).

Constantes a 25 °C (K&R, Ap. A; força iônica média I = 0,035 em k_I+; [Na⁺] = 0,0312 em K_II). Unidades SI do STAR (kmol, m³, s) e, entre parênteses, Chemkin (mol, cm³, s):

| Reação | Direta | Reversa |
|---|---|---|
| **R_I**: CO2L + OHM ⇌ HCO3M | **8,288e3 m³/(kmol·s)** (8,288e6) | **1,813e-4 s⁻¹** |
| **R_II**: HCO3M + OHM ⇌ CO3MM + H2O | **1,0e4 m³/(kmol·s)** (1,0e7)¹ | **1,548 s⁻¹** (H2O expoente 0) |
| *Etapa C:* **R_III**: CO2L + H2O ⇌ HCO3M + HP | **3,786e-2 s⁻¹** (H2O expoente 0) | **8,385e4 m³/(kmol·s)** (8,385e7) |
| *Etapa C:* **R_W**: HP + OHM ⇌ H2O | **1,4e8 m³/(kmol·s)** (1,4e11) | **1,383e-6 kmol/(m³·s)** (1,383e-9 mol/(cm³·s); H2O expoente 0) |

¹ K&R: o valor real é ~10¹⁰ m³/(kmol·s), mas **1e4 já não altera o resultado** e deixa o sistema muito menos rígido.

**Reacting System Properties:** Species Reaction Source Jacobian = **Numerical**. **Chemistry Acceleration: desligar Clustering** (as variáveis padrão são de combustão). ISAT e DMR também desligados.

Constantes completas e verificadas: `Programacao/coluna_reativa_darmana/resultados/constantes_star.json`.

---

## 6. Condições de contorno e iniciais

| Boundary | Tipo | Ajustes |
|---|---|---|
| **Aspersor** | Velocity Inlet | Gas: α = **0,35**, |u| = **0,40 m/s** (α·u = 0,14 m/s = U_G·A_coluna/A_aspersor); **Y_CO2 = `${Y_CO2_entrada}`**, Y_N2 = 1 − Y_CO2; d32 = **5,5 mm**. Agua: α = 0,65, |u| = 0; Y = composição inicial |
| **Topo** | Wall | Phase Conditions > Gas: **Phase Permeable** (degassing). Espécies com gradiente nulo |
| Fundo e paredes | Wall | No-slip para a água. Gás: free-slip, se a opção existir por fase (K&R) |

`${Y_CO2_entrada}` = `($Time >= 20) ? 1 : 0`: N₂ por 20 s para formar a pluma, depois CO₂ puro, como no experimento. **O t do pH é contado a partir da troca:** t_pH = $Time − 20.

---

## 7. Field functions

⚠️ Como na coluna anterior, **confira os nomes internos** na tabela *Reference* de cada field function antes de colar (ex.: `$MassFractionOHMAgua`, `$VolumeFractionGas`, `$SauterMeanDiameterGas`). Os nomes abaixo são **ilustrativos**.

**Constantes** (Scalar, sem dimensão, ou *Global Parameters*):

```
KW      = 9.878e-15          // (kmol/m3)^2
He      = 0.823              // C_L/C_G no equilíbrio (com salting-out, pH 12,5)
D_CO2   = 1.918e-9           // m2/s
D_OH    = 5.291e-9           // m2/s
delta   = 1.661              // sqrt(D_OH/D_CO2)
k1      = 8288.0             // m3/(kmol s)   (R_I+)
muL     = 8.907e-4 ; rhoL = 997.05
```

**Concentrações (kmol/m³):**

```
C_OH  = ${rhoL} * $MassFractionOHMAgua / 17.007
C_CO2L= ${rhoL} * $MassFractionCO2LAgua / 44.01
C_G   = $DensityGas * $MassFractionCO2Gas / 44.01
```

**Hidrodinâmica local:**

```
urel  = mag($$VelocityGas - $$VelocityAgua)
dB    = max($SauterMeanDiameterGas, 1e-4)
Re    = ${rhoL} * ${urel} * ${dB} / ${muL}
Sc    = ${muL} / (${rhoL} * ${D_CO2})
kL    = ${D_CO2} / ${dB} * (2 + 0.015 * pow(${Re}, 0.89) * pow(${Sc}, 0.7))      // Brauer (K&R)
// alternativa (etapa D): kL_Higbie = 2*sqrt(${D_CO2}*${urel}/(3.14159*${dB}))
```

**Fator de aumento** (DeCoursey + E_a de K&R, Ap. B; as mesmas fórmulas de `modelo_pontual.py`):

```
Ha    = sqrt(${k1} * ${D_CO2} * max(${C_OH}, 0)) / ${kL}
CAi   = max(${He} * ${C_G}, 1e-8)
chi   = max(${C_OH} / (2 * ${CAi}) * ${delta}, 1e-10)
Ea    = 1 + ${chi}/${delta} * (1 + 0.5*(${delta}-1) * (2/3.14159*atan(0.2*3.14159/2*log(exp(${chi})-1)) + 1))
aE    = ${Ea} - 1
E     = (${aE} < 1e-6) ? 1 : max(1, -pow(${Ha},2)/(2*${aE}) + sqrt(pow(${Ha},4)/(4*${aE}*${aE}) + ${Ea}*pow(${Ha},2)/${aE} + 1))
```

**Coeficientes das reações interfaciais (m/s).** A divisão por α_L recupera a área 6·α_G/d de K&R a partir da área simétrica do STAR (etapa D: testar sem ela):

```
k_abs = ${E} * ${kL} * ${He} / max($VolumeFractionAgua, 0.5)
k_des = ${E} * ${kL}       / max($VolumeFractionAgua, 0.5)
```

**Etapa B** (E constante): use `E_B = 1.4` no lugar de `${E}`.

**Diagnóstico:**

```
pH       = -log10(${KW} / max(${C_OH}, 1e-20))          // etapa B
pH_C     = -log10(max(${rhoL}*$MassFractionHPAgua/1.008, 1e-20))   // etapa C (H+ explícito)
Gamma    = ${E}*${kL}*$InteractionAreaDensityAguaGas*(${He}*${C_G} - ${C_CO2L})   // kmol/(m3 s)
Y_CO2_entrada = ($Time >= 20) ? 1 : 0
```

---

## 8. Relatórios, monitores e plots

| Objeto | Definição | Uso |
|---|---|---|
| **Point Probe "Sensor_pH"** | (0; 0,98; 0) m | Report Maximum de `pH`, `C_OH`, `E`, `Ha`, d32 → monitores a **cada passo** → plot pH × t |
| **Point Probe "PIV"** | (−0,05; 0,50; 0) m | v_y do gás a cada passo → FFT → **f_pluma** |
| **Line Probe "Lateral_750"** | x de −0,1 a 0,1 m em y = 0,75, z = 0 (101 pontos) | α_G e v_y do gás **médios no tempo** (Field Mean, 20–80 s na etapa A) |
| **Line Probe "Eixo"** | y de 0 a 1 m em x = z = 0 | **d32/d₀ médio no tempo** × Fig. 13 |
| Volume Average | α_G na região | **gas holdup integral** |
| Volume Integral | `Gamma` | taxa de absorção (kmol/s) |
| Report | Normalized Phase Mass Conservation Error (Gas) | conservação |

**Field Mean** (lembrete da coluna anterior: o Start é em **passos de tempo**, não em segundos).

---

## 9. Solver e execução

- **Δt = 5 ms**, como em K&R na hidrodinâmica, com 10 a 15 iterações internas e 2ª ordem no tempo. Conferir CFL < 1. Se a química ou o S-Gamma oscilarem, ir para 2 ms. K&R precisaram de 0,2 a 1 ms no CFX com química acoplada; no STAR o CVODE integra a química de forma rígida dentro do passo.
- Sub-relaxação (tutorial Hibiki): velocidade 0,4 a 0,7; pressão 0,2 a 0,3 (transiente); fração volumétrica 0,3 a 0,5; **S-Gamma igual à fração volumétrica**; espécies iguais à energia.
- **Etapa A:** 0 a 80 s com Y_CO2 = 0. Médias de 20 a 80 s.
- **Etapas B e C:** partir do estado da etapa A em t = 20 s (salvar o .sim nesse instante) e rodar até **t = 270 s** (250 s de CO₂). Médias de 20 a 95 s depois da troca, como em K&R.
- Custo estimado: 50 mil passos. Com 48 mil células e química, contar de dias a uma semana num desktop. A malha "Directed" de K&R (20 mil células) reduz isso a cerca de 1/3.

---

## 10. Critérios de validação

| Grandeza | Experimento | Simulações de referência | Meta |
|---|---|---|---|
| α_G (N₂) | 2,3 % | DBM 2,2 %; K&R 2,0 % | ± 15 % |
| f_pluma (N₂) | 0,17 Hz | DBM 0,17; K&R 0,14 | ± 20 % |
| α_G (CO₂) | 1,2 % | DBM 1,6 %; K&R 1,3 % | ± 20 % |
| f_pluma (CO₂) | 0,10 Hz | DBM 0,15; K&R 0,08 | — |
| t(pH 8) | 162 s | modelo pontual 167 s; K&R ≈ 20 % mais lento | **≤ 20 %** |
| d32/d₀ em z/H = 0,9 | 0,65 ± 0,03 | DBM ≈ 0,85; K&R entre os dois | tendência de queda |
| E máximo no sensor | — | K&R ≈ 1,5; pontual 1,51 | — |

Ao chegar a cada etapa, mande os CSV, como fizemos com a coluna anterior.

---

## 11. Etapa F: LES (planejamento)

Motivação: K&R concluem que o atraso de ~20 % no pH vem da **hidrodinâmica RANS**: a frequência da pluma sai baixa (0,14 Hz contra 0,17 Hz) e o tempo de residência das bolhas sai curto. A LES Euler–Lagrange de Darmana acerta a frequência. A pergunta da etapa F é **quanto do pH melhora só trocando RANS por LES**, com a mesma química.

| Item | Ajuste |
|---|---|
| Modelo | Turbulent > **Large Eddy Simulation > WALE Subgrid Scale**, All y+ (desligar o Auto-select). Verificar se o EMP aceita com Mixture Turbulence |
| Malha | **base = 5 mm (a mesma do RANS)** e uma variante de 4 mm. Critério Euler–Euler: Δ ≳ d_b (Milelli). Não usar 2,5 mm (menor que a bolha) |
| Verificação | No RANS da etapa A, plotar *Taylor Micro Scale* e *Kolmogorov Length Scale* no plano z = 0. No LES, k_res/k_sgs > 5, com k_res das Field Variances de u, v, w e k_sgs de *SGS Turbulent Kinetic Energy* |
| Convecção | **Bounded-Central** no momento (fator de upwind padrão); fração volumétrica como no RANS |
| Tempo | 2ª ordem; **Δt = 2–2,5 ms** (CFL ≈ 0,5–1 com u ~ 0,5 m/s); ≤ 15 iterações internas |
| Início | do **.sim RANS em t = 20 s** (troca de modelo no mesmo arquivo); descartar ~15 s (≈ 2 passagens da pluma) |
| Estatística | Field Mean de α_G e u_G; **Field Variance** de u, v, w (Reynolds normais); 60 s de amostragem para N₂ |
| Comparação | f_pluma, α_G, perfis em y = 750 mm (RANS × LES × experimento). Depois, com CO₂: pH(t) e d32(z) |
| Custo | ~3–5× o RANS na mesma malha (passo menor e central) |

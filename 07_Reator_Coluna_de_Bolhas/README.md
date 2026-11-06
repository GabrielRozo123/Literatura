# 07 — Reator de Coluna de Bolhas (Seminário de Cinética)

**Objetivo:** reunir as equações de projeto de uma coluna de bolhas, mostrar por que só elas não bastam (motivação para o CFD) e montar uma simulação Euler–Euler **curta** no STAR-CCM+ para comparar com a literatura.

| Item | Onde está |
|------|-----------|
| Equações de projeto + exemplo numérico | `Programacao/coluna_bolhas/projeto_coluna_bolhas.py` |
| Passo a passo do caso no STAR-CCM+ | [`SETUP_StarCCM.md`](SETUP_StarCCM.md) |
| Pós-processamento CFD × literatura | `Programacao/coluna_bolhas/compara_cfd_literatura.py` |
| **Resultados das rodadas CFD 2D** | [`RESULTADOS_CFD_2D.md`](RESULTADOS_CFD_2D.md) |
| Dados experimentais (a preencher) | `Programacao/coluna_bolhas/dados_experimentais.csv` |

---

## 1. O reator

A coluna de bolhas é um vaso vertical com líquido (ou suspensão), em que o gás é injetado pelo fundo através de um aspersor (prato perfurado, anel ou "spider"). Ela não tem partes móveis e a mistura é feita pelas próprias bolhas. Tem boa transferência de calor e massa e baixo custo. Aparece em oxidações em fase líquida (p-xileno, cicloexano), hidrogenações, cloração, Fischer–Tropsch (coluna de lama), fermentação aeróbia e tratamento de efluentes.

**Regimes de escoamento** (Besagni et al., 2018; Shah et al., 1982):

| Regime | U_G típico (ar–água) | Características |
|--------|----------------------|-----------------|
| Homogêneo (bolhas dispersas) | < 3–5 cm/s | bolhas pequenas e de tamanho parecido, εG cresce ~linearmente com U_G, pouca circulação |
| Transição | 3–8 cm/s | aparecem aglomerados e bolhas grandes |
| Heterogêneo (turbulento) | > 5–8 cm/s | bolhas grandes por coalescência, forte circulação do líquido ("gulf stream"), muita retromistura |
| Pistonado (slug) | colunas estreitas (D < 0,15 m) | bolhas do tamanho do tubo; não representa o equipamento industrial |

A velocidade de transição diminui quando os furos do aspersor ficam maiores (> 1–2 mm), a viscosidade aumenta ou há internos.

---

## 2. Equações de projeto

### 2.1 Retenção gasosa (gas holdup) εG

A retenção gasosa é a variável central: dela dependem a área interfacial, o tempo de residência do gás e a altura da dispersão.

**Akita & Yoshida (1973):**

```
εG/(1−εG)^4 = C · Bo^(1/8) · Ga^(1/12) · Fr
Bo = g D² ρL/σ    Ga = g D³/νL²    Fr = U_G/√(gD)
C = 0,20 (líquidos puros / não eletrólitos) ; 0,25 (eletrólitos)
Para D > 0,6 m, usar D = 0,6 m.
```

**Hikita et al. (1980):**

```
εG = 0,672 (U_G μL/σ)^0,578 (μL⁴ g/(ρL σ³))^−0,131 (ρG/ρL)^0,062 (μG/μL)^0,107
```

**Reilly et al. (1986)** (SI):  `εG = 296 U_G^0,44 ρL^−0,98 σ^−0,16 ρG^0,19 + 0,009`

**Modelo de deslizamento (drift-flux), regime homogêneo, líquido em batelada:**

```
U_G/εG = U∞ (1−εG)^(n−1)      (Wallis / Richardson–Zaki; U∞ ≈ 0,23 m/s p/ bolhas de 4–6 mm)
```

**Critérios de escala de Wilkinson et al. (1992):** εG não depende do tamanho da coluna quando **D > 0,15 m**, **H/D > 5** e **furos do aspersor > 1–2 mm**. Por isso podemos comparar o nosso CFD (D = 0,15 m) com dados de outras colunas que também atendam aos três critérios.

### 2.2 Bolhas, área interfacial e transferência de massa

```
d32/D = 26 Bo^−0,5 Ga^−0,12 Fr^−0,12            Akita & Yoshida (1974)
a     = 6 εG / d32                              (área interfacial, m²/m³)
U∞    = √(2σ/(ρL d) + g d/2)                    Mendelson (1967), d ≳ 2 mm
kL    = 2 √(DA · u_slip/(π d))                  penetração de Higbie
kLa·D²/DA = 0,6 Sc^0,5 Bo^0,62 Ga^0,31 εG^1,1   Akita & Yoshida (1973)
kLa   = 0,467 U_G^0,82   (ar–água, SI)          Shah et al. (1982)
```

### 2.3 Mistura da fase líquida

```
D_L = 2,7 D^1,4 U_G^0,3   [cm²/s; D em cm; U_G em cm/s]   Deckwer et al. (1974)
D_L = 0,35 D^(4/3) (g U_G)^(1/3)   [SI]                    Baird & Rice (1975)
V_L(eixo) = 0,21 √(gD) (U_G³/(g νL))^(1/8)                 Riquarts (1981)
```

O perfil de velocidade do líquido sobe no centro e desce junto à parede, com inversão em r/R ≈ 0,7. É essa circulação que gera o D_L alto, e é ela que o CFD resolve.

### 2.4 Cinética + transferência de massa: a equação de projeto do reator

Reação gás–líquido A(g) + bB(l) → P, com A se dissolvendo e reagindo no líquido (Levenspiel, 1999, cap. 23–24). Resistências em série:

```
           p_A
−r_A = ─────────────────────────────────────────────  (por volume de reator)
        1/(k_Ag a) + H_A/(k_Al a E) + H_A/(k C_B εL)

Ha = √(k1 DA)/kL       (número de Hatta, pseudo-1ª ordem k1 = k C_B)
Ha < 0,3   → reação LENTA no seio do líquido: o projeto depende de kLa e εL (hidrodinâmica!)
0,3–3      → intermediária
Ha > 3     → RÁPIDA, ocorre no filme: o projeto depende da área a e do fator de aumento E ≈ Ha
```

**Modelo de projeto 1: gás pistonado + líquido misturado (semibatelada, regime lento).** Balanço do gás `U_G dC_G/dz = −kLa(C_G/He − C_L)` e do líquido `kLa⟨C_G/He − C_L⟩ = k1 εL C_L`. A solução analítica está no script:

```
St = kLa H/(He U_G)        Φ = kLa(1 − e^−St)/St
C_L/C* = Φ/(Φ + k1 εL)      X_A,gás = (1 − C_L/C*)(1 − e^−St)
```

**Modelo de projeto 2: líquido contínuo com dispersão axial (ADM), 1ª ordem, CC de Danckwerts:**

```
X = 1 − 4a e^(Pe/2) / [(1+a)² e^(aPe/2) − (1−a)² e^(−aPe/2)]
a = √(1 + 4Da/Pe)    Da = k1 τ    Pe = u_L H/D_L
Pe → 0: CSTR   |   Pe → ∞: PFR
```

Para D = 0,15 m e U_G = 2 cm/s, o script dá **Pe ≈ 0,3**, ou seja, a fase líquida se comporta quase como um CSTR (X_ADM = 0,66 contra X_PFR = 0,84, com Da = 1,8). A conversão depende diretamente de D_L, e D_L vem da circulação do líquido.

---

## 3. Por que precisamos de CFD

1. **As correlações discordam entre si.** Com ar–água a 2 cm/s, Akita & Yoshida dão εG = 0,055, Hikita 0,062 e Reilly 0,105, uma diferença de quase **2×** (ver `fig_holdup_correlacoes.png`). Cada uma foi ajustada a um aspersor, uma faixa de D e um sistema específicos.
2. **Ampliação de escala.** Colunas industriais têm D de 3 a 10 m, operam com pressão, internos (trocadores de calor) e líquidos reais (eletrólitos, surfactantes, sólidos). Isso fica fora da faixa das correlações de laboratório.
3. **O projeto depende de grandezas locais.** O perfil radial de εG provoca a circulação do líquido, e a circulação define a retromistura (D_L), as zonas mortas e a distribuição de tempos de residência. A seletividade de reações em série ou paralelas e os pontos quentes de reações exotérmicas dependem desses campos locais, não das médias.
4. **Projeto de aspersor e internos.** Mudar o tipo de aspersor, o diâmetro dos furos ou colocar tubos muda o regime e a transição. O CFD avalia cada alternativa antes de construir.
5. **Acoplamento com a cinética.** O CFD pode resolver espécies na fase líquida com transferência de massa local (kLa(r, z)) e reação, o que é o passo natural para depois deste seminário.

**Limitações do CFD Euler–Euler** (a mencionar na apresentação):

- as forças interfaciais (arrasto, sustentação, lubrificação de parede, dispersão turbulenta) precisam de modelos de fechamento;
- o coeficiente de sustentação **muda de sinal** perto de d ≈ 5,8 mm (Tomiyama et al., 2002), então o diâmetro de bolha escolhido decide se o gás se concentra na parede ou no centro;
- no regime heterogêneo é preciso um balanço populacional (coalescência e quebra);
- a solução é transiente e as médias temporais precisam ser longas;
- **sempre é preciso validar**.

Draw & Rzehak (2024) mostram que o modelo "baseline" do HZDR funciona até εG ≈ 20%; acima disso é preciso uma correção de enxame no arrasto.

---

## 4. Literatura recente para validação

| # | Referência | Por que interessa | Status |
|---|------------|-------------------|--------|
| 1 | Draw & Rzehak (2024), *IJMF* 181:104969 | Euler–Euler × experimento, coluna redonda D = 0,288 m, H = 2,5 m, regime homogêneo até εG ~ 50% | 🔲 Pegar PDF (acesso aberto) |
| 2 | Sommer et al. (2023), *Chem. Eng. Technol.* — Hydrodynamics in a Bubble Column, Part 1 | Banco de dados HZDR para validar CFD: d_b, εG, velocidades vs. U_G e diâmetro do orifício | 🔲 Pegar PDF |
| 3 | (autores a conferir, 2023), *J. Braz. Soc. Mech. Sci. Eng.* 45(10), doi:10.1007/s40430-023-04433-1 — εG global experimental × CFD | Brasileiro (FAPESP), coluna quadrada; mostra que a força de sustentação melhora o εG | 🔲 Conferir autores/PDF |
| 4 | Besagni & Inzoli (2016), *CES* 146:259–290 | D = 0,24 m, H = 5,3 m, U_G de 0,004 a 0,20 m/s: εG global, transição, d_b | 🔲 Pegar PDF |
| 5 | Besagni, Inzoli & Ziegenhein (2018), *ChemEngineering* 2:13 | Revisão completa: regimes, correlações, kLa | 🔲 Ler (acesso aberto) |
| 6 | Rzehak, Krauß, Kováts & Zähringer (2017), *IJMF* — "Fluid dynamics in a bubble column: new experiments and simulations" | Modelo "baseline" HZDR de forças interfaciais × experimento (dados citados de memória: conferir) | 🔲 |
| 7 | Deen, Solberg & Hjertager (2001), *CES* 56:6341 | Benchmark clássico (coluna quadrada de 0,15 m), muito usado com o STAR-CCM+ | Referência |
| — | Akita & Yoshida (1973, 1974); Hikita et al. (1980); Shah et al. (1982); Deckwer et al. (1974); Wilkinson et al. (1992); Tomiyama et al. (2002); Levenspiel (1999) | Equações de projeto (seção 2) | Usadas no script |

> ⚠️ O ambiente de nuvem onde este material foi preparado não conseguiu abrir o texto completo dos artigos 1–5. As tabelas de εG × U_G ainda **não** foram extraídas. Baixe os PDFs pela UNICAMP (Portal CAPES) e preencha `dados_experimentais.csv`, usando a tabela do artigo ou digitalizando a figura com o WebPlotDigitizer.

Entradas BibTeX: `references.bib` (bloco "07 — COLUNA DE BOLHAS"). Os campos marcados `TBD` ainda precisam ser conferidos.

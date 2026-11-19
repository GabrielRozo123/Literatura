# Equações cinéticas de projeto: reator de coluna de bolhas

**Seminário de Cinética, FEQ/UNICAMP** · Gabriel Rozo
**Implementação:** `Programacao/coluna_bolhas/cinetica_projeto.py` (regimes, fator de aumento, altura de projeto) e `projeto_coluna_bolhas.py` (hidrodinâmica, modelos de reator)
**Base:** Levenspiel (1999, cap. 23–24), Danckwerts (1970), Deckwer (1992), Shah et al. (1982), Kantarci et al. (2005)

---

## 0. Ideia central

Numa coluna de bolhas, a taxa observada **não é** a taxa intrínseca da reação. O reagente gasoso precisa:

```
gás (bolha) ─► filme gasoso ─► interface (Henry) ─► filme líquido ─► seio do líquido
                  k_G a              C* = p/H              k_L a·E           k1 εL
```

A equação de projeto combina **cinética** (k, ordem, Ha) com **hidrodinâmica** (εG, a, kL, D_L) e com um **modelo de escoamento** das fases (pistonado, mistura perfeita ou dispersão axial). As correlações, ou o CFD, entram exatamente nos parâmetros hidrodinâmicos.

---

## 1. Nomenclatura

| Símbolo | Significado | Unidade |
|---------|-------------|---------|
| A, B | reagente gasoso (dissolve) e reagente líquido; A(g) + b B(l) → P | — |
| p_A, C_G | pressão parcial / concentração de A no gás | Pa, mol/m³ |
| C* = p_A/H_A | concentração de A na interface, no equilíbrio (lei de Henry) | mol/m³ |
| He = H_A/(RT) | constante de Henry adimensional (C_G/C*) | — |
| C_L, C_B | concentrações de A e de B no seio do líquido | mol/m³ |
| k₂, k₁ = k₂C_B | constantes de 2ª ordem e de pseudo-1ª ordem | m³/(mol·s), 1/s |
| εG, εL = 1−εG | retenção de gás / de líquido | — |
| a = 6εG/d₃₂ | área interfacial por volume de dispersão | m²/m³ |
| k_L, k_G | coeficientes de filme (lado líquido / lado gás) | m/s |
| D_A, D_B | difusividades no líquido | m²/s |
| E | fator de aumento (*enhancement*) | — |
| U_G, u_L | velocidades superficiais | m/s |
| D_L | coeficiente de dispersão axial do líquido | m²/s |
| H | altura da dispersão | m |

---

## 2. Taxa de transferência com reação: as resistências em série

**Equação geral (Levenspiel, 1999, cap. 23)**, por volume de reator, com reação de pseudo-1ª ordem em A:

```
                         p_A
 −r_A''' = ───────────────────────────────────────────────          (1)
            1/(k_G a)  +  H_A/(k_L a E)  +  H_A/(k₁ εL)
            └─filme gás─┘ └─filme líquido─┘ └─reação no seio─┘
```

- Para gases pouco solúveis (O₂, CO₂, H₂, N₂), o termo 1/(k_G a) é desprezível.
- Em concentração (C* = p_A/H_A), resulta na **constante global** K:

```
 −r_A''' = K · C*         1/K = 1/(k_L a E) + 1/(k₁ εL)               (2)
```

### 2.1 Número de Hatta: onde a reação acontece

```
 Ha = √(k₁ D_A) / k_L  = (taxa máxima de reação no filme) / (taxa máxima de difusão no filme)     (3)
```

### 2.2 Fator de aumento E

- **Pseudo-1ª ordem** (B em excesso, E ≪ Ei):

  ```
  E = Ha / tanh(Ha)                                                      (4)
  ```

- **Fator instantâneo** (limite em que A e B se encontram num plano de reação dentro do filme):

  ```
  Ei = 1 + D_B C_B / (b D_A C*)                                          (5)
  ```

- **Caso geral de 2ª ordem: van Krevelen–Hoftijzer**, resolvido iterativamente:

  ```
  E = Ha·√[(Ei−E)/(Ei−1)] / tanh{ Ha·√[(Ei−E)/(Ei−1)] }                   (6)
  ```

### 2.3 Regimes e o que controla o projeto

| Regime | Critério | Taxa por volume | O projeto depende de… | Hidrodinâmica relevante |
|--------|----------|-----------------|------------------------|-------------------------|
| **Lento, controle cinético** | Ha < 0,3 e k₁εL ≪ k_La | −r = k₁ εL C* | volume de **líquido** (εL) | quase nada: bastam H e εL |
| **Lento, controle por TM** | Ha < 0,3 e k₁εL ≫ k_La | −r = k_La C* | **k_La** | εG, d_b, k_L → CFD/correlação |
| Lento (geral) | Ha < 0,3 | Eq. (2) com E = 1 | k_La e k₁εL | |
| Intermediário | 0,3 < Ha < 3 | Eq. (2) com E da Eq. (4) | tudo | |
| **Rápido** | 3 < Ha < Ei/10 | −r = **a C* √(k₁ D_A)** | **a** (k_L desaparece!) | εG e d_b (área) |
| **Instantâneo** | Ha > 10 Ei | −r = k_L a C* Ei | k_La e C_B | εG, d_b, k_L |

> **Mensagem para o seminário:** a cinética define o regime (Ha), e o regime define qual parâmetro hidrodinâmico precisa ser conhecido com precisão. No regime rápido, por exemplo, errar a área interfacial em 2× significa errar o reator em 2×.

---

## 3. Modelos de escoamento: as equações de projeto

### 3.1 Gás pistonado, reação local (o modelo mais usado para absorção)

Balanço de A na fase gás, em regime estacionário, com gás ideal e queda de pressão e contração do gás desprezíveis:

```
 U_G dC_G/dz = −K C_G / He                                              (7)

 ⇒  X_A = 1 − exp[ −K H / (He U_G) ]                                     (8)

 ⇒  H = He U_G ln[1/(1−X_A)] / K        (altura de dispersão para conversão X_A)     (9)
```

Na forma integral (Levenspiel, 1999, cap. 24), útil quando K varia com a composição:

```
 H = (U_G / RT) ∫ dp_A / (−r_A''')     (de p_saída a p_entrada)             (10)
```

### 3.2 Gás pistonado + líquido perfeitamente misturado (semibatelada, regime lento)

```
 Gás:       U_G dC_G/dz = −k_La (C_G/He − C_L)
 Líquido:   k_La ⟨C_G/He − C_L⟩_H = k₁ εL C_L

 St = k_La H/(He U_G),   Φ = k_La (1 − e^−St)/St
 C_L/C* = Φ/(Φ + k₁εL),   X_A = (1 − C_L/C*)(1 − e^−St)                    (11)
```

### 3.3 Fase líquida contínua: o efeito da retromistura

Reação de 1ª ordem no líquido (reagente B, ou A quando o gás está em excesso), com balanço no líquido pelo **modelo de dispersão axial** e condições de contorno de Danckwerts:

```
 D_L d²C/dz² − u_L dC/dz − k₁ C = 0

 X = 1 − 4a e^(Pe/2) / [(1+a)² e^(aPe/2) − (1−a)² e^(−aPe/2)]              (12)
 a = √(1 + 4Da/Pe),   Da = k₁ τ,   τ = εL H/u_L,   Pe = u_L H/D_L
 Limites:  Pe → 0 ⇒ CSTR  X = Da/(1+Da);   Pe → ∞ ⇒ PFR  X = 1 − e^(−Da)
```

**D_L** pode vir de correlações (Deckwer 1974: D_L = 2,7 D^1,4 U_G^0,3 em cgs; Baird & Rice 1975) ou da **circulação calculada no CFD** (Joshi 1980: D_L ≈ 0,31 V_c D).

### 3.4 Modelo completo: dispersão axial nas duas fases (Deckwer, 1992)

```
 Gás:      D_G εG C_G'' − U_G C_G' − k_La (C_G/He − C_L) = 0
 Líquido:  D_L εL C_L'' + u_L C_L' + k_La (C_G/He − C_L) − k₁ εL C_L = 0         (13)
 + CC de Danckwerts nas duas extremidades (problema de contorno, solução numérica)
```

É o modelo de projeto "completo". Os parâmetros εG, k_La, D_L e D_G são exatamente o que as correlações (ou o CFD) fornecem.

### 3.5 Coluna de lama (três fases, catalisador sólido): ligação com LHHW

Para reação catalítica (hidrogenação, Fischer–Tropsch), entra mais uma resistência, a líquido–sólido, e a taxa intrínseca no catalisador:

```
                          C*
 −r_A''' = ──────────────────────────────────────────                     (14)
            1/(k_La) + 1/(k_s a_s) + 1/(η k w)
 (η = fator de efetividade da partícula; w = carga de catalisador; a cinética
  intrínseca pode ser LHHW, linearizada em torno da condição de operação)
```

### 3.6 Balanço de energia (reação exotérmica)

```
 0 = D_L εL ρ c_p T'' + u_L ρ c_p T' + (−ΔH)(−r) − (4 h_w/D)(T − T_c)       (15)
 h_w (parede/serpentina): St = h_w/(ρ c_p U_G) = 0,1 (Re Fr Pr²)^(−1/4)   (Deckwer, 1980; conferir)
```

A alta retromistura (Pe pequeno) torna a coluna quase isotérmica. Essa é uma das razões do seu uso em oxidações exotérmicas.

---

## 4. Algoritmo de projeto

```
1. Cinética: k₂ (ou k₁), ordem, ΔH, estequiometria b            ← laboratório/literatura
2. Propriedades: H_A (Henry), D_A, D_B, ρ, μ, σ
3. Escolher D e U_G (regime homogêneo: U_G < U_trans ≈ 2,5–4 cm/s)
4. HIDRODINÂMICA → εG, d₃₂, a = 6εG/d₃₂, k_L, k_La, D_L         ← CORRELAÇÕES ou CFD
5. Ha (Eq. 3), Ei (Eq. 5) → regime → E (Eq. 4/6)
6. Modelo de escoamento (3.1–3.4) → H para a conversão desejada
7. Verificações: regime de escoamento coerente com U_G; H/D > 5; ΔT; Ha coerente com o modelo
8. Iterar (H e U_G mudam εG, D_L, …)
```

> O passo 4 é a fonte de incerteza: as correlações discordam até 2× (seção 3 do README). O passo 5 mostra quando isso importa.

---

## 5. Exemplo numérico (U_G = 2 cm/s, D = 0,15 m, 25 °C)

`python cinetica_projeto.py`, figura `resultados/fig_cinetica_projeto.png`.

Hidrodinâmica de quatro fontes:

| Fonte | εG | d_b [mm] | a [m⁻¹] | k_La (O₂) [s⁻¹] |
|-------|-----|----------|---------|-----------------|
| Correlação (Akita & Yoshida) | 0,055 | 6,1 (A&Y 1974) | 54 | 0,021 |
| Exp. Besagni & Inzoli (2016), aspersor *spider* | 0,069 | 3,5 (Figs. 19–21) | 118 | 0,056 |
| Exp. Mudde et al. (2009), aspersor de agulhas | 0,089 | 4,25 | 126 | 0,047 |
| **CFD STAR-CCM+ (rodada 4)** | **0,086** | 5,0 | 103 | 0,036 |

(k_L de Higbie com velocidade de deslizamento U_G/εG.)

**Exemplo 1: O₂ com consumo lento no líquido** (k₁ = 0,05 s⁻¹, típico de oxidação biológica; Ha ≈ 0,03, regime **lento**, misto cinética/TM):

| Fonte | K [s⁻¹] | Volume relativo para a mesma conversão |
|-------|---------|----------------------------------------|
| Correlação | 0,0147 | 1,00 |
| Besagni | 0,0253 | 0,58 |
| Mudde | 0,0232 | 0,63 |
| CFD | 0,0202 | 0,73 |

**Exemplo 2: CO₂ (10 % em ar) em NaOH 0,1 M**
- Cinética: CO₂ + OH⁻ → HCO₃⁻, com k_OH ≈ 8×10³ m³/(kmol·s) a 25 °C (Pohorecki & Moniuk, 1988), o que dá k₁ = 800 s⁻¹.
- Ha ≈ 3–3,7, regime **rápido**. Ei ≈ 44 ≫ Ha, então vale o pseudo-1ª ordem.

| Fonte | E | K = k_La·E [s⁻¹] | H para 95 % de remoção [m] | Volume relativo |
|-------|---|------------------|----------------------------|-----------------|
| Correlação | 3,2 | 0,065 | 1,16 | 1,00 |
| Besagni | 2,7 | 0,144 | 0,52 | 0,45 |
| Mudde | 3,4 | 0,151 | 0,50 | 0,43 |
| CFD | 3,6 | 0,123 | 0,61 | 0,53 |

**Leitura:**

1. No regime **rápido** (CO₂/NaOH), a taxa é a·C*·√(k₁D_A). O projeto depende **só da área interfacial**. Projetar pela correlação clássica superdimensiona o reator em **~2×** em relação aos experimentos. O CFD fica a 20 % dos dados experimentais.
2. No regime **lento** com TM relevante (O₂), o projeto depende de k_La. As diferenças são de 30–40 %.
3. Se k₁ fosse muito menor (controle cinético puro), as quatro fontes dariam o **mesmo** reator. Nesse caso a hidrodinâmica não importa, e nenhum CFD é necessário.

> **Ressalvas:** k_L de Higbie supõe interface móvel; em sistemas contaminados ou com eletrólitos, k_L é menor e a coalescência é inibida (bolhas menores). O valor de k_OH depende da força iônica e da temperatura. D_L de Joshi foi usado com a constante 0,31, que precisa ser conferida no original.

## 5b. Estudo de caso: CO₂ puro em NaOH, semibatelada (o regime muda no tempo)

`python caso_co2_naoh.py` → `resultados/caso_co2_naoh.{json,csv}` e `fig_caso_co2_naoh.png`.

Sistema-referência da literatura recente de colunas reativas: experimento de Darmana et al. (2007); modelos de E de Krauß & Rzehak (2017); Euler–Euler reativo de Krauß & Rzehak (2018) e Liu et al. (2021); modelo de projeto de Michelson et al. (2023). Aqui a mesma química é aplicada à nossa coluna.

**Condições.** CO₂ puro a 1 atm (C* = 34 mol/m³) em NaOH 31,6 mol/m³ (pH 12,5); D = 0,15 m, H₀ = 0,9 m, U_G = 2 cm/s; 25 °C.

**Modelo** (quatro blocos acoplados, BDF):
1. Hidrodinâmica: εG, d_b → a = 6εG/d_b; k_L de Higbie.
2. Ha = √(k_OH[OH⁻]D_CO₂)/k_L; Ei = 1 + D_OH[OH⁻]/(2D_CO₂C*); E de van Krevelen–Hoftijzer, recalculados a cada instante.
3. Gás pistonado com bolhas que encolhem (CO₂ puro): F(H) = F₀·exp(−λH_D), λ = N·a₀/F₀.
4. Líquido bem misturado: balanços de CO₂ dissolvido e de carbono iônico. Rede: CO₂ + OH⁻ ⇌ HCO₃⁻ (Pohorecki & Moniuk, 1988); CO₂ + H₂O (k_w ≈ 0,03 s⁻¹); HCO₃⁻/CO₃²⁻ em equilíbrio. pH pelo balanço de cargas.

| Hidrodinâmica | εG | a [m⁻¹] | k_La [s⁻¹] | Ha₀ | Ei₀ | E₀ | absorção inicial | t (pH 10) | t (pH 8,3) | Ha < 0,3 em |
|---|---|---|---|---|---|---|---|---|---|---|
| Correlação (Akita & Yoshida) | 0,055 | 54 | 0,0205 | 1,84 | 2,28 | 1,56 | 72 % | 44 s | 66 s | 30 s |
| CFD validado | 0,086 | 103 | 0,0347 | 2,07 | 2,28 | 1,63 | 90 % | 34 s | 50 s | 24 s |

**Leitura.**
- A hidrodinâmica do CFD reduz em ~24 % o tempo de batelada até pH 8,3.
- O regime **muda durante a batelada**:
  - no início é intermediário (Ha ≈ 2, E ≈ 1,6, limitado por Ei);
  - quando o OH⁻ cai, Ha < 0,3 e o controle passa a ser por transferência de massa (E = 1, taxa = k_La·C*);
  - depois que o carbonato vira bicarbonato, resta absorção física.
- Portanto, o parâmetro hidrodinâmico que governa a taxa (a, depois k_La) também muda com o tempo.

**Tabela de projeto por regime** (usada nos slides "Taxa de consumo" e "Equações de projeto"). Hipóteses: altura com A diluído e B em excesso; tempo de batelada com C* constante e líquido bem misturado; β = b·D_A·C*/D_B.

| Regime | −r_A | Altura (gás pistonado) | Tempo de batelada para consumir B |
|---|---|---|---|
| Lento, cinético (k₁ε_L ≪ k_La) | k₁ε_L C* | He U_G ln[1/(1−X)]/(k₁ε_L) | ln(C_B0/C_B)/(b k₂ C*) |
| Lento, TM (Ha < 0,3; k₁ε_L ≫ k_La) | k_La C* | He U_G ln[1/(1−X)]/(k_La) | ε_L(C_B0 − C_B)/(b k_La C*) |
| Rápido (3 < Ha ≪ Ei) | a C* √(k₂C_B D_A) | He U_G ln[1/(1−X)]/(a√(k₂C_B D_A)) | 2ε_L(√C_B0 − √C_B)/(b a C* √(k₂D_A)) |
| Instantâneo (Ha ≫ Ei) | k_La (C* + D_B C_B/(b D_A)) | (He U_G/k_La) ln[(C_AG0+γ)/(C_AG0(1−X)+γ)], γ = He D_B C_B/(b D_A) | (ε_L D_A/(k_La D_B)) ln[(C_B0+β)/(C_B+β)] |

> Correção (v3): no instantâneo a taxa k_La(C* + D_B C_B/(b D_A)) não é proporcional a C*, então a altura exata é a forma com γ. A forma antiga, He U_G ln[1/(1−X)]/(k_La Ei), só vale com Ei constante.

## 5c. Generalização: estequiometria, ordem (m, n) e reação reversível

`python projeto_generico.py` confere as formas fechadas contra a integral numérica (`scipy.quad`). O maior desvio é 7×10⁻⁹ para m = 0,5–2, n = 0–3 e os quatro regimes. O script também resolve um caso reversível pela integral.

**Reação e o b.** ν_A A(g→l) + ν_B B(l) ⇌ ν_C C(l) + ν_D D(l).
- Usamos ν para não confundir com a área interfacial a.
- Na base de 1 mol de A absorvido: A + b B ⇌ c C + d D, com b = ν_B/ν_A, c = ν_C/ν_A, d = ν_D/ν_A.
- b = mols de B consumidos por mol de A, logo −r_B = b(−r_A).
- Exemplos: CO₂ + 2OH⁻ → CO₃²⁻ + H₂O (b = 2, o fator 2 do Ei no estudo de caso); CO₂ + OH⁻ → HCO₃⁻ (b = 1); O₂ + 2SO₃²⁻ → 2SO₄²⁻ (b = 2).

**Lei de velocidade (por volume de líquido).** r = k C_A^m C_B^n − k' C_C^p C_D^q.
- Irreversível: k' = 0. Elementar: k/k' = K_c.

**Estequiometria do líquido em batelada.** C_B = C_B0(1−X_B), C_C = C_C0 + (c/b)C_B0 X_B, C_D = C_D0 + (d/b)C_B0 X_B.

**Equações de projeto gerais** (−r_A por volume de reator; valem para qualquer cinética):

| Caso | Equação |
|---|---|
| Líquido em batelada (C* constante) | t = (ε_L C_B0/b) ∫₀^{X_B} dX_B/(−r_A) |
| Gás pistonado (A diluído, U_G ≈ cte) | H = U_G C_AG0 ∫₀^{X_A} dX_A/(−r_A), com C* = C_AG0(1−X_A)/He; V_R = A_T H |
| Líquido contínuo (CSTR) | V_R = Q_L C_B0 X_B / [b (−r_A)_saída] |

O −r_A dentro da integral depende do regime:
- **lento, cinético:** −r_A = ε_L[k C*^m C_B^n − k' C_C^p C_D^q];
- **caso geral, com filme:** −r_A = k_L a E (C* − C_A,e).

**Reversível.**
- A integral diverge na conversão de equilíbrio X_Be, onde −r_A = 0.
- Exemplo A + B ⇌ C no regime cinético, com κ = K_c C* e τ = b k C* t: X_B → κ/(1+κ). A integral numérica dá X_B(τ = 4) = 0,795 para κ = 4 e 0,500 para κ = 1.
- No regime com filme, E depende também de K (Danckwerts, 1970), e a linearização de Hikita–Asai não vale em geral para reações reversíveis.

**Formas fechadas (irreversível, ordem m em A e n em B).** Use ln[1/(1−X)] quando o expoente vale 1.

| Regime | −r_A | t(X_B) | H(X_A) |
|---|---|---|---|
| Lento, cinético | ε_L k C*^m C_B^n | [(1−X_B)^{1−n} − 1] / [(n−1) b k C*^m C_B0^{n−1}] | U_G He^m C_AG0^{1−m} [(1−X_A)^{1−m} − 1] / [(m−1) ε_L k C_B^n] |
| Lento, TM | k_La C* | ε_L C_B0 X_B / (b k_La C*) | (He U_G/k_La) ln[1/(1−X_A)] |
| Rápido (Hikita & Asai, 1964) | a √[2/(m+1)·k D_A C*^{m+1} C_B^n] | ε_L C_B0^{1−n/2} [1 − (1−X_B)^{1−n/2}] / [(1−n/2) b a √(2/(m+1)·k D_A C*^{m+1})] | U_G He^p C_AG0^{1−p} [(1−X_A)^{1−p} − 1] / [(p−1) a √(2/(m+1)·k D_A C_B^n)], p = (m+1)/2 |
| Instantâneo | k_La (C* + D_B C_B/(b D_A)) | (ε_L D_A/(k_La D_B)) ln[(C_B0+β)/(C_B0(1−X_B)+β)], β = b D_A C*/D_B | (He U_G/k_La) ln[(C_AG0+γ)/(C_AG0(1−X_A)+γ)] |

**Conversão explícita** (invertendo as expressões acima):
- cinético, n ≠ 1: X_B = 1 − [1 + (n−1) b k C*^m C_B0^{n−1} t]^{1/(1−n)};
- cinético, n = 1: X_B = 1 − exp(−b k C*^m t);
- controle por TM: X_B = b k_La C* t/(ε_L C_B0), linear até X_B = 1;
- gás pistonado com m = 1: X_A = 1 − exp(−ε_L k C_B^n H/(He U_G)).

**Ordem aparente** (por que a cinética "falsificada" engana):

| Regime | ordem em A | ordem em B | E_a aparente |
|---|---|---|---|
| Lento, cinético | m | n | E_a |
| Lento, TM | 1 | 0 | baixa (difusão) |
| Rápido | (m+1)/2 | n/2 | ≈ (E_a + E_D)/2 |
| Instantâneo | 0 a 1 | 0 a 1 | baixa (difusão) |

---

## 6. Referências desta seção

Levenspiel (1999), cap. 23–24 · Danckwerts (1970), *Gas–Liquid Reactions* · van Krevelen & Hoftijzer (1948) · Deckwer (1992), *Bubble Column Reactors* · Shah et al. (1982) · Pohorecki & Moniuk (1988) · Joshi (1980) · Akita & Yoshida (1973, 1974) · Besagni & Inzoli (2016) · Draw & Rzehak (2024) / Mudde et al. (2009) · Darmana et al. (2007) · Krauß & Rzehak (2017, 2018) · Liu et al. (2021) · Michelson et al. (2023) · Hikita & Asai (1964). Entradas em `references.bib`; campos `TBD` ainda a conferir.

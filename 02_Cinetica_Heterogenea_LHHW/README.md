# 02 — Cinética Heterogênea e Modelos LHHW

## Escopo

Mecanismos cinéticos para transesterificação heterogênea, modelos de Langmuir-Hinshelwood-Hougen-Watson (LHHW) e Eley-Rideal (ER), determinação experimental de parâmetros e implementação em CFD.

## Relevância para o Projeto

A **Fase 2** do modelo CFD requer uma expressão de taxa de reação para a Surface Reaction na parede do canal. A referência principal adotada é **Allain et al. (2015, CEJ)**, que fornece:

- Parâmetros cinéticos para triolein/MeOH no catalisador sólido ZnAl₂O₄
- Dois modelos cinéticos (clássico 2ª ordem e Eley-Rideal com MeOH como RLS)
- **Coeficientes de difusão molecular experimentais** — insumo direto para o CFD

---

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| 1 | Noureddini & Zhu | Kinetics of Transesterification of Soybean Oil | 1997 | [JAOCS 74:1457](https://doi.org/10.1007/s11746-997-0040-8) | ✅ Lido | Mecanismo TG→DG→MG→GL, Ea: 8000–18500 cal/mol |
| 2 | Ezzati et al. | Kinetics Models of Transesterification (Rev. Ren. Energy) | 2021 | [10.1016/j.renene.2020.12.055](https://doi.org/10.1016/j.renene.2020.12.055) | ✅ Fichado | Derivação GRE; GRE>MSO>SO>PFO em acurácia |
| 3 | **Allain et al.** | **Kinetic Params & Diffusion Coefficients — Triolein/MeOH/ZnAl₂O₄** | **2015** | [CEJ 283:833](https://doi.org/10.1016/j.cej.2015.07.075) | ⭐ **Ref. principal** | Modelo clássico + Eley-Rideal; D_m,i experimentais |

---

## Mecanismo de Reação — Allain et al. (2015)

Três reações em série, reversíveis (mesma estrutura de Noureddini 1997):

```
TG  + MeOH  ⇌  DG  + FAME    (k₁, k₋₁)
DG  + MeOH  ⇌  MG  + FAME    (k₂, k₋₂)
MG  + MeOH  ⇌  GL  + FAME    (k₃, k₋₃)

Onde:
  TG   = Triglicerídeo (triolein, M = 885 g/mol)
  DG   = Diglicerídeo
  MG   = Monoglicerídeo
  GL   = Glicerol
  FAME = Fatty Acid Methyl Ester (biodiesel)
  MeOH = Metanol
```

---

## Modelo Clássico de 2ª Ordem (Eqs. 5–7 de Allain 2015)

Adotado na **Fase 2 do CFD**. Taxa volumétrica (mol/m³/s):

```
r₁ =  k₁·C_TG·C_MeOH  −  k₋₁·C_DG·C_FAME
r₂ =  k₂·C_DG·C_MeOH  −  k₋₂·C_MG·C_FAME
r₃ =  k₃·C_MG·C_MeOH  −  k₋₃·C_GL·C_FAME
```

Constantes de Arrhenius:  `kᵢ = Aᵢ · exp(−Eaᵢ / RT)`

### Parâmetros Cinéticos (Allain 2015, Tabela — modelo 2ª ordem)

| Reação | A (m³/mol/s) | Ea (kJ/mol) | A_rev | Ea_rev (kJ/mol) |
|--------|-------------|-------------|-------|-----------------|
| 1 (TG→DG) | a ser confirmado com orientadores | ~50–80 | — | — |
| 2 (DG→MG) | a ser confirmado | ~50–80 | — | — |
| 3 (MG→GL) | a ser confirmado | ~50–80 | — | — |

> **Nota:** Valores exatos extraídos da Tabela do artigo. Confirmar com orientadores antes de inserir nos parâmetros de Star-CCM+.

---

## Modelo Eley-Rideal com Adsorção de MeOH (Eqs. 8–10 de Allain 2015)

Mecanismo alternativo — ajuste experimental MELHOR que o modelo clássico:

```
Hipótese RLS: MeOH adsorve na superfície; TG reage com MeOH* adsorvido.

         k_ER,i · C_TGᵢ · K_MeOH · C_MeOH
rᵢ = ─────────────────────────────────────────
              1 + K_MeOH · C_MeOH

Onde:
  K_MeOH = constante de adsorção do metanol na superfície ZnAl₂O₄
  k_ER,i  = constante cinética superficial da reação i
```

Implementação no Star-CCM+ requer **User Field Function** para o denominador de inibição.

---

## Coeficientes de Difusão Molecular — Allain (2015)

Valores experimentais determinados para mistura triolein/MeOH no catalisador ZnAl₂O₄ a 120°C:

| Espécie | D_m,i (m²/s) | Sc = ν/D | Observação |
|---------|-------------|----------|------------|
| TG (triolein) | 1.01 × 10⁻¹⁰ | ~54 000 | Espécie controlante; δ_c ≈ 22 µm |
| DG | 2.3 × 10⁻¹⁰ | ~23 500 | Intermediário leve |
| MG | 9.13 × 10⁻¹⁰ | ~5 900 | Intermediário mais difusivo |
| FAME | 5.33 × 10⁻¹⁰ | ~10 100 | Produto biodiesel |
| GL (glicerol) | 5.71 × 10⁻⁹ | ~940 | Co-produto, alta difusividade |
| MeOH | 1.0 × 10⁻⁸ | ~540 | Reagente, difusividade ~100× TG |

> **Sc = ν/D** calculado com ν ≈ 5.45 × 10⁻⁶ m²/s (mistura a 120°C, estimativa)

### Implicações para o CFD (Fase 2)

- **Sc_TG ≈ 54 000** → camada limite de concentração extremamente fina: **δ_c ≈ 22 µm**
- Canal com Dh = 1.1 mm: relação **δ_c / Dh ≈ 0.02** (2% do raio hidráulico)
- A concentração de TG varia de Y = 0.58 (centro) a Y ≈ 0 (parede) — **gradiente de 53%**
- Regime dominante: **MTL (Mass Transfer Limited)** — Lévêque/Graetz
- MeOH tem D_MeOH/D_TG ≈ 100 → **auto-enriquecimento na parede**: Y_MeOH sobe de 0.18 (entrada) até 0.61 (parede, saída)
- Justifica malha refinada junto à parede (y⁺ < 1, resolução de δ_c)

---

## Coeficientes de Atividade UNIFAC-LLE (Allain 2015)

Para mistura altamente não-ideal:

| Espécie | γᵢ (a T=120°C) | Observação |
|---------|---------------|------------|
| TG | ~1.0 | Fase oleosa — ideal |
| MeOH | ~1.5 | Ligeiramente não-ideal |
| GL | **30.26** | Muito não-ideal — grande desvio positivo |
| FAME | ~1.1 | Quase ideal |

> Glicerol é altamente imiscível com a fase oleosa → γ_GL >> 1. Relevante para conversões acima de 80%.

---

## Expressão Geral LHHW (para implementação no Star-CCM+)

```
          k · [A]^m · [B]^n
r = ─────────────────────────────────
     (1 + Ka·[A] + Kb·[B] + Kp·[P])^n

Onde:
  k   = constante cinética de Arrhenius: k = A·exp(-Ea/RT)
  Ka, Kb, Kp = constantes de adsorção/dessorção de Langmuir
  [A], [B] = concentrações superficiais dos reagentes
  [P] = concentração do produto (inibição)
```

---

## Comparação: Modelo Clássico vs Eley-Rideal (Allain 2015)

| Critério | 2ª Ordem Clássico | Eley-Rideal (MeOH ads.) |
|----------|------------------|------------------------|
| Ajuste experimental | Razoável | **Melhor** |
| Complexidade | Simples | Denominador extra (K_MeOH) |
| Implementação CFD | Direta (Field Function) | Requer UFF para denominador |
| Adotado na Fase 2 | **Sim** | Pendente |
| Próximo passo | — | Avaliar impacto na conversão |

---

## Notas de Implementação (Star-CCM+)

- Caminho: `Physics → Chemistry → Surface Reactions → Add Reaction`
- Taxa em **[mol/m²/s]** — já incluída como superficial na parede do canal
- Constantes de Arrhenius: campos `Pre-exponential Factor` e `Activation Energy`
- Para Eley-Rideal, o denominador de inibição exige **User Field Function** customizada
- Referência cruzada: ver `06_Modelagem_e_Simulacao/FASE2_resultados_CFD.md` para resultados quantitativos

---

*Última atualização: Junho/2026 | Gabriel Rozo — FEQ/UNICAMP*

# 02 — Cinética Heterogênea e Modelos LHHW

## Escopo

Mecanismos cinéticos para transesterificação heterogênea, modelos de Langmuir-Hinshelwood-Hougen-Watson (LHHW) e Eley-Rideal (ER), determinação experimental de parâmetros e implementação em CFD.

## Relevância para o Projeto

A **Fase 2** do modelo CFD requer uma expressão de taxa de reação para a Surface Reaction na parede do canal. O mecanismo adotado é do tipo **LHHW**, onde:

- Adsorção do metanol (ou do triglicerídeo) na superfície catalítica
- Reação superficial entre espécie adsorvida e espécie em fase líquida
- Dessorção dos produtos (FAME + glicerol)

O Star-CCM+ permite a implementação direta de cinética LHHW via **Field Function** ou **User-Defined EOS** na aba de Surface Chemistry.

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| 1 | Noureddini & Zhu | Kinetics of Transesterification of Soybean Oil | 1997 | [JAOCS 74:1457](https://doi.org/10.1007/s11746-997-0040-8) | ✅ Lido | Fundação mecanística TG→DG→MG→GL, Ea: 8000–18500 cal/mol |
| 2 | Revisão Ren. Energy | Kinetics Models of Transesterification | 2020 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila | Comparação GRE, MSO, SO, PFO |
| 3 | — | Parâmetros Cinéticos para Triolein/MeOH em ZnAl₂O₄ | ~2018 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila | Limitação por difusão molecular, excesso de MeOH |

## Mecanismo de Referência — Noureddini & Zhu (1997)

```
Reações em série (reversíveis):

TG  + MeOH ⇌ DG  + FAME    (k₁, k₋₁)
DG  + MeOH ⇌ MG  + FAME    (k₂, k₋₂)
MG  + MeOH ⇌ GL  + FAME    (k₃, k₋₃)

Onde:
  TG  = Triglicerídeo
  DG  = Diglicerídeo
  MG  = Monoglicerídeo
  GL  = Glicerol
  FAME = Fatty Acid Methyl Ester (biodiesel)
```

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

## Notas de Implementação (Star-CCM+)

- Caminho: `Physics → Chemistry → Surface Reactions → Add Reaction`
- A expressão da taxa é inserida como **Field Function** em `[mol/m²/s]`
- As constantes de Arrhenius são cadastradas nos campos `Pre-exponential Factor` e `Activation Energy`
- Para LHHW, o denominador de inibição exige uma **User Field Function** customizada
- Referência cruzada: ver pasta `06_Modelagem_e_Simulacao` para tutoriais do Star-CCM+

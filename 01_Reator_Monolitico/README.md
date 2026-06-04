# 01 — Reator Monolítico

## Escopo

Literatura sobre geometria, design, fabricação e aplicações de reatores monolíticos cerâmicos (cordierita) e metálicos. Foco em monólitos com washcoat catalítico para reações líquido-sólido.

## Relevância para o Projeto

O reator modelado é um monólito do tipo colmeia (honeycomb) com recheio estruturado. A geometria CFD é simplificada para **1 canal representativo 2D (retângulo)**. As referências aqui fundamentam:

- A escolha geométrica e sua justificativa na dissertação
- As dimensões típicas (diâmetro hidráulico, CPSI — células por polegada quadrada)
- A hipótese de canal representativo (simetria do monólito)
- A caracterização do washcoat (espessura, porosidade)

## Referências

| # | Autores | Título | Ano | DOI/Link | Status | Notas |
|---|---------|--------|-----|----------|--------|-------|
| 1 | Univ. Bath (Tese) | Biodiesel Production in Fixed-Bed Monolithic Reactors | ~2015 | [Bath Portal](https://researchportal.bath.ac.uk) | 📖 Em leitura | SrO/cordierita, 61 células/cm², Dh=1.1mm, 120°C, 8 bar |
| 2 | Univ. Bath (Tese) | Catalytic Monoliths for Biodiesel Production | ~2017 | [Bath Portal](https://researchportal.bath.ac.uk) | 🔲 Na fila | Zn-prolina, 62 células/cm², 2 métodos de coating |

## Parâmetros de Referência (extraídos da literatura Bath)

```
Suporte:           Cordierita (2MgO·2Al₂O₃·5SiO₂)
Densidade:         61–62 células/cm² (≈ 400 CPSI)
Diâmetro hidráulico (Dh): ~1.1 mm
Catalisador (tese 1): SrO (19.6 wt%)
Catalisador (tese 2): Zn(C₅H₈NO₂)₂ (zinco-prolina)
T operação:        120 °C
P operação:        8 bar
Razão molar MeOH:óleo: 6:1
Substrato:         Óleo de canola
```

## Conceitos-Chave para a Dissertação

- **Canal representativo:** A hipótese de periodicidade do monólito permite simular apenas 1 canal com condições de contorno de simetria, reduzindo drasticamente o custo computacional.
- **Washcoat:** Camada fina (~10–50 µm) de catalisador depositada sobre as paredes do canal. No CFD (Star-CCM+), modelada como **Surface Reaction** na parede (boundary condition), sem necessidade de resolver a difusão intraparticular na Fase 1.
- **CPSI (Cells Per Square Inch):** Métrica de densidade celular. 400 CPSI corresponde a ~62 células/cm².

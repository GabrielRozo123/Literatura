# 📚 Literatura — Mestrado FEQ/UNICAMP

**Projeto:** Modelagem Computacional (CFD) e Avaliação Hidrodinâmica da Produção de Biodiesel via Transesterificação Heterogênea em Reator Monolítico Estruturado

**Autor:** Gabriel Rozo  
**Programa:** Pós-Graduação em Engenharia Química — FEQ/UNICAMP  
**Orientadores:** Prof. Dr. Raphael | Prof. Dr. Dirceu Noriler  
**Período:** 2025–2027  

---

## 🗂️ Estrutura do Repositório

```
Literatura/
├── 01_Reator_Monolitico/           → Geometria, design e aplicações de reatores monolíticos
├── 02_Cinetica_Heterogenea_LHHW/   → Cinética catalítica heterogênea, mecanismos LHHW e Eley-Rideal
├── 03_CFD_Microcanais_e_Monolitos/ → Simulações CFD em microcanais e canais de monólito
├── 04_Transferencia_Calor_e_Massa/ → CHT, difusão, Nusselt, Sherwood em escoamento laminar
├── 05_Biodiesel_e_Transesterificacao/ → Processo, catalisadores heterogêneos, condições de reação
├── 06_Modelagem_e_Simulacao/       → Metodologia CFD geral, validação, Star-CCM+
└── references.bib                  → Arquivo BibTeX unificado (LaTeX-ready)
```

---

## 📋 Tabela Geral de Referências

| # | Autores | Título (resumido) | Tipo | Tema | Ano | DOI/Link | Status |
|---|---------|-------------------|------|------|-----|----------|--------|
| 1 | Noureddini & Zhu | Kinetics of Transesterification of Soybean Oil | Artigo | Cinética | 1997 | [JAOCS 74:1457](https://doi.org/10.1007/s11746-997-0040-8) | ✅ Lido |
| 2 | Univ. Bath (Tese) | Biodiesel Production in Fixed-Bed Monolithic Reactors | Tese | Reator Monolítico | ~2015 | [Bath Research Portal](https://researchportal.bath.ac.uk) | 📖 Em leitura |
| 3 | Univ. Bath (Tese) | Catalytic Monoliths for Biodiesel Production | Tese | Reator Monolítico | ~2017 | [Bath Research Portal](https://researchportal.bath.ac.uk) | 🔲 Na fila |
| 4 | Pinheiro & Larimi | CFD Modeling of FBR vs PBMR for Biodiesel (Sci. Rep.) | Artigo | CFD + Biodiesel | 2024 | [Nature/Sci.Rep.](https://doi.org/10.1038/s41598-024-XXXXX) | 🔲 Na fila |
| 5 | Revisão (Ren. Energy) | Kinetics Models of Transesterification | Revisão | Cinética | 2020 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila |
| 6 | — | Estimação de Parâmetros — ZnAl2O4 (ScienceDirect) | Artigo | Cinética LHHW | ~2018 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila |
| 7 | MDPI Energies | Microchannel Reactor Technologies for Biodiesel | Revisão | CFD + Microcanais | 2024 | [MDPI](https://www.mdpi.com) | 🔲 Na fila |
| 8 | Chem. Eng. Process. | Numerical Simulations of Biodiesel Synthesis in Microchannels | Artigo | CFD | 2015 | [ScienceDirect](https://www.sciencedirect.com) | 🔲 Na fila |
| 9 | IntechOpen | Mixing Performance in Microchannel | Capítulo | Escoamento Laminar | 2019 | [IntechOpen](https://www.intechopen.com) | 🔲 Na fila |

**Legenda de Status:**
- ✅ Lido e fichado
- 📖 Em leitura
- 🔲 Na fila
- ⭐ Referência-chave da dissertação
- ❌ Descartado (justificar no README da pasta)

---

## 🧭 Mapa Conceitual do Projeto

```
REATOR MONOLÍTICO (canal 2D representativo)
        │
        ├── FASE 1: Hidrodinâmica a frio
        │       └── Perfil de velocidade de Poiseuille
        │           Validação do ΔP ≈ 0
        │           Re << 1 (escoamento laminar desenvolvido)
        │
        └── FASE 2: Reação + CHT acoplados
                └── Surface Reaction (washcoat na parede)
                    Cinética LHHW (TG → DG → MG → GL)
                    Transferência de calor conjugada
                    Reação endotérmica → gradiente de T axial
```

---

## 📌 Como Contribuir com Novas Referências

1. Adicione o PDF na pasta temática correspondente com o nome: `Autor_Ano_PalavraChave.pdf`
2. Atualize a tabela acima com os metadados
3. Adicione a entrada BibTeX no arquivo `references.bib`
4. Atualize o `README.md` da pasta temática correspondente

---

*Repositório mantido por Gabriel Rozo | FEQ/UNICAMP | 2025–2027*

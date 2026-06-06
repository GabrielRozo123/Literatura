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
| 2 | Firth (Bath, Tese) | Biodiesel Production in Fixed-Bed Monolithic Reactors | Tese | Reator Monolítico | 2014 | [Bath Research Portal](https://researchportal.bath.ac.uk/en/studentTheses/biodiesel-production-in-fixed-bed-monolithic-reactors) | ✅ Fichado |
| 3 | Asli (Bath, Tese) | Catalytic Monoliths for Biodiesel Production | Tese | Reator Monolítico | 2011 | [Bath Research Portal](https://researchportal.bath.ac.uk/en/studentTheses/catalytic-monoliths-for-biodiesel-production) | 🔲 Na fila |
| 4 | Omranpour & Larimi | Modeling and Simulation of Biodiesel: FBR vs PBMR (Sci. Rep.) | Artigo | CFD + Biodiesel | 2024 | [10.1038/s41598-024-60757-5](https://doi.org/10.1038/s41598-024-60757-5) | ✅ Fichado |
| 5 | Ezzati et al. | Kinetics Models of Transesterification (Ren. Energy) | Revisão | Cinética | 2021 | [10.1016/j.renene.2020.12.055](https://doi.org/10.1016/j.renene.2020.12.055) | ✅ Fichado |
| 6 | Allain et al. | Kinetic Parameters & Diffusion Coefficients — Triolein/MeOH/ZnAl₂O₄ | Artigo | Cinética LHHW | 2015 | [CEJ 283:833](https://doi.org/10.1016/j.cej.2015.07.075) | ⭐ Ref. principal |
| 7 | Subramaniam et al. | Enhancing Biodiesel Production: A Review of Microchannel Reactor Technologies | Revisão | CFD + Microcanais | 2024 | [10.3390/en17071652](https://doi.org/10.3390/en17071652) | 🔲 Na fila |
| 8 | Mohd Laziz et al. | Rapid Production of Biodiesel in a Microchannel Reactor at Room Temperature (CES) | Artigo | CFD | 2020 | [10.1016/j.ces.2020.115532](https://doi.org/10.1016/j.ces.2020.115532) | 🔲 Na fila |

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
        └── FASE 2: Reação + Transferência de Massa ✅ CONCLUÍDA
                └── Surface Reaction (washcoat na parede)
                    Cinética Allain 2015 — 2ª ordem reversível
                    TG + 3 MeOH → DG → MG → GL + 3 FAME
                    Sc_TG ≈ 54 000 → δ_c ≈ 22 µm (regime MTL)
                    ΔY_TG = 0.44 entre centro e parede (x=L)
                    Auto-enriquecimento MeOH: Y_wall 0.18→0.61
                    Ver: 06_Modelagem_e_Simulacao/FASE2_resultados_CFD.md
```

---

## 📌 Como Contribuir com Novas Referências

1. Adicione o PDF na pasta temática correspondente com o nome: `Autor_Ano_PalavraChave.pdf`
2. Atualize a tabela acima com os metadados
3. Adicione a entrada BibTeX no arquivo `references.bib`
4. Atualize o `README.md` da pasta temática correspondente

---

*Repositório mantido por Gabriel Rozo | FEQ/UNICAMP | 2025–2027*

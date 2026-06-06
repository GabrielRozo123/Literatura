# Fase 2 — Resultados CFD: Reação + Transferência de Massa

**Projeto:** CFD de Reator Monolítico para Biodiesel (Star-CCM+)
**Autor:** Gabriel Rozo | FEQ/UNICAMP | 2025–2027
**Status:** ✅ Concluída — Junho/2026
**Referência principal:** Allain et al. (2015), CEJ 283:833–845

---

## 1. Configuração da Simulação

| Parâmetro | Valor |
|-----------|-------|
| Geometria | Canal 2D plano — 1 canal representativo do monólito |
| CPSI | 400 (células por polegada quadrada) |
| Diâmetro hidráulico Dh | 1.1 mm |
| Comprimento L | 50 mm |
| Temperatura | 120°C (isotérmica) |
| Pressão | 8 bar |
| Razão molar MeOH:TG | 6:1 |
| Escoamento | Laminar, Re << 1 (Poiseuille desenvolvido) |
| Catalisador | ZnAl₂O₄ (washcoat na parede — Top_Wall) |
| Solver | Star-CCM+ (Fase 2 — Surface Reaction ativada) |

---

## 2. Modelo Cinético Adotado

**Allain et al. (2015) — Modelo clássico de 2ª ordem:**

```
r₁ = k₁·C_TG·C_MeOH  −  k₋₁·C_DG·C_FAME
r₂ = k₂·C_DG·C_MeOH  −  k₋₂·C_MG·C_FAME
r₃ = k₃·C_MG·C_MeOH  −  k₋₃·C_GL·C_FAME
```

**Coeficientes de difusão molecular (Allain 2015):**

| Espécie | D_m,i (m²/s) |
|---------|-------------|
| TG | 1.01 × 10⁻¹⁰ |
| DG | 2.3 × 10⁻¹⁰ |
| MG | 9.13 × 10⁻¹⁰ |
| FAME | 5.33 × 10⁻¹⁰ |
| GL | 5.71 × 10⁻⁹ |
| MeOH | 1.0 × 10⁻⁸ |

---

## 3. Resultados Quantitativos Principais

### 3.1 Perfil Transversal (x = L = 50 mm)

| Espécie | Y_centerline | Y_wall | ΔY | Observação |
|---------|-------------|--------|-----|------------|
| TG | 0.58 | ~0 | **0.44 (53%)** | Gradiente dominante — controla a reação |
| MeOH | 0.18 | 0.61 | −0.43 | **Auto-enriquecimento** na parede |
| DG | ~0 | ~0.008 | — | Intermediário leve na parede |
| FAME | ~0.003 | ~0.05 | — | Produto em formação |
| GL | ~0 | traços | — | Co-produto ainda negligível em x=L |

> **Conclusão chave:** Gradiente transversal de TG de 53% à saída do canal — justifica o uso de CFD 2D completo versus modelo de canal com concentração uniforme.

### 3.2 Perfil Axial (linha central, y = 0)

| Posição x/L | Y_TG (centro) | Y_MeOH (centro) |
|-------------|--------------|----------------|
| 0 (entrada) | ~0.58 | ~0.18 |
| 0.5 (meio) | ~0.57 | ~0.19 |
| 1.0 (saída) | ~0.57 | ~0.19 |

> A linha central quase não reage — os gradientes são radiais, não axiais. O TG no centro não "vê" o catalisador na parede em L=50 mm com Sc_TG=54 000.

### 3.3 Camada Limite de Concentração

| Quantidade | Valor | Como calculado |
|-----------|-------|---------------|
| Sc_TG = ν/D_TG | **~54 000** | ν ≈ 5.45×10⁻⁶ m²/s, D_TG = 1.01×10⁻¹⁰ |
| δ_c (estimativa Lévêque) | **~22 µm** | δ_c ∝ (D·x/u)^(1/3) |
| δ_c / Dh | ~0.02 (2%) | Camada muito fina |
| Regime | **MTL** (Mass Transfer Limited) | Sc >> 1 → Lévêque/Graetz |

### 3.4 Intermediários na Parede Catalítica (Top_Wall)

- **DG na parede:** Y ≈ 0.008 (0.8%) — acumula como intermediário (produzido em r₁, consumido em r₂)
- **FAME na parede:** Y ≈ 0.05 (5%) — produto em formação
- **DG no centro:** Y < 0.0003 → negligível na linha axial (não difunde de volta ao centro em L=50 mm)

---

## 4. Análise Física e Conclusões

### 4.1 Regime de Operação

A Fase 2 confirmou que o reator opera no **regime de transferência de massa** (MTL):

- Sc_TG ≈ 54 000 é extremamente alto — a difusividade do triglicerídeo é ~100× menor que a do metanol
- A camada limite de concentração δ_c ≈ 22 µm é apenas 2% de Dh
- A taxa de reação é limitada não pela cinética, mas pela chegada de TG à superfície catalítica
- Conclusão prática: **refinamento de malha junto à parede é crítico** (y⁺ < 1, resolução de δ_c)

### 4.2 Auto-Enriquecimento de MeOH na Parede

Fenômeno físico relevante:
- MeOH tem D ≈ 100× maior que TG
- À medida que TG é consumido na parede, MeOH difunde muito mais rapidamente para repor o espaço
- Resultado: **fração mássica de MeOH na parede aumenta de 0.18 (entrada) para 0.61 (saída)**
- Isso favorece a reação (excesso local de MeOH) mas reduz TG disponível

### 4.3 Justificativa para CFD 2D

O gradiente transversal de TG de **ΔY = 0.44 (53%)** entre centro e parede em x=L mostra que:
- Modelos 1D (plug flow com concentração uniforme) subestimam o gradiente real
- A concentração "vista" pelo catalisador é muito menor que a concentração média
- **A conversão real é controlada pela difusão transversal** — não pela cinética

### 4.4 Comprimento de Entrada de Concentração

- O comprimento de entrada de concentração para Sc >> 1 é muito maior que para velocidade
- Em L = 50 mm, a camada limite ainda está em desenvolvimento (regime de Graetz)
- O fluxo de TG à parede **aumenta com x** (camada limite ainda crescendo)

### 4.5 Comparação com Allain 2015

| Aspecto | Allain 2015 (experimento) | CFD Fase 2 |
|---------|--------------------------|------------|
| Sistema | Reator tubular, catalisador em pó | Canal 2D, washcoat |
| T | 120°C | 120°C ✅ |
| Catalisador | ZnAl₂O₄ | ZnAl₂O₄ ✅ |
| D_m,i | Medidos experimentalmente | Usados diretamente ✅ |
| Regime | — | MTL confirmado ✅ |
| Modelo cinético | 2ª ordem + Eley-Rideal | 2ª ordem (Fase 2) |
| Próximo passo | — | Testar Eley-Rideal (Fase 3) |

---

## 5. Figuras Geradas

Todas as figuras em `biodiesel_monolith_cfd/results/` (repo Programacao):

| Arquivo | Conteúdo |
|---------|---------|
| `fig1_perfil_transversal.pdf` | Perfil Y(y) em x=L: painel (a) canal completo, painel (b) zoom camada wall com δ_c |
| `fig2_perfil_axial.pdf` | Perfil Y(x) na linha central (y=0): TG e MeOH |
| `fig3_intermediarios_axial.pdf` | DG, MG, GL, FAME na linha central |

**Estilo:** CEJ (Chemical Engineering Journal) — fonte Helvetica, 2 colunas, 300 dpi

---

## 6. Próximas Etapas (Fase 3)

- [ ] Obter propriedades físicas reais da mistura (ρ, μ, Cp) dos orientadores
- [ ] Implementar correlação Nu/Sh de Lévêque para validação analítica do δ_c
- [ ] Exportar perfil de fluxo de TG na parede J_TG(x) vs x
- [ ] Testar modelo Eley-Rideal (Eqs. 8–10 de Allain 2015) e comparar conversão
- [ ] Avaliar impacto da razão molar MeOH:TG (6:1 → 12:1) no auto-enriquecimento
- [ ] Adicionar equação de energia (CHT) para avaliar gradiente térmico axial

---

## 7. Referências Cruzadas

- Modelo cinético: `02_Cinetica_Heterogenea_LHHW/README.md`
- BibTeX: `references.bib` — entrada `Allain2015`
- Scripts de pós-processamento: `biodiesel_monolith_cfd/scripts/plot_especies_fase2.py`

---

*Documento criado: Junho/2026 | Gabriel Rozo — FEQ/UNICAMP*

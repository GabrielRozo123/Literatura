# Fase 1 — Resultados CFD: Hidrodinâmica a Frio

**Projeto:** CFD de Reator Monolítico para Biodiesel (Star-CCM+)
**Autor:** Gabriel Rozo | FEQ/UNICAMP | 2025–2027
**Status:** ✅ Concluída e Validada
**Objetivo:** Validar escoamento de Poiseuille no canal 2D antes de ativar reação química

---

## 1. Configuração da Simulação

| Parâmetro | Valor |
|-----------|-------|
| Geometria | Canal 2D plano retangular |
| Diâmetro hidráulico Dh | 1.1 mm |
| Comprimento L | 50 mm |
| Fluido | Mistura óleo/MeOH (estimativa: ρ=870 kg/m³, μ=6×10⁻³ Pa·s) |
| Temperatura | 120°C (isotérmica) |
| Velocidade de entrada | 1 mm/s (uniforme) |
| Modelos ativados | Steady + Segregated Flow + Laminar + Constant Density |
| Modelos **desativados** | Energy, Multi-Component, Reaction (frio = sem reação) |
| Malha | Trimmer, Base Size = 0.05 mm (~22×1000 células) |
| Arquivo Star-CCM+ | `biodiesel_canal2D_fase1.sim` |

---

## 2. Critérios de Validação e Resultados

| Grandeza | Valor Analítico | Resultado CFD | Desvio | Status |
|----------|----------------|---------------|--------|--------|
| Re | 0.160 | 0.160 | — | ✅ Stokes laminar |
| u_max (saída) | **1.500 mm/s** | **1.500 mm/s** | < 0.1% | ✅ |
| u_max / u_média | **1.500** | **1.500** | < 0.1% | ✅ Poiseuille confirmado |
| ΔP (Inlet→Outlet) | **2.975 Pa** | **2.975 Pa** | < 1% | ✅ |
| R² perfil vs. analítico | — | > 0.999 | — | ✅ |
| Resíduos convergência | — | < 1×10⁻⁶ | — | ✅ |

---

## 3. Equações Analíticas de Referência

**Perfil de Poiseuille (canal plano 2D):**
```
u(y) = u_max · [1 − (2y/Dh − 1)²]

u_max = (3/2) · u_média = 1.500 mm/s    (para canal plano)
```

**Queda de pressão (Hagen-Poiseuille):**
```
ΔP = 12 · μ · L · u / Dh²
   = 12 × 6×10⁻³ × 0.05 × 1×10⁻³ / (1.1×10⁻³)²
   = 2.975 Pa   ← virtualmente zero vs. P_operação = 8 bar = 800 000 Pa
```

**Comprimento de entrada hidrodinâmico:**
```
L_hid = 0.05 · Re · Dh = 0.05 × 0.160 × 1.1 mm ≈ 8.8 µm

→ O perfil está desenvolvido nos primeiros 0.009 mm do canal.
  Para L = 50 mm, o canal opera 99.98% em regime de Poiseuille puro.
```

---

## 4. Grandezas Adimensionais e Diagnóstico do Regime

| Número | Expressão | Valor | Interpretação |
|--------|-----------|-------|---------------|
| Reynolds | Re = ρuDh/μ | **0.160** | Regime de Stokes — laminar desenvolvido |
| Número de Mach | Ma = u/c_s | << 0.001 | Incompressível ✅ |
| ΔP / P_operação | 2.975 / 800 000 | **0.00037%** | Queda de pressão negligível ✅ |
| L_hid / L | 8.8 µm / 50 mm | **0.018%** | Perfil desenvolvido em < 0.02% do canal ✅ |
| τ_wall | 3μu/(Dh/2) | **32.7 mPa** | Tensão de cisalhamento na parede |

---

## 5. Conclusões da Fase 1

**1. Validação bem-sucedida:** O Star-CCM+ reproduz o perfil de Poiseuille com desvio < 0.1% em relação à solução analítica. A metodologia CFD está correta.

**2. Regime de Stokes confirmado:** Re = 0.160 — sem instabilidades, sem transição para turbulência em nenhuma condição operacional prevista.

**3. ΔP desprezível:** 2.975 Pa vs. 8 bar de operação → a queda de pressão no canal não altera o regime de escoamento nem as condições de reação da Fase 2.

**4. Escoamento 100% desenvolvido:** O canal opera em Poiseuille puro desde x ≈ 0.009 mm. Isso simplifica enormemente a análise — a Fase 2 parte de condições hidrodinâmicas uniformes e conhecidas.

**5. Hipótese de canal representativo validada:** A simetria do Poiseuille 2D confirma que simular apenas 1 canal do monólito é fisicamente correto (sem efeitos de borda entre canais vizinhos para Re << 1).

---

## 6. Transição para a Fase 2

Com a Fase 1 validada, o arquivo `.sim` foi salvo como base:
```
biodiesel_canal2D_fase2_base.sim
```

Modificações aplicadas para a Fase 2:
- Ativação de **Multi-Component Liquid** (TG, MeOH, DG, MG, FAME, GL)
- Ativação de **Surface Reaction** na Top_Wall (washcoat catalítico)
- Coeficientes de difusão D_m,i de Allain et al. (2015)
- Malha refinada junto à Top_Wall para resolver δ_c ≈ 22 µm

---

## 7. Figuras

| Arquivo | Conteúdo |
|---------|---------|
| `figuras/fig0_fase1_poiseuille.pdf` | (a) Perfil u(y) analítico vs. CFD em x=L; (b) desenvolvimento axial u_max(x) |

---

## 8. Referências Cruzadas

- Checklist de configuração Star-CCM+: `biodiesel_monolith_cfd/docs/fase1_starccm_checklist.md` (repo Programacao)
- Análise analítica detalhada: `biodiesel_monolith_cfd/docs/literatura_analise.md` (repo Programacao)
- Fase 2 resultados: `06_Modelagem_e_Simulacao/FASE2_resultados_CFD.md`

---

*Documento criado: Junho/2026 | Gabriel Rozo — FEQ/UNICAMP*

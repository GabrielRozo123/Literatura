# 06 — Modelagem e Simulação CFD (Star-CCM+)

## Escopo

Metodologia geral de CFD, validação de modelos, tutoriais e documentação do Simcenter Star-CCM+, boas práticas de simulação para escoamento laminar reativo.

## Relevância para o Projeto

Repositório de referências técnicas para a execução direta das simulações no Star-CCM+. Inclui tutoriais Siemens, referências de validação e documentação de configurações específicas.

## Referências

| # | Autores | Título | Ano | Tipo | Status | Notas |
|---|---------|--------|-----|------|--------|-------|
| — | Siemens | Star-CCM+ User Guide (v2406) | 2024 | Doc. Técnica | 🔲 | Manual principal — baixar do Siemens Support |
| — | Siemens | Tutorial: Surface Chemistry | 2024 | Tutorial | 🔲 | Configuração de Surface Reactions |
| — | Siemens | Tutorial: CHT (Conjugate Heat Transfer) | 2024 | Tutorial | 🔲 | Acoplamento fluido-sólido |
| — | A preencher | — | — | — | 🔲 | — |

## Configuração da Fase 1 — Hidrodinâmica a Frio (Checklist Star-CCM+)

### Physics Models (árvore de física)

```
Continuum → Physics
├── Space:              Two Dimensional ✓
├── Time:               Steady ✓
├── Material:           Liquid ✓
│   └── Fluid: definir mistura óleo/MeOH
├── Flow:               Segregated Flow ✓
├── Equation of State:  Constant Density ✓
└── Viscous Regime:     Laminar ✓
    (NÃO ativar modelos de turbulência)
```

### Boundary Conditions

```
Inlet:   Velocity Inlet  → u = u_entrada (m/s), perfil uniforme
Outlet:  Pressure Outlet → P_gauge = 0 Pa
Walls:   No-Slip Wall    → u = 0 (parede estacionária)
         (Fase 1: sem reação, sem fluxo de calor)
```

### Critério de Convergência

```
Resíduos:   < 1×10⁻⁶  (Continuidade e Momento)
Monitores:  ΔP (inlet-outlet), u_max na saída
Malha:      Refinar na parede → y+ irrelevante em laminar,
            mas garantir ≥ 10 células na direção transversal
```

## Configuração da Fase 2 — Reação + CHT (Checklist Star-CCM+)

### Physics Models adicionais

```
Continuum → Physics
├── Energy:             Fluid Temperature ✓  (habilitar)
├── Species:            Multi-Component Liquid ✓
│   └── Componentes: TG, DG, MG, MeOH, FAME, GL
└── Chemistry:          Surface Reactions ✓
    └── Reaction: LHHW (via Field Function)
```

### Wall Boundary — Washcoat

```
Walls → Thermal Specification:  Coupled Wall
Walls → Chemistry:              Surface Reaction habilitada
         └── Taxa: r_LHHW [mol/m²/s]  (Field Function customizada)
```

## Análise de Sensibilidade de Malha (Grid Independence)

```
Malha 1 (grossa):   N×M  células
Malha 2 (média):    2N×2M células  → refinamento x2
Malha 3 (fina):     4N×4M células  → refinamento x4

Critério GCI (Grid Convergence Index):
  GCI < 5%  → malha independente aceita
```

## Notas de Boas Práticas

- Sempre inicializar a Fase 2 com a solução convergida da Fase 1 (Field Initialization)
- Para cinética LHHW: implementar limitador de taxa (clamp r ≥ 0) para evitar taxas negativas
- Monitorar o perfil axial de temperatura e concentração como probes na linha central
- Exportar dados via `Tools → Reports → Line Probe` para pós-processamento em Python

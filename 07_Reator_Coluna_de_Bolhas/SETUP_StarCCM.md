# Coluna de Bolhas: caso Euler–Euler no STAR-CCM+ (versão "demo rápida")

**Base recomendada:** tutorial *"Eulerian: Hibiki's Bubble Column"* da documentação local (Simcenter STAR-CCM+ 2602 → Tutorials → Multiphase). Use esse tutorial para conferir os **nomes exatos** de menus e modelos na sua versão. Este roteiro troca a geometria e as condições de contorno por uma coluna de bolhas em batelada.

> Nomes de menus escritos de memória (v2406 em diante). Se algo estiver diferente na 2602, siga o tutorial Hibiki e me mande o trecho para eu ajustar o roteiro ou fazer uma macro Java.

---

## 0. Resumo do caso

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Geometria | Cilindro D = 0,15 m, H_coluna = 1,2 m | D ≥ 0,15 m (critério de Wilkinson) |
| Líquido estático | H0 = 0,90 m (H0/D = 6) | H/D > 5; 0,3 m de espaço livre no topo |
| Sistema | Ar–água, 25 °C, 1 atm, densidades constantes | |
| Aspersor | **Fundo inteiro** = entrada de gás (prato perfurado ideal) | Distribuição uniforme, como nas correlações |
| U_G | **2 cm/s** (caso principal); 1 e 4 cm/s (opcional) | Regime homogêneo / início da transição |
| Bolha | Monodispersa, **d = 5 mm** | d32 de 5,6–6,7 mm (Akita & Yoshida) e U∞ = 0,23 m/s |
| Malha | Trimmer, base 7,5 mm → ~50–60 mil células | "Rápida"; versão grossa com 10 mm → ~25 mil |
| Tempo | Δt = 0,01 s, 60 s físicos, média de 20 a 60 s | CFL_bolha ≈ 0,3·0,01/0,0075 ≈ 0,4 |

Custo estimado (ordem de grandeza, **não medido**): de 1 a 3 h em 8 núcleos com a malha de 7,5 mm; menos de 1 h com a de 10 mm. Para a apresentação, dá para rodar as 3 velocidades em paralelo (um .sim por U_G).

---

## 1. Geometria (3D-CAD)

1. `Geometry → 3D-CAD Models → New`. Sketch no plano XY: círculo de **Ø 150 mm** centrado na origem.
2. `Extrude` de **1200 mm** em +Z. Eixo da coluna = Z, fundo em z = 0.
3. Renomeie as faces: fundo → **`Aspersor`**, topo → **`Topo`**, lateral → **`Parede`**.
4. `Close 3D-CAD` → `New Geometry Part` → `Assign Parts to Regions` (uma região: **`Coluna`**, uma condição de contorno por superfície).

## 2. Malha

`Geometry → Operations → New → Mesh → Automated Mesh`:

- Meshers: **Surface Remesher** + **Trimmed Cell Mesher** (sem Prism Layer).
- `Default Controls → Base Size` = **7,5 mm** (ou 10 mm na versão rápida). Target Surface Size = 100 %, Minimum Surface Size = 25 %.
- Gere a malha e confira a contagem (~55 mil células com 7,5 mm).

> Alternativa mais "limpa": Directed Mesh (malha O-grid extrudada em Z). Vale a pena só se sobrar tempo.

## 3. Física (Physics Continuum)

Selecione os modelos nesta ordem:

```
Space ........................ Three Dimensional
Time ......................... Implicit Unsteady
Material ..................... Multiphase → Eulerian Multiphase (EMP)
Flow ......................... Segregated Flow
Optional ..................... Gravity  (−9,81 m/s² em Z)
                               Multiphase Interaction
Viscous Regime ............... Turbulent
Reynolds-Averaged Turbulence . K-Epsilon Turbulence
```

**Fases** (`Eulerian Multiphase → Eulerian Phases → New`):

| Fase | Modelos da fase |
|------|-----------------|
| `Agua` | Liquid, Constant Density (997 kg/m³, μ = 8,9e-4 Pa·s); Turbulent → **Realizable K-Epsilon Two-Layer** (ou SST K-Omega) |
| `Ar` | Gas, Constant Density (1,18 kg/m³, μ = 1,8e-5 Pa·s); turbulência da fase dispersa = **resposta à turbulência** (Turbulence Response / Tchen), *sem* equações próprias de k–ε |

**Interação de fases** (`Multiphase Interaction → Phase Interactions → New → Continuous-Dispersed`), com `Agua` contínua e `Ar` dispersa:

| Modelo | Escolha | Observação |
|--------|---------|-----------|
| Interaction Length Scale | **Constante = 5 mm** | diâmetro da bolha |
| Interaction Area Density | Spherical Particle | a = 6α/d |
| Drag Force | **Tomiyama** (água levemente contaminada) | dá U∞ ≈ 0,23 m/s |
| Virtual Mass Force | C_VM = 0,5 | ajuda a estabilidade |
| Turbulent Dispersion Force | Padrão (Burns / FAD) | espalha o gás lateralmente |
| Lift Force | **Opcional**: Tomiyama | C_L ≈ +0,18 para d = 5 mm. Rodar com e sem é um bom slide |
| Bubble Induced Turbulence | Opcional (Sato / Troshko–Hassan) | deixe desligado na demo |

**Gravidade / densidade de referência:** `Reference Values → Reference Density` = **1,18 kg/m³** (densidade do ar). Assim a pressão de saída igual a 0 no topo é coerente com o espaço livre cheio de gás.

## 4. Condições de contorno

| Fronteira | Tipo | Fase `Ar` | Fase `Agua` |
|-----------|------|-----------|-------------|
| `Aspersor` | **Velocity Inlet** | Volume Fraction = **1**, Velocity = **U_G** (0,02 m/s) | Volume Fraction = 0, Velocity = U_G |
| `Topo` | **Pressure Outlet**, p = 0 Pa | Backflow: Volume Fraction = **1** | Backflow: Volume Fraction = 0 |
| `Parede` | Wall | **Slip** (sem atrito) | **No-slip** |

Turbulência na entrada: intensidade de 5 %, razão de viscosidade 10.

## 5. Condições iniciais

Crie duas *Field Functions* (`Tools → Field Functions → New → Scalar`):

```
FF_alphaAgua = ($${Centroid}[2] <= 0.9) ? 1 : 0
FF_pHidro    = ($${Centroid}[2] <= 0.9) ? (997 - 1.18)*9.81*(0.9 - $${Centroid}[2]) : 0
```

- `Initial Conditions → Volume Fraction` (Agua) = `FF_alphaAgua`; (Ar) = `1 - FF_alphaAgua`. Se a sua versão pedir as frações por componente, use dois FF.
- `Initial Conditions → Pressure` = `FF_pHidro` (inicialização hidrostática, evita o "pulso" inicial).
- Velocidades = 0.

> A sintaxe `$${Centroid}[2]` é a componente Z do centróide da célula. Se der erro, use o autocompletar do editor de Field Function e escolha *Centroid → [2]*.

## 6. Solver e critérios de parada

- `Implicit Unsteady`: **Time-Step = 0,005 s** nos primeiros 2 s (fase de partida), depois **0,01 s**. Temporal Discretization: 1st order (demo) ou 2nd order (final).
- `Stopping Criteria`: **Maximum Inner Iterations = 15**; **Maximum Physical Time = 60 s**. Desative Maximum Steps.
- Under-relaxation: manter os padrões do EMP. Se divergir, use Velocity 0,5 e Pressure 0,2.

## 7. Relatórios, monitores e cenas

**(a) Retenção gasosa global (comparação principal)**

1. `Derived Parts → New → Threshold`: região `Coluna`, escalar = **Volume Fraction da fase Agua**, faixa **[0,5 ; 1]**. Nome: `Dispersao` (separa a dispersão do espaço livre).
2. `Reports → New → Volume Average`: escalar = **Volume Fraction da fase Ar**, partes = `Dispersao`. Nome: **`Holdup Global`**.
3. Botão direito → `Create Monitor and Plot from Report` (trigger = Time Step).
4. Ao final: Plot → botão direito → `Export` → CSV com o nome **`holdup_Ug2.csv`** (para 1 cm/s use `holdup_Ug1.csv`, e assim por diante).

**(b) Altura da dispersão (conferência):** `Reports → Maximum` de `Centroid[2]` em `Dispersao`. Ela deve ficar em torno de H0/(1−εG) ≈ 0,95 m para εG ≈ 0,06.

**(c) Médias temporais (perfis locais):** `Solvers → Field Mean Monitor`, com início em **t = 20 s**, para Volume Fraction (Ar) e Velocity (Agua). Depois crie uma `Line Probe` radial em **z = 0,6 m** (de x = −0,075 a +0,075 m, 50 pontos) e exporte os campos médios. O que se espera ver:

- εG(r) mais ou menos parabólico, ou com pico na parede se o lift estiver ligado;
- líquido subindo no centro (≈ 0,25 m/s segundo Riquarts) e descendo na parede, com inversão em r/R ≈ 0,7.

**(d) Para a plateia:**

- `Scenes → Scalar`: plano XZ (y = 0), Volume Fraction (Ar) com escala de 0 a 0,2.
- Uma segunda cena com vetores da velocidade da Agua.
- `Isosurface` com Volume Fraction (Agua) = 0,5 para mostrar a superfície livre subindo e oscilando.
- `Animation → Hardcopy` a cada 0,1 s de 10 a 40 s: gera o vídeo da pluma.

## 8. Pós-processamento e comparação

Coloque os CSV exportados em `Programacao/coluna_bolhas/star_exports/` e rode:

```bash
cd Programacao/coluna_bolhas
python projeto_coluna_bolhas.py
python compara_cfd_literatura.py --pasta star_exports --t-media 20
```

Saídas: `resultados/fig_cfd_vs_literatura.png` (CFD × Akita & Yoshida × Hikita × Reilly × dados experimentais) e `resultados/tabela_cfd.csv` com os desvios.

**Critérios de "sucesso" para a demo:**

| Grandeza | Faixa esperada (U_G = 2 cm/s) | Fonte |
|----------|-------------------------------|-------|
| εG global | 0,055 – 0,10 | Correlações (A&Y 0,055; Hikita 0,062; Reilly 0,105; deslizamento homogêneo ≈ 0,095) |
| V_L no eixo | 0,2 – 0,3 m/s | Riquarts (1981): 0,25 m/s |
| Inversão do V_L | r/R ≈ 0,7 | literatura clássica |
| Estatística | εG(t) oscila em torno de um patamar após ~15 s | — |

## 9. Ideias para slides

1. **Equações × CFD:** figura das correlações (até 2× de diferença) com o ponto do CFD por cima.
2. **Animação** da pluma e da superfície livre.
3. **"Uma coisa que a correlação não vê":** perfil radial de V_L com a inversão em r/R ≈ 0,7, que é a origem física do D_L do modelo de dispersão axial.
4. **Sensibilidade ao fechamento:** com e sem força de sustentação (εG e perfil radial mudam). Mostra por que a validação é obrigatória.
5. **Volta à cinética:** o Pe ≈ 0,3 do exemplo 2 mostra que o reator se comporta como CSTR na fase líquida, e é a hidrodinâmica que define a conversão.

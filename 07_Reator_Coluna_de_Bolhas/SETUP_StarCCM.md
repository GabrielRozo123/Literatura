# Coluna de Bolhas: passo a passo no STAR-CCM+ 2602

**Base:** tutorial *"Eulerian: Hibiki's Bubble Column"* (Simcenter STAR-CCM+ 2602 / 21.02.007). Física, fases, interação, contorno, condições iniciais, solver e S-Gamma foram **conferidos com as 10 páginas do tutorial**. O que muda em relação a ele está marcado com 🔁.

> **Ordem de trabalho recomendada:** monte primeiro o **2D axissimétrico** (passos 1 a 10, roda em minutos) para depurar o setup. Depois repita com o **3D** (o mesmo .sim, trocando geometria, malha e Space) para a apresentação.

## 0. Resumo do caso

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Coluna | D = 0,15 m, H = 1,2 m | D ≥ 0,15 m (critério de Wilkinson) |
| Líquido parado | H0 = 0,90 m (H0/D = 6), 0,3 m de espaço livre no topo | H/D > 5 |
| Sistema | ar–água, 25 °C, densidades constantes | |
| Aspersor | fundo inteiro (prato perfurado ideal) | distribuição uniforme, como nas correlações |
| U_G | **2 cm/s** (principal); 1 e 4 cm/s (opcional) | homogêneo / início da transição |
| Bolha | monodispersa, **5 mm** (S-Gamma opcional no passo 13) | d32 de 5,6–6,7 mm (Akita & Yoshida) |
| Tempo | Implicit Unsteady, 60 s, média de 20 a 60 s | |
| Malha | 2D: ~14 mil células · 3D: ~55 mil | |

Custo (estimativa, **não medido**): 2D em minutos; 3D de 1 a 3 h em 8 núcleos.

---

## 1. Baixar a geometria

Os STEP estão na branch `claude/determined-gauss-9wt81x` do repositório **Programacao**, pasta `coluna_bolhas/geometria/`:

| Arquivo | Uso | Faces nomeadas |
|---------|-----|----------------|
| `coluna_2D_axi_R75_H1200.step` | 2D axissimétrico: eixo da coluna = **X**, raio = **Y** (convenção do STAR, igual ao tutorial); placa de 10 mm em Z | `Aspersor` (x=0), `Topo` (x=1200), `Parede` (y=75), `Eixo` (y=0), `Plano_2D` (z=0), `Plano_tras` (z=10) |
| `coluna_3D_D150_H1200.step` | 3D: eixo **Z**, fundo em z = 0 | `Aspersor`, `Topo`, `Parede` |

Para baixar, use uma destas opções:

- **GitHub:** abra o arquivo na branch e clique em *Download raw file*.
- **Git:**
  ```bash
  git clone -b claude/determined-gauss-9wt81x https://github.com/GabrielRozo123/Programacao.git
  ```
- **Gerar de novo, com outras medidas** (precisa de `pip install cadquery`):
  ```bash
  python gera_geometria.py --D 150 --H 1200
  ```

## 2. Importar no STAR-CCM+

1. `File → New Simulation` (Parallel on Local Host, com o número de núcleos que tiver).
2. `File → Import → Import CAD Model...` e escolha o `.step`.
3. Na janela de importação:
   - **Import Mode** = *Create New Part*;
   - unidades **mm** (o STEP já declara mm; confira);
   - mantenha a separação das superfícies **por face do CAD**, para os nomes `Aspersor`, `Topo` etc. virarem superfícies da parte.
4. Confira em `Geometry → Parts → <parte> → Surfaces`: devem aparecer as faces nomeadas. Se vierem como `Face 1, 2, ...`, renomeie à mão: são poucas e dá para identificar cada uma clicando nela.

   > Alternativa: `Geometry → 3D-CAD Models → New` e importar o STEP dentro do 3D-CAD (aí as faces aparecem com nome e dá para renomear lá). Depois `Close 3D-CAD` e `New Geometry Part`.

5. Botão direito na parte → `Assign Parts to Regions`: **One region per part** e **One boundary per part surface**. Renomeie a região para `Coluna`.
6. **Só no 2D:** a fronteira `Plano_tras` não será usada (some no 2D).

## 3. Malha

| | 2D axissimétrico | 3D |
|--|------------------|----|
| Operação | `Geometry → Operations → New → Mesh → Automated Mesh (2D)` com a parte (o mesher usa a face `Plano_2D`, que está em z = 0) | `Automated Mesh` |
| Mesher | **Quadrilateral Mesher** (ou Polygonal) | **Surface Remesher + Trimmed Cell Mesher**, sem Prism Layer |
| Base Size | **2,5 mm** (≈ 30 × 480 ≈ 14 mil células) | **7,5 mm** (≈ 55 mil); versão grossa 10 mm (≈ 25 mil) |

Gere com `Execute` e confira em `Mesh → Diagnostics`. Se o *Automated Mesh (2D)* não estiver disponível, gere a malha 3D da placa e use `Mesh → Convert to 2D`.

## 4. Modelos físicos (= *Selecting the Physics Models*)

`Continua → Physics 1 → Select models`. No 2D deixe *Two Dimensional*; no 3D desmarque. Selecione **nesta ordem**:

| Group Box | 2D | 3D |
|-----------|----|----|
| Space | **Axisymmetric** | **Three Dimensional** |
| Time | 🔁 **Implicit Unsteady** (o tutorial usa Steady) | 🔁 **Implicit Unsteady** |
| Material | **Multiphase** (+ Multiphase Interaction automático) | idem |
| Multiphase Model | **Eulerian Multiphase (EMP)** (+ Gradients automático) | idem |
| Viscous Regime | **Turbulent** | idem |
| EMP Turbulence | **Phasic Turbulence** | idem |
| Optional Models | **Gravity** | idem |

> Por que transiente: no tutorial a mistura atravessa o tubo e o escoamento médio é estacionário. Numa coluna em batelada a pluma oscila e a superfície livre se mexe, então um cálculo *Steady* não converge ou dá um resultado sem significado físico.

## 5. Fases (= *Defining the Phases and Selecting Phase Models*)

**Water:** botão direito em `Physics 1 → Models → Multiphase → Phases → New`, renomeie para `Water`. Botão direito em `Water → Models → Select models`:

| Group Box | Modelo |
|-----------|--------|
| Enabled Models | Flow, Turbulent (pré-selecionados) |
| Material | **Liquid** |
| Turbulence | Reynolds-Averaged Navier-Stokes (automático) |
| Equation of State | **Constant Density** |
| Reynolds-Averaged Turbulence | **K-Epsilon Turbulence** → Realizable K-Epsilon Two-Layer, Wall Distance, Two-Layer All y+ Wall Treatment (automáticos) |

Em `Water → Models → Liquid → H2O → Material Properties`, coloque Density = 🔁 **997 kg/m³** e Dynamic Viscosity = 🔁 **8,9E-4 Pa-s** (água a 25 °C, as mesmas propriedades do script de correlações; o tutorial usa 1000 e 0,001).

**Air:** `Phases → New`, renomeie para `Air`. `Air → Models → Select models`:

| Group Box | Modelo |
|-----------|--------|
| Enabled Models | Flow, Turbulent (pré-selecionados) |
| Material | **Gas** |
| Turbulence | Reynolds-Averaged Navier-Stokes (automático) |
| Reynolds-Averaged Turbulence | **Turbulence Response** |
| Equation of State | **Constant Density** |
| Turbulence Response Models | **Issa Turbulence Response Model** (+ Wall Distance) |

Em `Air → Models → Gas → Air → Material Properties`, coloque Density = 🔁 **1,18 kg/m³** e Dynamic Viscosity = **1,8E-5 Pa-s**.

## 6. Interação de fases (= *Setting up the Phase Interactions*)

1. Botão direito em `Multiphase Interaction → Phase Interactions → New → Water → Air (Continuous-Dispersed)`. Renomeie para `Water-Air`.
2. Em `Water-Air → Models → Select models`, **desmarque *Auto-select recommended models*** e selecione:
   - **Enabled** (pré-selecionados): Continuous-Dispersed Topology, Drag Force, Multiphase Material, Interaction Length Scale, Interaction Area Density;
   - **Optional**: **Virtual Mass Force**, **Turbulent Dispersion Force**; 🔁 **Lift Force: no caso base, NÃO selecione**;
   - **Virtual Mass Coefficient**: Virtual Mass Coefficient.
3. Propriedades:

| Nó | Tutorial | **Nossa coluna** |
|----|----------|------------------|
| Drag Force → Drag Coefficient → Method | Tomiyama | **Tomiyama** |
| Interaction Length Scale → Method / Value | Constant / 0,003 m | Constant / 🔁 **0,005 m** |
| Multiphase Material → Surface Tension → Constant | (0,072 na parte S-Gamma) | **0,072 N/m** |
| Lift Force → Lift Coefficient | Constant −0,05 | 🔁 desligado no caso base. Rodadas de sensibilidade: −0,05 e +0,18 |

4. `Phases → Air → Models → Issa Turbulence Response Model` → **Phase Interaction = Water-Air**.

## 7. Reference Values (= *Setting Initial Conditions and Reference Values*, passo 2)

`Physics 1 → Models → Reference Values`:

| Propriedade | Tutorial | **Nossa coluna** |
|-------------|----------|------------------|
| Gravity | [−9,81, 0] m/s² | 2D: **[−9,81, 0]** (eixo = X) · 3D: 🔁 **[0, 0, −9,81]** |
| Reference Density | 1000 kg/m³ | 🔁 **1,18 kg/m³** |

> Por que mudar a densidade de referência: no tutorial o tubo está cheio de mistura. Aqui o topo da coluna está no **ar**. Com ρ_ref = ρ_ar, a pressão de 0 Pa no `Topo` é coerente com a coluna de ar acima da superfície livre.

## 8. Condições de contorno (= *Setting Boundary Conditions*)

Em `Regions → Coluna → Boundaries`, defina o **Type** de cada fronteira e, em seguida, `Phase Conditions`:

| Fronteira | Type | Air | Water |
|-----------|------|-----|-------|
| `Aspersor` | 🔁 **Velocity Inlet** | Physics Values → Volume Fraction = **1**; Velocity Magnitude = **0,02 m/s** (= U_G) | Volume Fraction = **0**; Velocity Magnitude = 0,02 m/s (sem efeito, pois α = 0); Turbulence Specification = Intensity + Length Scale, **0,005 m** (como no tutorial) |
| `Topo` | 🔁 **Pressure Outlet**, 0 Pa | Backflow Volume Fraction = **1** | Backflow Volume Fraction = **0** |
| `Parede` | Wall (No-slip) | — | — |
| `Eixo` (só 2D) | **Axis** | — | — |

> 🔁 No tutorial a mistura **atravessa** o tubo (80 % de água a 1,23 m/s + 20 % de ar a 1,61 m/s, saída tipo *Outlet*). Na coluna o líquido fica **em batelada**: só entra gás, que sai pelo topo. Como o aspersor cobre o fundo inteiro com α_ar = 1, Q_gás = U_G · A, a mesma definição usada nas correlações.

## 9. Condições iniciais (= *Setting Initial Conditions...*, passo 1)

1. Crie as Field Functions em `Tools → Field Functions → New → Scalar Field Function`. Use `[0]` no 2D (altura = X) e `[2]` no 3D (altura = Z):

   ```
   FF_alphaAgua :  ($${Centroid}[0] <= 0.9) ? 1 : 0
   FF_alphaAr   :  1 - ${FF_alphaAgua}
   FF_pHidro    :  ($${Centroid}[0] <= 0.9) ? (997 - 1.18)*9.81*(0.9 - $${Centroid}[0]) : 0
   ```

   (No 3D, troque `[0]` por `[2]` nas três.) Se o editor reclamar da sintaxe, use o autocompletar (*Centroid → [i]*).

2. Em `Physics 1 → Models → Multiphase → Phases`:

| Nó | Tutorial | **Nossa coluna** |
|----|----------|------------------|
| Water → Initial Conditions → Volume Fraction | 0,8 | 🔁 Method = *Field Function* → `FF_alphaAgua` |
| Water → Initial Conditions → Velocity | [1,23, 0] | 🔁 **[0, 0]** (3D: [0, 0, 0]) |
| Water → Turbulence Specification | Intensity + Length Scale, 0,005 m | igual; Intensity = 0,01 |
| Air → Initial Conditions → Volume Fraction | 0,2 | 🔁 *Field Function* → `FF_alphaAr` |
| Air → Initial Conditions → Velocity | [1,61, 0] | 🔁 **[0, 0]** |

3. `Physics 1 → Initial Conditions → Pressure` → *Field Function* → `FF_pHidro`. É a hidrostática do líquido e evita o "pulso" de pressão no início.

## 10. Solver (= *Running the Simulation...*)

`Solvers`:

| Nó | Propriedade | Tutorial | **Nossa coluna** |
|----|-------------|----------|------------------|
| Implicit Unsteady | Time-Step | — | 🔁 **0,005 s** (2D e 3D; se estiver estável depois de ~5 s, pode subir para 0,01 s no 3D) |
| Implicit Unsteady | Temporal Discretization | — | 1st order (demo) |
| Segregated EMP Flow → Phase Coupled Velocity | Implicit Under-Relaxation Factor | 0,4 | 0,4 |
| Segregated EMP Flow → Pressure | Under-Relaxation Factor | 0,5 | 0,5 |
| Volume Fraction | Implicit Under-Relaxation Factor | 0,3 | 0,3 |
| K-Epsilon Turbulence | Under-Relaxation Factor | 0,8 | 0,8 |

`Stopping Criteria`:

- 🔁 **Maximum Inner Iterations = 20**;
- 🔁 **Maximum Physical Time = 60 s**;
- **desative** *Maximum Steps* (o tutorial usa 2000 porque é estacionário).

Antes de rodar, crie os relatórios do passo 11.

## 11. Relatórios, monitores e cenas

**(a) Retenção gasosa global (comparação principal)**

1. `Derived Parts → New Part → Threshold`: região `Coluna`, escalar = **Volume Fraction da Water**, faixa **[0,5 ; 1]**. Nome: `Dispersao`.
2. `Reports → New Report → Volume Average`: escalar = **Volume Fraction da Air**, Parts = `Dispersao`. Nome: **`Holdup Global`**.
3. Botão direito no report → `Create Monitor and Plot from Report`. No monitor, Trigger = *Time Step*.

> No 2D axissimétrico o Volume Average já pondera pelo volume de revolução (2πr).

**(b) Conferência:** `Reports → Maximum` de `Centroid[0]` (3D: `[2]`) em `Dispersao`. Ele deve ficar perto de H0/(1−εG) ≈ 0,95–0,96 m.

**(c) Médias temporais:**

1. Botão direito em **`Monitors` → `New Monitor` → `Field Mean Monitor`** (fica em *Monitors*, não em *Solvers*). Crie dois:

   | Monitor | Field Function | Parts |
   |---------|----------------|-------|
   | `Media_alphaAr` | Volume Fraction da Air | `Coluna` |
   | `Media_vAgua` | componente **axial** da Velocity da Water: `[0]` no 2D, `[2]` no 3D | `Coluna` |

   Se o seletor não aceitar o vetor, crie uma Scalar Field Function com o componente (autocompletar → *Velocity of Water* → `[0]`).
2. Em cada monitor: **Trigger** = Time Step e **Start** (nó *Update* / *Start Time*) = **20 s**. Cada monitor cria a field function `Mean of ...`, que pode ser usada em cenas e plots.
3. `Derived Parts → New Part → Probe → Line`, com Resolution = **50**:

   | Probe | 2D axissimétrico (eixo X, raio Y) | 3D (eixo Z) |
   |-------|-----------------------------------|-------------|
   | `Radial_z060` (principal) | Point 0 = [0,6, 0,0, 0,0] · Point 1 = [0,6, 0,0745, 0,0] m | [−0,0745, 0,0, 0,6] → [0,0745, 0,0, 0,6] m |
   | `Radial_z030` (opcional) | [0,3, 0,0, 0,0] → [0,3, 0,0745, 0,0] m | [−0,0745, 0,0, 0,3] → [0,0745, 0,0, 0,3] m |
   | `Axial_centro` (opcional) | [0,0, 0,001, 0,0] → [1,2, 0,001, 0,0] m | [0,0, 0,0, 0,0] → [0,0, 0,0, 1,2] m |

   Ficar em 0,0745 (e não 0,075) evita que o último ponto caia exatamente na parede. Com z = 0,6 m (H/D = 4) a medida fica longe do aspersor e da superfície livre (≈ 0,95 m).
4. `Plots → New Plot → XY Plot`, com Parts = `Radial_z060`. X Type: *Direction* [0, 1, 0] no 2D (raio) ou [1, 0, 0] no 3D. Y Types: `Mean of Volume Fraction (Air)` em um plot e `Mean of Velocity[0] (Water)` em outro. Exporte como `perfil_alpha_Ug2.csv` e `perfil_vL_Ug2.csv`.

O que se espera: εG(r) maior no centro, ou com pico na parede se o lift estiver ligado; V_L subindo no centro (≈ 0,25 m/s, Riquarts) e **descendo perto da parede**, com troca de sinal em r ≈ 0,7R ≈ 0,052 m. No 2D axissimétrico essa simetria é forçada, e o perfil tende a ficar mais "comportado" que no 3D.

**(d) Para a plateia:** Scalar Scene da Volume Fraction (Air), com escala de 0 a 0,2 (no 3D, plano XZ em y = 0); vetores da velocidade da Water; Isosurface da Volume Fraction (Water) = 0,5 (superfície livre); `Animation` ou Hardcopy a cada 0,1 s de 10 a 40 s.

**Rodar:** clique em `Run`. Ao final, salve o .sim.

**Exportar** (igual ao passo 5 do tutorial, botão direito no plot → `Export`):

- plot do `Holdup Global` → **`holdup_Ug2.csv`** (1 cm/s → `holdup_Ug1.csv`, 4 cm/s → `holdup_Ug4.csv`);
- plots da Line Probe → `perfil_alpha_Ug2.csv` e `perfil_vL_Ug2.csv`.

## 12. Comparação com a literatura

Coloque os CSV em `Programacao/coluna_bolhas/star_exports/` e rode:

```bash
cd Programacao/coluna_bolhas
python compara_cfd_literatura.py --pasta star_exports --t-media 20
```

A saída é `resultados/fig_cfd_vs_literatura.png` com CFD × Akita & Yoshida × Hikita × Reilly × dados experimentais (`dados_experimentais.csv`).

| Grandeza (U_G = 2 cm/s) | Faixa esperada | Fonte |
|-------------------------|----------------|-------|
| εG global | 0,055 – 0,10 | Correlações (A&Y 0,055; Hikita 0,062; Reilly 0,105; deslizamento homogêneo ≈ 0,095) |
| V_L no eixo | 0,2 – 0,3 m/s | Riquarts (1981): 0,25 m/s |
| Inversão do V_L | r/R ≈ 0,7 | literatura clássica |
| εG(t) | oscila em torno de um patamar depois de ~15 s | — |

## 13. (Opcional) Distribuição de tamanho de bolhas: S-Gamma

Igual à parte 2 do tutorial. Salve uma cópia do .sim antes.

1. `Air → Models → Select models`: Optional Models = **Particle Size Distribution** → **S-Gamma** (Discrete Quadrature S-Gamma automático). Number of S-Gamma Equations = **Two Equation**.
2. `Air → Initial Conditions → Sauter Mean Diameter` = 🔁 **0,005 m**.
3. `Water-Air → Models → Select models`: **S-Gamma Breakup** + **S-Gamma Coalescence**.
4. `Interaction Length Scale → Method` = **Sauter Mean Diameter**. Surface Tension = 0,072 N/m. Breakup Rate: Cg = **5,0**, WeCrit = **0,23**. Collision Rate: Cg = **0,1** (valores do tutorial).
5. `Aspersor → Phase Conditions → Air → Physics Values → Sauter Mean Diameter` = 🔁 **0,005 m**.
6. `Clear Solution` e depois `Run`.

Isso fica bom como slide de "próximo nível": no regime heterogêneo (U_G > 5 cm/s) a coalescência gera bolhas grandes e só um modelo de população captura a queda de εG.

## 14. Ideias para slides

1. **Equações × CFD:** figura das correlações (até 2× de diferença entre elas) com o ponto do CFD por cima.
2. **Animação** da pluma e da superfície livre.
3. **"O que a correlação não vê":** perfil radial de V_L com a inversão em r/R ≈ 0,7, que é a origem do D_L do modelo de dispersão axial.
4. **Sensibilidade ao fechamento:** lift desligado × −0,05 × +0,18.
5. **Volta à cinética:** Pe ≈ 0,3, ou seja, a fase líquida é quase um CSTR, e a hidrodinâmica define a conversão.

## 15. E a reação química? Não é necessária no CFD

**Para a demo, não ative reação no STAR-CCM+.** A estratégia é **híbrida**:

```
CFD (só hidrodinâmica)  ──►  εG, d_b, a = 6εG/d, V_L(r), D_L
                                   │
                                   ▼
Equação de projeto (Python) ──►  kLa (Higbie: kL·a), Ha, conversão X
```

1. **O que a correlação erra é a hidrodinâmica.** No regime lento (Ha ≈ 0,01 ≪ 0,3, ver `resumo_projeto.txt`) a reação não altera o escoamento. A cinética entra depois, na equação de projeto, usando o εG e o `a` do CFD no lugar das correlações.
2. **Custo.** Espécies no EMP exigem mistura multicomponente, transferência de massa interfásica e reação. Isso multiplica o tempo de cálculo e as fontes de divergência.
3. **Validação.** Existem muitos dados de εG × U_G; dados simples de coluna com reação são raros.

**Quando valeria ativar** (fora do escopo da demo): reação rápida (Ha > 3, no filme), exotérmica (pontos quentes), seletividade sensível à retromistura, ou consumo forte de gás. O caminho no STAR seria: Water como *Multi-Component Liquid* (H2O + O2), *Interphase Mass Transfer* com kL de Higbie/Ranz–Marshall e uma fonte −k1·C via *User Source*.

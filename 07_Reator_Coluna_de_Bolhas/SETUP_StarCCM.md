# Coluna de Bolhas: caso Euler–Euler no STAR-CCM+ (versão "demo rápida")

**Base:** tutorial *"Eulerian: Hibiki's Bubble Column"* (Simcenter STAR-CCM+ 2602 / 21.02). Este roteiro troca a geometria e as condições de contorno por uma coluna de bolhas em batelada.

> ✅ Seções 3 a 5 conferidas com as páginas do tutorial 2602: *Selecting the Physics Models*, *Setting up the Phase Interactions*, *Setting Boundary Conditions* e *Setting Initial Conditions and Reference Values*. Ainda falta conferir com as próximas páginas: propriedades das fases, modelo de turbulência de cada fase, solver e malha.

**Geometria pronta (STEP, em mm):** `Programacao/coluna_bolhas/geometria/`

| Arquivo | Uso | Faces nomeadas |
|---------|-----|----------------|
| `coluna_3D_D150_H1200.step` | Caso principal 3D transiente; eixo Z, fundo em z = 0 | `Aspersor`, `Topo`, `Parede` |
| `coluna_2D_axi_R75_H1200.step` | **Versão rápida axissimétrica**, como no tutorial Hibiki. Eixo de simetria = X, raio = Y, placa de 10 mm em Z para usar *Convert to 2D* | `Aspersor`, `Topo`, `Parede`, `Eixo`, `Plano_2D`, `Plano_tras` |

Importação: `Geometry → Parts → New Shape Part → Import CAD Model` (ou *Import Surface*), com **Units = mm**. Se os nomes das faces não vierem do STEP, as superfícies são poucas e dá para renomear à mão (botão direito → *Split by Patch* e depois *Rename*).

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

## 1. Geometria

Importe o STEP (tabela acima) e faça `Assign Parts to Regions` (uma região **`Coluna`**, uma condição de contorno por superfície).

Para refazer no 3D-CAD: círculo de Ø 150 mm no plano XY e `Extrude` de 1200 mm em +Z. Para outras dimensões, use `python gera_geometria.py --D 150 --H 1200`.

**Versão axissimétrica:** depois de gerar a malha 3D da placa, use `Mesh → Convert to 2D` (a face `Plano_2D` em z = 0 vira o domínio). A fronteira `Eixo` deve ficar com Type = **Axis**, como no passo 2 de *Setting Boundary Conditions* do tutorial. Nesse caso a gravidade é **[−9,81, 0] m/s²**, porque o eixo da coluna é X.

## 2. Malha

`Geometry → Operations → New → Mesh → Automated Mesh`:

- Meshers: **Surface Remesher** + **Trimmed Cell Mesher** (sem Prism Layer).
- `Default Controls → Base Size` = **7,5 mm** (ou 10 mm na versão rápida). Target Surface Size = 100 %, Minimum Surface Size = 25 %.
- Gere a malha e confira a contagem (~55 mil células com 7,5 mm).
- **2D axissimétrico:** Base Size = **2,5 mm** gera ~30 × 480 ≈ 14 mil células depois do *Convert to 2D*. Roda em minutos; use para testar o setup antes do 3D.

> Alternativa mais "limpa": Directed Mesh (malha O-grid extrudada em Z). Vale a pena só se sobrar tempo.

## 3. Física (Physics Continuum)

Em `Continua → Physics 1`, desmarque *Two Dimensional* (no caso 3D) e selecione **nesta ordem**, como no tutorial:

| Group Box | 3D (principal) | 2D axissimétrico (rápido) |
|-----------|----------------|---------------------------|
| Space | Three Dimensional | **Axisymmetric** |
| Time | **Implicit Unsteady** | Implicit Unsteady (o tutorial usa *Steady*, mas uma coluna com superfície livre não fica estacionária) |
| Material | **Multiphase** (+ Multiphase Interaction, automático) | idem |
| Multiphase Model | **Eulerian Multiphase (EMP)** (+ Gradients, automático) | idem |
| Viscous Regime | **Turbulent** | idem |
| EMP Turbulence | **Phasic Turbulence** | idem |
| Optional Models | **Gravity** | idem |

**Fases** (`Models → Multiphase → Phases → New`; o tutorial usa os nomes `Water` e `Air`, e mantê-los facilita seguir as páginas):

| Fase | Propriedades |
|------|--------------|
| `Water` | líquido, densidade constante 997 kg/m³, μ = 8,9e-4 Pa·s; turbulenta (k-ε, a conferir na próxima página do tutorial) |
| `Air` | gás, densidade constante 1,18 kg/m³, μ = 1,8e-5 Pa·s; usa o **Issa Turbulence Response Model**, que vem com a fase dispersa |

**Interação de fases**: botão direito em `Multiphase Interaction → Phase Interactions → New → Water → Air (Continuous-Dispersed)` e renomeie para `Water-Air`. **Desmarque *Auto-select recommended models*** e selecione:

| Modelo | Tutorial Hibiki (tubo, 3 mm) | **Nossa coluna** | Observação |
|--------|------------------------------|------------------|-----------|
| Drag Force → Drag Coefficient | Tomiyama | **Tomiyama** | exige Gravity ligada; dá U∞ ≈ 0,23 m/s |
| Interaction Length Scale | Constant 0,003 m | **Constant 0,005 m** | d32 de 5,6–6,7 mm (Akita & Yoshida) |
| Interaction Area Density | pré-selecionado | pré-selecionado | a = 6α/d |
| Virtual Mass Force + Virtual Mass Coefficient | ✓ | ✓ (0,5) | |
| Turbulent Dispersion Force | ✓ | ✓ | |
| Lift Force → Lift Coefficient | Constant −0,05 | **caso base: desligado**; sensibilidade: −0,05 (tutorial) × +0,18 (Tomiyama, d = 5 mm) | o sinal decide se o gás vai para a parede ou para o centro: bom slide |

Depois: `Phases → Air → Models → Issa Turbulence Response Model` → **Phase Interaction = Water-Air** (passo 6 do tutorial; sem isso a fase dispersa não "sente" a turbulência).

**Reference Values** (`Physics 1 → Models → Reference Values`):

| Propriedade | Tutorial | **Nossa coluna** | Por quê |
|-------------|----------|------------------|---------|
| Gravity | [−9,81, 0] (eixo em X) | 3D: **[0, 0, −9,81]**; 2D axi: **[−9,81, 0]** | |
| Reference Density | 1000 kg/m³ (tubo cheio de água) | **1,18 kg/m³** | o topo da nossa coluna está no gás (espaço livre); com a densidade do ar, p = 0 na saída é coerente com a coluna de ar acima da superfície |

## 4. Condições de contorno

Diferença principal em relação ao tutorial: lá a mistura **atravessa** o tubo (entrada com 80 % de água a 1,23 m/s e 20 % de ar a 1,61 m/s, saída tipo *Outlet*). Na nossa coluna **o líquido fica em batelada**: só entra gás, e o gás sai por cima da superfície livre.

Em `Regions → Coluna → Boundaries → <fronteira> → Phase Conditions`:

| Fronteira | Tipo | `Air` | `Water` |
|-----------|------|-------|---------|
| `Aspersor` | **Velocity Inlet** | Volume Fraction = **1**, Velocity Magnitude = **U_G** (0,02 m/s) | Volume Fraction = 0; Turbulence Specification = *Intensity + Length Scale* (5 %, 0,005 m, igual ao tutorial) |
| `Topo` | **Pressure Outlet**, p = 0 Pa (não o *Outlet* do tutorial, porque aqui o fluxo líquido é zero) | Backflow Volume Fraction = **1** | Backflow Volume Fraction = 0 |
| `Parede` | Wall | Slip, se a sua versão permitir condição por fase (senão, No-slip) | No-slip |
| `Eixo` (só 2D) | **Axis** | — | — |

> Como o aspersor cobre o fundo inteiro com α_ar = 1, a vazão de gás é Q = U_G · A_coluna, o que coincide com a definição de U_G das correlações.

## 5. Condições iniciais

Crie duas *Field Functions* (`Tools → Field Functions → New → Scalar`):

```
FF_alphaAgua = ($${Centroid}[2] <= 0.9) ? 1 : 0
FF_pHidro    = ($${Centroid}[2] <= 0.9) ? (997 - 1.18)*9.81*(0.9 - $${Centroid}[2]) : 0
```

Onde aplicar (mesmo caminho do tutorial: `Physics 1 → Models → Multiphase → Phases → <fase> → Initial Conditions`):

| Nó | Tutorial | **Nossa coluna** |
|----|----------|------------------|
| Water → Volume Fraction | 0,8 (constante) | Method = *Field Function* → `FF_alphaAgua` |
| Air → Volume Fraction | 0,2 | *Field Function* → `FF_alphaAr` = `1 - ${FF_alphaAgua}` |
| Water/Air → Velocity | [1,23, 0] / [1,61, 0] m/s | **[0, 0, 0]** (líquido parado) |
| Water → Turbulence Specification | Intensity + Length Scale, 0,005 m | igual, com intensidade baixa (1 %) |
| `Physics 1 → Initial Conditions → Pressure` | — | *Field Function* → `FF_pHidro` (perfil hidrostático, evita o "pulso" inicial) |

> `$${Centroid}[2]` é a componente Z do centróide da célula (3D). **No 2D axissimétrico a altura é X**: troque por `$${Centroid}[0]`. Se o editor reclamar da sintaxe, use o autocompletar (*Centroid → [i]*).

## 6. Solver e critérios de parada

- `Implicit Unsteady`: **Time-Step = 0,005 s** nos primeiros 2 s (fase de partida), depois **0,01 s**. Temporal Discretization: 1st order (demo) ou 2nd order (final).
- `Stopping Criteria`: **Maximum Inner Iterations = 15**; **Maximum Physical Time = 60 s**. Desative Maximum Steps.
- Under-relaxation: manter os padrões do EMP. Se divergir, use Velocity 0,5 e Pressure 0,2.

## 7. Relatórios, monitores e cenas

**(a) Retenção gasosa global (comparação principal)**

1. `Derived Parts → New → Threshold`: região `Coluna`, escalar = **Volume Fraction da fase Water**, faixa **[0,5 ; 1]**. Nome: `Dispersao` (separa a dispersão do espaço livre).
2. `Reports → New → Volume Average`: escalar = **Volume Fraction da fase Air**, partes = `Dispersao`. Nome: **`Holdup Global`**.
3. Botão direito → `Create Monitor and Plot from Report` (trigger = Time Step).
4. Ao final: Plot → botão direito → `Export` → CSV com o nome **`holdup_Ug2.csv`** (para 1 cm/s use `holdup_Ug1.csv`, e assim por diante).

**(b) Altura da dispersão (conferência):** `Reports → Maximum` de `Centroid[2]` em `Dispersao`. Ela deve ficar em torno de H0/(1−εG) ≈ 0,95 m para εG ≈ 0,06.

**(c) Médias temporais (perfis locais):** `Solvers → Field Mean Monitor`, com início em **t = 20 s**, para Volume Fraction (Air) e Velocity (Water). Depois crie uma `Line Probe` radial em **z = 0,6 m** (de x = −0,075 a +0,075 m, 50 pontos) e exporte os campos médios. O que se espera ver:

- εG(r) mais ou menos parabólico, ou com pico na parede se o lift estiver ligado;
- líquido subindo no centro (≈ 0,25 m/s segundo Riquarts) e descendo na parede, com inversão em r/R ≈ 0,7.

**(d) Para a plateia:**

- `Scenes → Scalar`: plano XZ (y = 0), Volume Fraction (Air) com escala de 0 a 0,2.
- Uma segunda cena com vetores da velocidade da Water.
- `Isosurface` com Volume Fraction (Water) = 0,5 para mostrar a superfície livre subindo e oscilando.
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

## 10. E a reação química? (não é necessária no CFD)

**Para a demo, não ative reação no STAR-CCM+.** A estratégia é **híbrida**:

```
CFD (só hidrodinâmica)  ──►  εG, d_b, a = 6εG/d, V_L(r), D_L
                                   │
                                   ▼
Equação de projeto (Python) ──►  kLa (Higbie: kL·a), Ha, conversão X
```

Por quê:

1. **O que a correlação erra é a hidrodinâmica.** No regime lento (Ha ≈ 0,01 ≪ 0,3, ver `resumo_projeto.txt`) a reação não altera o escoamento: o calor e a variação de volume são desprezíveis. Então a cinética entra *depois*, na equação de projeto, usando o εG e o `a` do CFD no lugar das correlações. Para um seminário de cinética, essa ponte é o ponto principal.
2. **Custo.** Espécies no EMP exigem mistura multicomponente na fase líquida, transferência de massa interfásica (com *Interphase Mass Transfer*) e a reação. Isso multiplica o tempo de cálculo e abre mais fontes de divergência.
3. **Validação.** Não há dado experimental recente "simples" de coluna com reação para comparar. Já εG × U_G existe em quantidade.

**Quando valeria ativar** (extensão, fora do escopo da demo): reação rápida (Ha > 3, que ocorre no filme e depende da área local), reação exotérmica (pontos quentes), seletividade em série/paralelo sensível à retromistura, ou absorção de gás com consumo forte (o gás encolhe ao longo da coluna). O caminho no STAR seria: fase `Water` como *Multi-Component Liquid* (H2O + O2 dissolvido), *Interphase Mass Transfer* com kL de Higbie/Ranz–Marshall, e um termo-fonte de 1ª ordem −k1·C_O2 via *User Source* (Field Function).
